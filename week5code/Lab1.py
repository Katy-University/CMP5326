"""Partition entry parser

This script accepts a single 16-byte MBR partition entry as a hex string
and parses the fields (boot flag, CHS start/end, type, start LBA, number
of sectors). It then computes byte offsets and sizes (512 bytes/sector).

Example 16-byte entry (hex, spaces optional):
  80 00 02 00 07 00 00 00 3F 00 00 00 00 08 00 00
or
  80000200070000003F00000000080000

Usage: run the script and paste the 16-byte hex when prompted.
"""

import sys

SECTOR_SIZE = 512

PARTITION_TYPE_MAP = {
    0x00: 'Unused',
    0x01: 'FAT12',
    0x04: 'FAT16 <32M',
    0x05: 'Extended (CHS)',
    0x06: 'FAT16',
    0x07: 'NTFS/exFAT',
    0x0B: 'FAT32 (CHS)',
    0x0C: 'FAT32 (LBA)',
    0x0E: 'FAT16 (LBA)',
    0x82: 'Linux swap',
    0x83: 'Linux filesystem',
    0x8E: 'Linux LVM',
    0xAF: 'HFS / HFS+',
    0xEE: 'GPT protective',
}


def parse_partition_entry(entry_bytes: bytes) -> dict:
    """Parse a 16-byte MBR partition entry and return fields as dict.

    entry_bytes must be exactly 16 bytes.
    Offsets (within entry):
      0: boot flag (1 byte)
      1-3: CHS start (3 bytes)
      4: partition type (1 byte)
      5-7: CHS end (3 bytes)
      8-11: start LBA (4 bytes, little-endian)
      12-15: number of sectors (4 bytes, little-endian)
    """
    if len(entry_bytes) != 16:
        raise ValueError('Partition entry must be 16 bytes')

    boot_flag = entry_bytes[0]
    chs_start = entry_bytes[1:4]
    part_type = entry_bytes[4]
    chs_end = entry_bytes[5:8]
    start_lba = int.from_bytes(entry_bytes[8:12], 'little')
    num_sectors = int.from_bytes(entry_bytes[12:16], 'little')

    return {
        'boot_flag': boot_flag,
        'chs_start': chs_start,
        'partition_type': part_type,
        'chs_end': chs_end,
        'start_lba': start_lba,
        'num_sectors': num_sectors,
    }


def human_readable_size(bytes_size: int) -> str:
    """Return a human readable size using binary prefixes (KiB, MiB...)."""
    for unit in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:
        if bytes_size < 1024 or unit == 'TiB':
            return f"{bytes_size:.2f} {unit}" if unit != 'bytes' else f"{bytes_size} {unit}"
        bytes_size /= 1024


def clean_hex_input(s: str) -> str:
    """Remove common separators and prefixes from a hex string."""
    s = s.strip()
    # remove 0x prefixes, spaces, and common separators
    s = s.replace('0x', '').replace('0X', '')
    s = s.replace(' ', '').replace('-', '').replace(':', '')
    return s


def main():
    print('Choose input mode:')
    print('  1) Paste a single 16-byte partition entry (hex)')
    print('  2) Parse 4 partition entries from an MBR in a disk image file')
    choice = input('Select mode (1 or 2) [1]: ').strip() or '1'

    if choice == '1':
        user = input('Enter 16-byte partition entry as hex (or press Enter to see an example): ').strip()
        if not user:
            print('Example: 80 00 02 00 07 00 00 00 3F 00 00 00 00 08 00 00')
            user = input('Paste the 16-byte hex now: ').strip()

        hexstr = clean_hex_input(user)
        if len(hexstr) != 32:
            print(f'Invalid input: expected 32 hex characters (16 bytes), got {len(hexstr)}')
            sys.exit(1)

        try:
            entry = bytes.fromhex(hexstr)
        except ValueError:
            print('Invalid hex input')
            sys.exit(1)

        parsed = parse_partition_entry(entry)
        partitions = [parsed]

    else:
        img_path = input('Enter disk image filename (MBR will be read from offset 0): ').strip()
        try:
            partitions = parse_mbr(img_path)
        except Exception as e:
            print('Error reading MBR:', e)
            sys.exit(1)

    # Print results for each partition
    for idx, parsed in enumerate(partitions, start=1):
        start_lba = parsed['start_lba']
        num_sectors = parsed['num_sectors']
        offset_bytes = start_lba * SECTOR_SIZE
        size_bytes = num_sectors * SECTOR_SIZE

        print(f"\nPartition {idx}:")
        print(f"  Boot flag: 0x{parsed['boot_flag']:02X} ({'bootable' if parsed['boot_flag'] == 0x80 else 'not bootable'})")
        print(f"  Partition type: 0x{parsed['partition_type']:02X} - {PARTITION_TYPE_MAP.get(parsed['partition_type'], 'Unknown')}")
        print(f"  CHS start: {parsed['chs_start'].hex()}  CHS end: {parsed['chs_end'].hex()}")
        print(f"  Start LBA: {start_lba} (byte offset: {offset_bytes})")
        print(f"  Number of sectors: {num_sectors}")
        print(f"  Size: {size_bytes} bytes ({human_readable_size(size_bytes)})")


def parse_mbr(image_path: str) -> list:
    """Read the MBR from image_path and return a list of up to 4 parsed partition entries."""
    with open(image_path, 'rb') as f:
        f.seek(446)  # partition table starts at offset 446
        table = f.read(16 * 4)
        if len(table) < 16 * 4:
            raise ValueError('File too small to contain a full MBR partition table')

    partitions = []
    for i in range(4):
        entry = table[i*16:(i+1)*16]
        parsed = parse_partition_entry(entry)
        partitions.append(parsed)
    return partitions


if __name__ == '__main__':
    main()