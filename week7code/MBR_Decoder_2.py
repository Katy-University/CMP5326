# Add the regex library to the program
import re
# Add the struct library to the program
import struct

# 1 open the disk image file
f = open('DiskImage.001', 'rb')

# 2 Read the mbr which is the first 512 bytes
mbr = f.read(512)

# Close the file.
f.close()

# 3 Display the value of the byte at the offset
print(f"Active part of the first partition is {mbr[446]}")

# 8 We are building a regex that is looking at bytes here. So each . represent a single byte.
# mbr_re = b"^.{446}((?P<active_byte>.)(?P<start_chs>.{3})(?P<partition_type>.)(?P<end_chs>.{3})(?P<start_lba>.{4})(?P<num_sectors>.{4})){4}\x55\xAA"
mbr_re = b"^.{446}(?P<active_byte_part1>.)(?P<start_chs_part1>.{3})(?P<partition_type_part1>.)(?P<end_chs_part1>.{3})(?P<start_lba_part1>.{4})(?P<num_sectors_part1>.{4})(?P<active_byte_part2>.)(?P<start_chs_part2>.{3})(?P<partition_type_part2>.)(?P<end_chs_part2>.{3})(?P<start_lba_part2>.{4})(?P<num_sectors_part2>.{4})(?P<active_byte_part3>.)(?P<start_chs_part3>.{3})(?P<partition_type_part3>.)(?P<end_chs_part3>.{3})(?P<start_lba_part3>.{4})(?P<num_sectors_part3>.{4})(?P<active_byte_part4>.)(?P<start_chs_part4>.{3})(?P<partition_type_part4>.)(?P<end_chs_part4>.{3})(?P<start_lba_part4>.{4})(?P<num_sectors_part4>.{4})\x55\xAA"

# 9 Create a regex object for the MBR regular expression.
regex = re.compile(mbr_re, re.DOTALL)

# 10 Match the MBR and store the resulting match object in m
m = regex.match(mbr)

# 11 Process the match provided there is one
if m is not None:
    print("Partition 1")
  # 12 We are taking this from the named regex
    active_byte = m.group('active_byte_part1')

    # 13. Check if active byte is ox80. Note to have to check for character code x80
    if active_byte ==b'\x80':
        print('Partition is active')
    else:
        print('Partition is not active')
#
    #14  Get the partition type byte value
    partition_type_byte = m.group('partition_type_part1')
    # print(partition_type_byte)
#
    # 15 Check partition type byte value against a number of values as there are different partitions.
    if partition_type_byte == b'\x06':
        print("Partition is DOS 3.31 FAT (>32MB)")
    elif partition_type_byte == b'\x07':
        print("Partition is NTFS/OS2 HPFS/exFAT")
    elif partition_type_byte == b'\x0B':
        print("Partition is Win95 OSR2 FAT32")
    elif partition_type_byte == b'\x05':
        print("Partition is extended partition")
    else:
        print("Partition Type is not recognised)")

# 16 Get the start LBA value from the matched group
start_lba_bytes = m.group("start_lba_part1")

# 17 Convert the bytes obtained above into a single integer value
start_lba = struct.unpack('<I', start_lba_bytes)

# 18 Display the start LBA
print(f"The start LBA of the partition is {start_lba[0]}")

# 19 code to get the number of sectors character bytes from the named group called num_sectors_part1 and store
# them in a variable called num_sectors_bytes
num_sectors_bytes = m.group("num_sectors_part1")

# 20 code to convert the bytes stored in num_sector_bytes into a little endian 32 bit integer,
# unsigned using the struct.unpack function.  Store the converted value in a variable called num_sectors.
num_sectors = struct.unpack('<I', num_sectors_bytes)[0]

# 21 code to display the converted value from the variable num_sectors.  The program should output something like
# f“The number of sectors in the partition is {num_sectors}"
print(f"The number of sectors in the partition is {num_sectors}")

'''
Solution to getting info from the rest of the partitions(It would make more sense to group all of this with the
previous, but I did not so the code is simpler to follow:) The below also is horrible coding practice,
you should definately use a loop or a function. The reason for this is to build muscle memory.

And hopefully it is so painful that it makes you want to do proper coding :)
'''
