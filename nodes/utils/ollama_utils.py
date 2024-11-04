import re
import subprocess


def check_ollama_installed():
    try:
        subprocess.run(
            ["ollama", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def run_ollama_command(command):
    full_command = f"ollama {command}"
    # Remove any newlines and extra spaces
    full_command_str = str(" ".join(full_command.split()))

    try:
        result = subprocess.run(full_command_str, capture_output=True, text=True)
        output = result.stdout + result.stderr
        # Remove console mode error messages
        output = re.sub(
            r"failed to get console mode for std(out|err): The handle is invalid.\n",
            "",
            output,
        )

        # Extract useful information
        success_message = re.search(r"copied '(.+)' to '(.+)'", output)
        if success_message:
            return f"Successfully {success_message.group(0)}", ""

        # If no success message found, return the cleaned output
        return output.strip(), ""
    except Exception as e:
        return "", str(e)


def clean_result(result):
    # Split the result into lines
    lines = result[0].split("\n")

    # Initialize lists to store different types of information
    layer_info = []
    other_info = []

    for line in lines:
        # Remove ANSI escape codes and strip whitespace
        clean_line = re.sub(r"\x1b\[.*?[\@-~]", "", line).strip()

        if "layer" in clean_line:
            # Extract and format layer information
            layer_type = "existing" if "using existing layer" in clean_line else "new"
            sha = clean_line.split("sha256:")[-1].strip()
            layer_info.append(f"{layer_type.capitalize()} layer: sha256:{sha}")
        elif clean_line and not clean_line.startswith(("using", "creating")):
            # Add other relevant information
            other_info.append(clean_line)

    # Combine the formatted information
    cleaned_result = "\n".join(
        other_info + ["\n===========================\n"] + layer_info
    )
    return cleaned_result
