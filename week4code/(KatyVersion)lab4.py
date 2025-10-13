import re # import regular expressions module

# Function to identify file type based on hex signature
def identifyFileType(filename):
    with open(filename,'rb') as file:
        binaryData = file.read()
    hexData = binaryData.hex()

# Dictionary of common file signatures
    fileSignatures = {
        '89504e47': 'PNG image',
        'ffd8ffe0': 'JPEG image',
        '504b0304': 'ZIP archive',
        '25504446': 'PDF document',
    }

# Check the file signature against known signatures
    for signature, fileType in fileSignatures.items(): # loop through signatures
        if hexData.startswith(signature): # check if file starts with signature
            print("File type identified:", fileType) # print file type
            return
    print("Unknown file type")

if __name__ == "__main__":
    mysteryfile = input("Enter the filename: ")
    identifyFileType(mysteryfile)

