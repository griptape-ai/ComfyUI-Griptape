import sys
import os

# Get the directory of the current script (__file__ is the path to the current file)
current_dir = os.path.dirname(__file__)
# Calculate the path to the 'py' directory
py_dir = os.path.abspath(os.path.join(current_dir, "..", "py"))

# Add the 'py' directory to the front of the search path
sys.path.insert(0, py_dir)
