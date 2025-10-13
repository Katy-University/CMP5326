import re

# Analyze suspicious files for various patterns
def analyze_suspicious_file(filename): 
    with open(filename, 'rb') as file:
        binary_data = file.read()
    hex_data = binary_data.hex()

    # Try to decode binary to text for text-based regexes
    text = binary_data.decode('utf-8', errors='replace')

    # Regex patterns for different types of suspicious data
    text_patterns = {
        'url': re.compile(r'https?://[^\s]+\.[^\s]{1,3}', re.IGNORECASE),
        'email': re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', re.IGNORECASE),
        'ipv4': re.compile(r'(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|1?\d{1,2})){3}'),
        'base64_blob': re.compile(r'(?:[A-Za-z0-9+/]{4}){4,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'),

    }

    # Patterns that should be applied against hex representation
    hex_patterns = {
        'long_hex': re.compile(r'[0-9a-fA-F]{32,}'),
    }

    # Search text-based patterns in the decoded text
    for name, pattern in text_patterns.items():
        matches = list(pattern.finditer(text))
        if matches:
            print(f"Suspicious {name} activity detected ({len(matches)} matches):")
            for m in matches:
                # show a truncated match to avoid flooding output
                snippet = m.group(0)
                if len(snippet) > 200:
                    snippet = snippet[:200] + '...'
                print('  ', snippet)

    # Search hex-based patterns in the hex data
    for name, pattern in hex_patterns.items():
        matches = list(pattern.finditer(hex_data))
        if matches:
            print(f"Suspicious {name} activity detected ({len(matches)} matches) in hex dump:")
            for m in matches:
                print('  ', m.group(0))

if __name__ == "__main__":
    filename = input("Enter the filename: ")
    analyze_suspicious_file(filename)
