#First application: Create a partition table decoder helper
#Find the start LBA stored in 4 bytes at offset 8 of the partition entry
#Calculate the offset to the partition in bytes (start LBA * 512)

#inputs 
start_lba = int(input("Enter the start LBA for the partition: "))
number_of_sectors_in_partition = int(input("Please input number of sectors value for the partition: "))
active_byte = int(input("Please input active byte (0x80 for active, 0x00 for inactive): "), 16)
partition_type = input("Please input partition type byte (e.g., 07 for NTFS): ")

#lba to byte offset calculation
offset_to_partition_in_bytes = start_lba * 512
print(f"The offset to the partition in bytes is: {offset_to_partition_in_bytes}")

#Find the number of sectors in the partition
#After the start lba at offset 12 of partition entry
#Output size of partition in bytes, kibibytes, mibibytes and gibibytes
size_of_partition_in_bytes = number_of_sectors_in_partition * 51

print(f"The size of the partition in bytes is: {size_of_partition_in_bytes}")
print(f"The size of the partition in kibibytes is: {size_of_partition_in_bytes / 1024}")
print(f"The size of the partition in mibibytes is: {size_of_partition_in_bytes / 1024**2}")
print(f"The size of the partition in gibibytes is: {size_of_partition_in_bytes / 1024**3}")

#active byte (Offset 0 of the partition entry)
if active_byte == 0x80:
    print("Partition is bootable")
else:
    print("Partition is not bootable")

#partition type (Offset 4 of the partition entry)
if partition_type == "05": 
    print("The partition is DOS 3.3+ Extended Partition ")
elif partition_type == "06":
    print("The partition is DOS 3.31+ 16-bit FAT (over 32M) ")
elif partition_type == "07":
    print("The partition is Windows NT NTFS ")
elif partition_type == "08":
    print("The partition is exFAT ")
elif partition_type == "0B":
    print("The partition is WIN95 OSR2 FAT32 ")
else:
    print("Unknown partition id value")