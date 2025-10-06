#imports regular expressions library
import re

# Open and read the content of lab1example.txt
with open('week2code\lab1example.txt', 'r',encoding="utf8") as input_file:
    # Read the entire file content
    # text = input_file.read()
    # Split the text into lines for line-by-line processing
    lines = input_file.readlines()

# Prompt the user to input a regex search pattern
search_pattern = input("Please enter a regex search pattern: ")

# Validate regex pattern
compiled_pattern = re.compile(search_pattern)

# Print the matching results with line numbers
print("\nMatching Results:")
# Iterate through each line with its line number
for line_number, line in enumerate(lines, start=1):
    # Find all matches in the current line
    matches = compiled_pattern.findall(line)
    if matches:
        result = f"Line {line_number}: {matches}"
        print(result)

#Example cases to test
    """
    Email addresses:
\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b

Phone numbers (11 digits):
\b\d{11}\b

Words with both British and American spelling (specialise/specialize):
speciali[sz]e

Any word ending with "ed":
\b\w+ed\b

Any sequence of digits:
\d+

Words starting with a capital letter:
\b[A-Z][a-z]*\b

Lines containing the word "random":
.*random.*
    """