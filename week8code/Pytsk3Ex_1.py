'''
The following skeleton code is designed to help you with the structure of the practice program
for the pytsk Workshop 1
As always, if you feel like something does not make sense, ask for help from your tutor, or
read the relevant documentation.
'''

# 1 Import the required Library
import pytsk3

# 2 Create a new IMG_Info object by opening the file and name object as diskimage
diskimage = pytsk3.Img_Info("week8code\\diskimageMT.001")

# 3 Display the size of the disk image in raw bytes
print(f"The image file size is {diskimage.get_size()} bytes in size")

# 4 closes the disk image much like the close method unlinked a file from a program using Python File I/O.
diskimage.close()

# 5 Display the number of sectors there are in the disk image file
totalsectors = diskimage.get_size()/512
print(f"Total Number of sectors in the image is {totalsectors}")

# 6 Create a Volume_Info object for the Img_Info object to get a Volume_Info object containing the partitions defined in the disk image
volume_info = pytsk3.Volume_Info(diskimage)

# 7 Displays the number of partitions pytsk3 has identified in the disk image.
TotalPartitions = volume_info.info.part_count
print(f"Number of partitions in the image is {TotalPartitions}")

# 8 Defines the start of a for loop for processing each partition in the disk image.
offsets = []
i=1
for volume in volume_info:
    # 9 displays a description of the partition’s type, start sector and number of sectors in the partition
    # Convert the bytes into a string for volume.desc
    volume_desc = volume.desc.decode('ascii')
    print(f" Partition type {i} {volume_desc}, start LBA {volume.start}, number of sectors {volume.len}")
    i+=1
    # 11 This statement adds the current volume’s start sector to the end of the list each iteration
    offsets.append(volume.start)


# 12 Display the contents of the partitions list
print(f"Partition offsets are {offsets}")