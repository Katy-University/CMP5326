import pytsk3
import hashlib
import os
#1
evidence_file = None
file_system = None

#2
menu = ("Program Options Menu\n"
        "--------------------\n"
        "\n"
        "1. Open an evidence file\n"
        "2. List Partitions in evidence file\n"
        "3. Open a partition in evidence file\n"
        "4. List files in partition\n"
        "5. Display details about file\n"
        "6. Exit program\n"
        "\n"
        )

# Function to print the menu string
def display_menu():
    print(menu)

# 3 Function to get an option from the user
def get_option():
    option_num = input("Please enter menu option> ")
    return option_num

#4
def open_evidence_file():

    global evidence_file

#prompt the user for the name of the evidence file to open
#if user presses enter, use the default file name "diskimageMT.001"
    evidence_file_name = input("Please enter name of evidence file to open (default: diskimageMT.001)> ")  
    if evidence_file_name == "":
        evidence_file_name = "diskimageMT.001"
        print(f"Using default file name {evidence_file_name}")
    else:
        print(f"Using file name {evidence_file_name}")

#open the evidence file and assign it to the evidence_file variable
#if the file does not exist, print an error message and return to the main menu
    if os.path.exists(evidence_file_name) == False:
        print("ERROR: File does not exist!!!")
        input("Press enter to continue")
        return
    else:
        evidence_file = pytsk3.Img_Info(evidence_file_name) #the actual opening of the file happens here
        print("Evidence file opened successfully!!")
        
        print("#"*45)
        # 4.1 Display the size of the disk image in raw bytes
        size =evidence_file.get_size()
        print(f"The image file is {size} bytes in size")
        totalSecors = size/512
        print(f"Total number of sectors in image is {totalSecors} ")

        volume_info = pytsk3.Volume_Info(evidence_file)
        print(f'Size of the block is set to {volume_info.info.block_size}')

        # 6
        partition_table = pytsk3.Volume_Info(evidence_file)
        
        # 14 Determining Partition Layout, Slide 18
        partition_table_type = partition_table.info.vstype
        if partition_table_type == pytsk3.TSK_VS_TYPE_DOS:
            print ("Partition table is MBR")
        elif partition_table_type == pytsk3.TSK_VS_TYPE_GPT:
            print ("Partition table is GPT")
        else:
            print ("Unknown partition table type")
        print("#"*45)
        
        input("Press enter to continue")
        return
#5
def list_partitions():
    global evidence_file
    partition_table = pytsk3.Volume_Info(evidence_file)
    print("List of Partitions \n\n")
    print('Partition number \tDesc\t Start Sector\t Number of Sectors')
    print('-' * 89)

    partition_count = 1
    for partition in partition_table:
        print(f"{partition_count:<20}{partition.desc.decode('ascii'):<24}{partition.start:<17}{partition.len:<16}")
        partition_count += 1
    print('\n\n')
    input("Press enter to continue")

def open_partition():
    global evidence_file, file_system
 
    if evidence_file is None:
        print("No evidence file is open. Please open an evidence file first.")
        return
 
    partition_table = pytsk3.Volume_Info(evidence_file)
 
    try:
        partition_num = int(input("Enter the partition number to open: "))
        partition = list(partition_table)[partition_num - 1]
    except (ValueError, IndexError):
        print("Invalid partition number.")
        return
 
    offset = partition.start * 512  # Assuming sector size is 512 bytes
    file_system = pytsk3.FS_Info(evidence_file, offset)
    print(f"Partition {partition_num} opened.")
        
    input("Press enter to continue")

def list_files_in_directory(dir_path):
    global file_system
 
    if file_system is None:
        print("No partition is open. Please open a partition first.")
        return
 
    try:
        directory = file_system.open_dir(path=dir_path)
        print(f"Listing files in directory: {dir_path}")
        for file in directory:
            print(file.info.name.name.decode("utf-8"))
    except IOError:
        print("Could not open directory.")
 

def list_files():
    directory_path = input("Enter the directory path to list files (default: root '/'): ")
    if directory_path == "":
        directory_path = "/"
    list_files_in_directory(directory_path)
    input("Press enter to continue")

def display_file_details():
    global file_system

    if file_system is None:
        print("No partition is open. Please open a partition first.")
        return

    file_path = input("Enter the file path to display details: ")
    if file_path == "":
        print("No file path entered.")
        return

    try:
        file_object = file_system.open(file_path)
    except IOError:
        print(f"Could not open file {file_path}.")
        return

    # Display basic file details
    print(f"File name: {file_object.info.name.name.decode('utf-8')}")
    print(f"File size: {file_object.info.meta.size} bytes")

    # Display timestamps
    print(f"Created time: {file_object.info.meta.crtime}")
    print(f"Modified time: {file_object.info.meta.mtime}")
    print(f"Accessed time: {file_object.info.meta.atime}")
    print(f"Changed time: {file_object.info.meta.ctime}")

    # Calculate and display hash value
    file_hash = hashlib.sha1()
    for file_attr in file_object:
        if file_attr.info.type == pytsk3.TSK_FS_ATTR_TYPE_DEFAULT:
            file_data = file_attr.read_random(0, file_attr.info.size)
            file_hash.update(file_data)
    print(f"SHA1 Hash: {file_hash.hexdigest()}")

    # Display file permissions (if available)
    if hasattr(file_object.info.meta, 'mode'):
        print(f"Permissions: {oct(file_object.info.meta.mode)}")

    input("Press enter to continue")

#6
def run_main():
    #7
    selected_option =0
    #8
    while selected_option != 6:
        #9
        display_menu()
        #10
        selected_option = get_option()
        #11
        if selected_option == '1':
            open_evidence_file()
        elif selected_option == '2':
            list_partitions()
        elif selected_option == '3':
            open_partition()
        elif selected_option == '4':
            list_files()
        elif selected_option == '5':
            display_file_details()
        elif selected_option == '6':
            print("Exiting Program.")
            #exit the program
            break
        else:
            print('Input not recongnised')

#12
if __name__ == "__main__":
    run_main()