import re

# Open and read the content of lab1example.txt
with open('lab1example.txt', 'r', encoding="utf8") as file:
    text = file.read()

# Define a regex pattern to match email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Find all email addresses in the text
emails = re.findall(email_pattern, text)

# Print the extracted email addresses with numbering
if emails:
    print("Extracted Emails:")
    for i, email in enumerate(emails, 1):
        print(f"{i}. {email}")
else:
    print("No emails found.")

# Optionally, save the results to a file
with open('extracted_emails.txt', 'w') as output_file:
    for email in emails:
        output_file.write(email + '\n')
