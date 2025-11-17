
# 1 Import the required Library
import pytsk3

# 2 Create a new IMG_Info object by opening the file and name object as diskimage
diskimage = pytsk3.Img_Info("DiskImage.001")
print("Disk image opened successfully!!")
print("#"*89)
#get size of disk image
image_size = diskimage.get_size()
size=image_size
#Make the bytes more readable by changing values to display in KB, MB, or GB and truncate to 2 decimal places
if size < 1024:
    print(f"The image file is {size} bytes in size")
    pass
elif size < 1024**2:
    size = size / 1024
    size = round(size, 2)
    print(f"The image file is {size} KB in size")
elif size < 1024**3:
    size = size / (1024**2)
    size = round(size, 2)
    print(f"The image file is {size} MB in size")
else:
    size = size / (1024**3)
    size = round(size, 2)
    print(f"The image file is {size} GB in size")

#get the number of sectors in the disk image
totalSectors = image_size/512
print(f"Total number of sectors in image is {totalSectors} ")
#get the boot sector
boot_sector = diskimage.read(0, 512)


# get the volume information
Myvolume_info = pytsk3.Volume_Info(diskimage)

print(f"Size of a block is {Myvolume_info.info.block_size}")
print("#"*89)
#finding endian type in human readable format
endian = Myvolume_info.info.endian
if endian == 1:
    endiantype = "Little Endian"
elif endian == 2:
    endiantype = "Big Endian"
else:
    endiantype = "Unknown Endian"
print(f'Endian in used is {endiantype}')
#Indicating if a backup exists or not.  0 = no backup, 1 = backup exists
backup = Myvolume_info.info.is_backup
if backup == 0:
    print('Partition table is not backup')
else:
    print('Partition table is backup')
print("#"*45)
print(f'Offset to partition table is {Myvolume_info.info.offset}')
#vstype 1 = DOS (MBR), 2 = GPT 
print(f'Type of partition table is {Myvolume_info.info.vstype}')
if Myvolume_info.info.vstype == pytsk3.TSK_VS_TYPE_DOS:
    print("Partition table is MBR")
elif Myvolume_info.info.vstype == pytsk3.TSK_VS_TYPE_GPT:
    print("Partition table is GPT" )
else:
    print("Unknown partition table type")
print(f'Number of partitions in partition table is {Myvolume_info.info.part_count}')
#Display parition table types with human readable format
partition_table = pytsk3.Volume_Info(diskimage)
print("List of Partitions \n")
print('Partition number \tDesc\t Start Sector\t Number of Sectors')
print('-' * 89)

partition_count = 1
for partition in partition_table:
    print(f"{partition_count:<20}{partition.desc.decode('ascii'):<24}{partition.start:<17}{partition.len:<16}")
    partition_count += 1
print("#"*89)
#number of unallocated partitions
unallocated_count = 0
for partition in partition_table:
    if partition.desc.decode('ascii') == 'Unallocated':
        unallocated_count += 1
print(f'Number of unallocated partitions: {unallocated_count}')

print("#"*89)



# 4 closes the disk image much like the close method unlinked a file from a program using Python File I/O.
diskimage.close()
