
# 1 Import the required Library
import pytsk3

# 2 Create a new IMG_Info object by opening the file and name object as diskimage
Mydiskimage = pytsk3.Img_Info("DiskImage.001")

#get size of disk image
image_size = Mydiskimage.get_size()
print(f"The image file size is {image_size} bytes in size")

#get the number of sectors in the disk image
totalSecors = image_size/512
print(f"Total number of sectors in image is {totalSecors} ")

#get the boot sector
boot_sector = Mydiskimage.read(0, 512)
#print the boot sector in hexadecimal format
print("Boot Sector in Hexadecimal Format:")
print(boot_sector.hex())

# get the volume information
Myvolume_info = pytsk3.Volume_Info(Mydiskimage)

print(f"Size of a block is {Myvolume_info.info.block_size}")
# above line gets the block size of the volume in logical bytes, not physical bytes normally 4096 bytes

print(f'Endian in used is {Myvolume_info.info.endian}')
# 1 = Little Endian（小端） 2 = Big Endian（大端）, little endian is the most common format used in modern computer systems. 
# little-endian format stores the least significant byte at the lowest memory address.(means reverse order)

print(f'Partition table is backup {Myvolume_info.info.is_backup}')
# 0 = No, 1 = Yes, indicates whether the partition table is a backup copy.
# so if it is 0 it means it is the primary partition table.

print(f'Offset to partition table is {Myvolume_info.info.offset}')
# Offset to partition table is 0 means the partition table starts at the beginning of the disk image.

print(f'Number of partitions in partition table is {Myvolume_info.info.part_count}')
# TSK counts all of the following as separate "partition entries":
# - Valid partitions
# - Unallocated space (UNALLOC)
# - Metadata regions (META)
# - Protective MBR entry
# - GPT entries (including empty slots)
# This is why the count is typically much higher than what you see in Windows/Mac.
# For example, a GPT disk commonly includes:
# Protective MBR, unallocated space, primary GPT header/entries,
# actual partitions, partition gaps, and backup GPT header/entries.

print(f'Type of partition table is {Myvolume_info.info.vstype}')
# Determine the type of partition table 
#Type of partition table is 1 means MBR
#Type of partition table is 5 means GPT
#https://www.sleuthkit.org/sleuthkit/docs/api-docs/4.5/tsk__vs_8h.html#a0659bf1a83a42f2f5795f807e73ce0ff

if Myvolume_info.info.vstype == pytsk3.TSK_VS_TYPE_DOS:
    print("Partition table is MBR")
elif Myvolume_info.info.vstype == pytsk3.TSK_VS_TYPE_GPT:
    print("Partition table is GPT" )

# 4 closes the disk image much like the close method unlinked a file from a program using Python File I/O.
Mydiskimage.close()
