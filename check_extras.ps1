# Create a new virtual environment
python -m venv pip-test

# Activate the virtual environment
.\pip-test\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Remove the virtual environment
Remove-Item -Recurse -Force pip-test