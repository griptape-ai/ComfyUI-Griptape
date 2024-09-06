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

    # ic(full_command_str)
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
