# Create a new virtual environment
python3 -m venv pip-test

# Activate the virtual environment
source pip-test/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Remove the virtual environment
rm -rf pip-test