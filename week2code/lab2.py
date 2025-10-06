#imports regular expressions library
import re

# Open and read the content of lab1example.txt
with open('week2code\lab1example.txt', 'r',encoding="utf8") as input_file:
    # text = file.read()
    # Read the file line bye line for tracking line numbers
    lines = input_file.readlines()

# Prompt the user to input a regex search pattern
search_pattern = input("Please enter a regex search pattern: ")

# Validate regex pattern
compiled_pattern = re.compile(search_pattern)

# Define a regex pattern to match email addresses
# email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Find all email addresses in the text
# emails = re.findall(email_pattern, text)

# Print the matching results with line numbers
print("\nMatching Results:")
for line_number, line in enumerate(lines, start=1):
    matches = compiled_pattern.findall(line)
    if matches:
        result = f"Line {line_number}: {matches}"
        print(result)
