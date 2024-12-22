from griptape.artifacts import BlobArtifact, TextArtifact
from griptape.tasks import CodeExecutionTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


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
    CATEGORY = "Griptape/Agent Utils"
    OUTPUTS = ("STRING", "AGENT", "TASK")

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "STRING": (
                    "STRING",
                    {
                        "multiline": True,
                        "placeholder": "Text that will be passed as `input` to the code.",
                        "default": "This text will be passed as `input` to the code.",
                    },
                )
            }
        )
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
        return inputs

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        code = kwargs.get("code", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()

        prompt = self.get_prompt_text(STRING, input_string)

        # Build the task
        dynamic_task = build_CodeExecutionTask(code)

        try:
            agent.add_task(dynamic_task)
            result = agent.run(prompt)
            return (result.output_task.output.value, agent, dynamic_task)
        except Exception as e:
            return (str(e), None, None)
            print(e)
