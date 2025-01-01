export const code_execution_templates = {
  "Custom code": `#Write your code here
output = input`,

  "Count the characters in a string": `output = len(input)`,

  "Count the words in a string": `output = len(input.split())`,

  "Sort the words in a string": `output = ' '.join(sorted(input.split()))`,

  "Extract hashtags from the input": `""" Example Input:

This paragraph is one of the best #humblebrag #kindness #gratitude paragraphs on the internet.
"""

import re

output = ' '.join(re.findall(r'#\\w+', input))`,

  "Extract a column by name from CSV": `""" Example Input:

Name, Age, Country
John, 25, New Zealand
Jane, 30, New Zealand
Carol, 35, Australia
Bob, 40, USA 
"""

import csv
from io import StringIO

def extract_column(csv_data, column_name):
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)
    return [row[column_name] for row in reader if column_name in row]

# Example: Extract column "Name"
output = extract_column(input, "Name")
`,

  "Filter rows based on condition from CSV": `""" Example Input:

Name, Age, Country
John, 25, New Zealand
Jane, 30, New Zealand
Carol, 35, Australia
Bob, 40, USA
"""

import csv 
from io import StringIO 
 
def filter_rows(csv_data, column_name, condition): 
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True) 
    return [row for row in reader if row.get(column_name) == condition] 
 
# Example: Filter rows where "Country" is "New Zealand" 
output = str(filter_rows(input, "Country", "New Zealand"))`,

  "Convert CSV to JSON": `""" Example Input:

Name, Age, County
John, 25, USA
Jane, 30, CAnada
Carol, 35, Australia
Bob, 40, USA
"""

import csv
import json
from io import StringIO
def csv_to_json(csv_data):
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)
    return json.dumps([row for row in reader], indent=2)

# Example: Convert CSV to JSON
output = csv_to_json(input)`,

  "Sort rows based on column from CSV": `""" Example Input:

Name,Age,Country
John,25,New Zealand
Jane,30,New Zealand
Carol,35,Australia
Bob,40,USA
"""

import csv
from io import StringIO

def sort_by_column(csv_data, column_name):
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)
    sorted_rows = sorted(reader, key=lambda row: row[column_name])
    return "\\n".join([",".join(sorted_rows[0].keys())] + [",".join(row.values()) for row in sorted_rows])

# Example: Sort rows by "Name"
output = sort_by_column(input, "Name")`,

  "Summarize Data by Group from CSV": `""" Example Input:

Name,Age,Country
John,25,New Zealand
Jane,30,New Zealand
Carol,35,Australia
Bob,40,USA
"""

import csv
from io import StringIO
from collections import Counter

def summarize_by_group(csv_data, group_column):
    reader = csv.DictReader(StringIO(csv_data), skipinitialspace=True)
    return dict(Counter(row[group_column] for row in reader))
# Summarize data by "Country"
output = summarize_by_group(input, "Country")`
}
