import os

import toml


def get_version():
    # Get the directory one level above the current script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Construct the path to pyproject.toml
    pyproject_path = os.path.join(parent_dir, "pyproject.toml")

    # Debug: Print the path being used
    # print(f"Reading pyproject.toml from: {pyproject_path}")

    # Load the toml file
    pyproject = toml.load(pyproject_path)
    return pyproject["tool"]["poetry"]["version"]
