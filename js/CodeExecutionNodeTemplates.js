
export const code_execution_templates = {
  "Custom code": "# Write your code here\n\noutput = input",
  "Count the characters in a string": "output = len(input)",

  "Count the words in a string": "output = len(input.split())",

  "Sort the words in a string": "output = ' '.join(sorted(input.split()))",

  "Extract hashtags from the input": "# Example Input:\n\
# This paragraph is one of the best #humblebrag #kindness #gratitude\n\n\
import re \n\
output = ' '.join(re.findall(r'#\\w+', input))",

  "Extract a column by name from CSV": "# Example Input:\n\
# Name, Age, Country\n\
# John, 25, New Zealand\n\
# Jane, 30, New Zealand\n\
# ... \n\n\
import csv \n\
from io import StringIO\n\
\n\
def extract_column(csv_data, column_name): \n\
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)\n\
    return [row[column_name] for row in reader if column_name in row]\n\
\n\
# Example: Extract column \"Name\"\n\
output = extract_column(input, \"Name\")\n\
",

  "Filter rows based on condition from CSV": "# Example Input:\n\
# Name, Age, Country\n\
# John, 25, New Zealand\n\
# Jane, 30, New Zealand\n\
# Carol, 35, Australia\n\
# Bob, 40, USA\n\
# ... \n\n\
import csv \n\
from io import StringIO \n\
 \n\
def filter_rows(csv_data, column_name, condition): \n\
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True) \n\
    return [row for row in reader if row.get(column_name) == condition] \n\
 \n\
# Example: Filter rows where \"Country\" is \"New Zealand\" \n\
output = str(filter_rows(input, \"Country\", \"New Zealand\"))",

  "Convert CSV to JSON": "# Example Input:\n\
# Name, Age, Country\n\
# John, 25, USA\n\
# Jane, 30, Canada\n\
# ... \n\n\
import csv\n\
import json\n\
from io import StringIO\n\
\n\
def csv_to_json(csv_data):\n\
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)\n\
    return json.dumps([row for row in reader], indent=2)\n\
\n\
# Example: Convert CSV to JSON\n\
output = csv_to_json(input)",

  "Sort rows based on column from CSV": "# Example Input:\n\
# Name,Age,Country\n\
# John,25,New Zealand\n\
# Jane,30,New Zealand\n\
# Carol,35,Australia\n\
# Bob,40,USA\n\
# ... \n\n\
import csv\n\
from io import StringIO\n\
\n\n\
def sort_by_column(csv_data, column_name):\n\
    reader = csv.DictReader(StringIO(csv_data))\n\
    sorted_rows = sorted(reader, key=lambda row: row[column_name])\n\
    return \"\\n\".join([\",\".join(sorted_rows[0].keys())] + [\",\".join(row.values()) for row in sorted_rows])\n\
\n\
# Example: Sort rows by \"Name\"\n\
output = sort_by_column(input, \"Name\")\
",

  "Summarize Data by Group from CSV": "# Example Input:\n\
# Name,Age,Country\n\
# John,25,New Zealand\n\
# Jane,30,New Zealand\n\
# Carol,35,Australia\n\
# Bob,40,USA\
# ... \n\n\
import csv\n\
from io import StringIO\n\
from collections import Counter\n\
\n\
def summarize_by_group(csv_data, group_column):\n\
    reader = csv.DictReader(StringIO(csv_data))\n\
    return dict(Counter(row[group_column] for row in reader))\n\
\n\
# Summarize data by \"Country\"\n\
output = summarize_by_group(input, \"Country\")\
"
}

  
