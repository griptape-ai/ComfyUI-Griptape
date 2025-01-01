import ast
from typing import Any, Tuple

from griptape.artifacts import BlobArtifact, TextArtifact
from griptape.tasks import CodeExecutionTask

from ...py.griptape_settings import GriptapeSettings
from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class DangerousCodeChecker(ast.NodeVisitor):
    allowed_imports = {
        # Date and Time
        "datetime",
        "time",
        "calendar",
        "zoneinfo",
        # Text Processing
        "re",
        "string",
        "difflib",
        "textwrap",
        "unicodedata",
        # Data Formats
        "json",
        "csv",
        "yaml",  # if pyyaml is installed
        "toml",  # if toml is installed
        "xml.etree.ElementTree",
        "xml.dom.minidom",
        "html.parser",
        # Math and Numbers
        "math",
        "decimal",
        "fractions",
        "numbers",
        "statistics",
        "random",
        # Data Structures and Algorithms
        "collections",
        "heapq",
        "bisect",
        "array",
        "queue",
        "dataclasses",
        # Functional Programming
        "itertools",
        "functools",
        "operator",
        # File and Path Operations (safe subset)
        "pathlib",
        "os.path",
        "fileinput",
        "configparser",
        "zipfile",
        "tarfile",
        "gzip",
        "bz2",
        "lzma",
        # Input/Output
        "io.StringIO",
        "io.BytesIO",
        "io.TextIOWrapper",
        # Data Types
        "typing",
        "enum",
        "uuid",
        # Encoding/Decoding
        "base64",
        "binascii",
        "codecs",
        "urllib.parse",
        # Development Tools
        "pdb",
        "unittest",
        "doctest",
        "timeit",
        # Formatting and Printing
        "pprint",
        "reprlib",
        "rich",
        # Commonly Used Third-Party Libraries (if installed)
        "numpy",  # Numerical computing
        "pandas",  # Data analysis
        "scipy",  # Scientific computing
        "matplotlib",  # Plotting
        "seaborn",  # Statistical visualization
        "PIL.Image",  # Image processing
        "PIL.ImageDraw",
        "PIL.ImageFont",
        # Compression and Archiving
        "zlib",
        "hashlib",  # Cryptographic hashing
        # Templating
        "string.Template",
        "jinja2",  # if installed
        # Logging
        "logging",
        "logging.config",
        "logging.handlers",
    }

    def __init__(self):
        super().__init__()
        self.unapproved_imports = []

        # Create a mapping of module to allowed submodules
        self.allowed_submodules = {}
        for imp in self.allowed_imports:
            parts = imp.split(".")
            if len(parts) > 1:
                if parts[0] not in self.allowed_submodules:
                    self.allowed_submodules[parts[0]] = set()
                self.allowed_submodules[parts[0]].add(parts[1])

    def visit_Import(self, node):
        for alias in node.names:
            # Check if the full import path is allowed
            if alias.name not in self.allowed_imports:
                # Check if it's a submodule of an allowed import
                parts = alias.name.split(".")
                if not (
                    len(parts) > 1
                    and parts[0] in self.allowed_submodules
                    and parts[1] in self.allowed_submodules[parts[0]]
                ):
                    self.unapproved_imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module is None:  # Handle relative imports
            self.unapproved_imports.append("relative import")
            return

        # If the module itself is in allowed_imports, everything is fine
        if node.module in self.allowed_imports:
            return

        # Check if we're importing from a module that has allowed submodules
        if node.module in self.allowed_submodules:
            for alias in node.names:
                # Check if the specific import is allowed
                if alias.name not in self.allowed_submodules[node.module]:
                    self.unapproved_imports.append(f"{node.module}.{alias.name}")
        else:
            # The module isn't in our allowed list at all
            self.unapproved_imports.append(node.module)

    def visit_Call(self, node):
        # Check for dangerous calls
        if isinstance(node.func, ast.Name) and node.func.id in {"exec", "__import__"}:
            self.unapproved_imports.append(f"{node.func.id}() call")
        self.generic_visit(node)


def check_script_for_danger(script):
    try:
        # Parse the script into an AST
        tree = ast.parse(script)
        checker = DangerousCodeChecker()
        checker.visit(tree)

        # If no unapproved imports are found, the script is safe
        is_safe = len(checker.unapproved_imports) == 0
        return is_safe, checker.unapproved_imports
    except SyntaxError as e:
        # Return as unsafe if there is a syntax error
        return False, [f"Syntax error: {e}"]


any = AnyType("*")
examples = {
    "Word count": "output = len(input.split())",
    "Reverse the input": "output = input[::-1]",
    "Sort a list of numbers": "output = sorted([int(x) for x in input.split(',')])",
    "Sort a list of words": "output = sorted(input.split())",
    "Find unique words": "output = list(set(input.split()))",
    "Extract numbers": "output = re.findall(r'\\d+', input)",
    "Replace words": "output = input.replace('old', 'new')",
    "Find email addresses": "output = re.findall(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b', input)",
    "Remove spaces and punctuation": """def clean_text(text):
    import string
    text = text.strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())

output = clean_text(input)
""",
}

examples_keys_list = list(examples.keys())


def build_CodeExecutionTask(code: str) -> CodeExecutionTask:
    """
    Takes Python code as a string and builds a CodeExecutionTask
    that executes the provided code. The return value of the code is
    automatically wrapped in an appropriate artifact.
    """
    function_name = "dynamic_task"
    exec_globals = {"TextArtifact": TextArtifact, "BlobArtifact": BlobArtifact}
    exec_locals = {}

    # Properly indent the user code to fit inside the function
    indented_code = "\n".join([f"    {line}" for line in code.splitlines()])

    # Wrap the user's code with return type inference
    wrapped_code = f"""
def {function_name}(task):
    # Map 'input' to 'task.input' for easier access
    input = task.input.value

{indented_code}

    # Convert the output to ensure consistent type handling
    output = locals().get('output', None)
    if output is None:
        raise ValueError("User code must define an 'output' variable.")

    # Determine artifact type based on the return value
    if isinstance(output, str):
        return TextArtifact(output)
    else:
        # Convert non-string outputs to string for TextArtifact
        return TextArtifact(str(output)) if not isinstance(output, bytes) else BlobArtifact(output)
"""
    # Compile and execute the code
    exec(wrapped_code, exec_globals, exec_locals)

    # Extract the dynamically created function
    dynamic_function = exec_locals[function_name]

    # Return a CodeExecutionTask that uses the dynamic function
    return CodeExecutionTask(on_run=dynamic_function)


class gtUICodeExecutionTask(gtUIBaseTask):
    DESCRIPTION = "Executes python code as a task.\nThe code takes the `input` from the task and should define an `output` variable that will be returned as the task's output."
    CATEGORY = "Griptape/Code"
    OUTPUTS = ("STRING", "AGENT", "TASK")

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "input": (
                    "STRING",
                    {
                        "multiline": False,
                        "placeholder": "Text that will be passed as `input` to the code.",
                        "default": "This text will be passed as `input` to the code.",
                    },
                ),
            }
        )
        del inputs["required"]["STRING"]
        del inputs["optional"]["input_string"]
        inputs["optional"].update(
            {
                "examples": (
                    (),
                    {
                        "default": "Custom code",
                        "tooltip": "Select an example code snippet to replace the default code.",
                    },
                ),
                "code": (
                    "STRING",
                    {
                        "placeholder": "Python code to execute. \n`input` is any input text.\n`output` will be returned as the task output.\n\noutput = input.upper()",
                        "default": """# Python code to execute.
# `input` is any input text.
# `output` will be returned as the task output

output = input.upper()
""",
                        "multiline": True,
                        "tooltip": """Python code to execute. 
The code should define an `output` variable that will be returned as the task's output.

Example:
# Sorts a list of numbers
def sort_numbers(numbers):
    return sorted(numbers)

output = str(sort_numbers([int(x) for x in input.split(',')]))
""",
                    },
                ),
            }
        )
        inputs["hidden"] = {"unique_id": "UNIQUE_ID"}
        return inputs

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("input")
        unique_id = kwargs.get("unique_id", None)
        print(unique_id)
        # input_string = kwargs.get("input_string", None)
        code = kwargs.get("code", None)
        agent = kwargs.get("agent", None)
        settings = GriptapeSettings()
        code_execution = settings.get_settings_key("allow_code_execution")
        code_execution_dangerous = settings.get_settings_key(
            "allow_code_execution_dangerous"
        )
        print(code_execution)
        # code_execution = kwargs.get("code_execution", False)
        if not code_execution:
            return (
                "❌ Code execution is disabled.\n\nTo enable it, please go to the Griptape Settings and turn on Enable Code Execution Nodes.",
                None,
                None,
            )
        if not agent:
            agent = Agent()

        prompt = STRING

        if not code_execution_dangerous:
            # Check the code for dangerous opoerations
            safe_code, response = check_script_for_danger(code)

            if not safe_code:
                return (
                    f"❌ Script contains dangerous operations. {response}",
                    None,
                    None,
                )

        # Build the task
        dynamic_task = build_CodeExecutionTask(code)

        try:
            agent.add_task(dynamic_task)
            result = agent.run(prompt)
            return (result.output_task.output.value, agent, dynamic_task)
        except Exception as e:
            return (str(e), None, None)
            print(e)
