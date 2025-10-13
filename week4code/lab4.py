import re # import regular expressions module

# Function to identify file type based on hex signature
def identifyFileType(filename):
    with open(filename,'rb') as file:
        binaryData = file.read()
    hexData = binaryData.hex()

# Dictionary of common file signatures
    fileSignatures = {
        '89504e47': 'PNG image',
        '47494638': 'GIF image',
        'ffd8ffe0': 'JPEG image',
        '504b0304': 'ZIP archive',
        '25504446': 'PDF document',
    }

# Check the file signature against known signatures
    for signature, fileType in fileSignatures.items():
        if hexData.startswith(signature):
            print("File type identified:", fileType)
            return
    print("Unknown file type")

if __name__ == "__main__":
    mysteryfile = input("Enter the filename: ")
    identifyFileType(mysteryfile)

