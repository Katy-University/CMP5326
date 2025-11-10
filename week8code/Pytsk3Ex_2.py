# 1 Import the required Library
import pytsk3

# 2 Create a new IMG_Info object by opening the file and name object as diskimage
file_name = "diskimageMT.001"
diskimage = pytsk3.Img_Info(file_name)

# 4 Display a message to the iuser that the image has been loaded:
print(f"Loaded {file_name} image file.")
print("*"*35)

# 4,2 closes the disk image much like the close method unlinked a file from a program using Python File I/O.
diskimage.close()

# 5 Display the number of sectors there are in the disk image file
print(f"The image file is {diskimage.get_size()} bytes in size")
print(f"Total number of sectors in image is {diskimage.get_size()/512}")
print("Size of the block is set to 512")

# 6 This statement invokes the Volume_Info function for the Img_Info object
# to get a Volume_Info object containing the partitions defined in the disk image.
partition_table = pytsk3.Volume_Info(diskimage)

# 14 Determining Partition Layout, Slide 18
partition_table_type = partition_table.info.vstype
if partition_table_type == pytsk3.TSK_VS_TYPE_DOS:
    print ("Partition table is MBR")

elif partition_table_type == pytsk3.TSK_VS_TYPE_GPT:
    print("Partition table is  GPT")
elif partition_table_type == pytsk3.TSK_VS_TYPE_NONE:
    print("No partition table found")
elif partition_table_type == pytsk3.TSK_VS_TYPE_MAC:
    print("Partition table is  MAC")
elif partition_table_type == pytsk3.TSK_VS_TYPE_BSD:
    print("Partition table is  BSD")
else: 
    print("Partition table type is unknown")


#7 Lets Create the table Header
print("Parition number \tDesc\t\tStartSector\t Number of Sectors")
print("-"*89)
#8
partition_count = 1

#9
offsets = []



#10
for partition in partition_table:
    print(f"{partition_count:<20}{partition.desc.decode('ascii'):<24}{partition.start:<17}{partition.len:<16}")
    offsets.append(partition.start)
    partition_count +=1
# Print out the  Total allocated vs total unallocated sectors as per Task 2
print ('-'*89)
TotalUnallocatedSectors =0
for partition in partition_table:
    if partition.desc.decode('ascii') == "Unallocated":
        TotalUnallocatedSectors += partition.len
print (f"Total unallocated sectors = {TotalUnallocatedSectors}")
TotalAllocatedSectors = diskimage.get_size()/512 - TotalUnallocatedSectors
print (f"Total allocated sectors = {TotalAllocatedSectors}")