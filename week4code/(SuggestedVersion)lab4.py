import re # Import the regular expressions module

# Function to identify file type based on hex signature using regex
def identify_file_type(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    hex_data = binary_data.hex()


    #Regex patterns for different file types
    jpeg_pattern_raw = r'\xff\xd8\xff'  # JPEG files start with these bytes
    zip_pattern_raw = r'\x50\x4b\x03\x04'  # ZIP files start with these bytes
    pdf_pattern_raw = r'\x25\x50\x44\x46'  # PDF files start with these bytes
    png_pattern_raw = r'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'  # PNG files start with these bytes


    # Compiled regex patterns
    jpeg_pattern_compiled = re.compile(jpeg_pattern_raw) 
    zip_pattern_compiled = re.compile(zip_pattern_raw) 
    pdf_pattern_compiled = re.compile(pdf_pattern_raw)
    png_pattern_compiled = re.compile(png_pattern_raw) 

    # Check the file signature against known signatures using regex
    if jpeg_pattern_compiled.match(binary_data):
        print("File type identified: JPEG image")
    elif zip_pattern_compiled.match(binary_data):
        print("File type identified: ZIP archive")
    elif pdf_pattern_compiled.match(binary_data):
        print("File type identified: PDF document")
    elif png_pattern_compiled.match(binary_data):
        print("File type identified: PNG image")
    else:
        print("File type not identified")       

# Main function
if __name__ == "__main__":
    filename = input("Enter the filename: ")
    identify_file_type(filename)
