#!/usr/bin/env python3
import os
import struct
import sys
from typing import Tuple, Optional
import zlib

class PartitionError(Exception):
    """Custom exception for partition-related errors"""
    pass

def get_disk_size(fd) -> int:
    fd.seek(0, 2)
    size = fd.tell()
    fd.seek(0)
    if size < 1024 * 1024:  # Less than 1MB
        raise PartitionError("Disk is too small to be valid")
    return size

def verify_read(fd, size: int, error_msg: str) -> bytes:
    """Read exact number of bytes or raise error"""
    data = fd.read(size)
    if len(data) != size:
        raise PartitionError(f"{error_msg} (expected {size} bytes, got {len(data)})")
    return data

def is_gpt(fd) -> bool:
    """Check if disk uses GPT partitioning"""
    try:
        fd.seek(512)  # LBA1
        sig = verify_read(fd, 8, "Failed to read GPT signature")
        return sig == b'EFI PART'
    except:
        return False

def read_gpt_header(fd) -> dict:
    """Read and validate primary GPT header"""
    # GPT header starts at LBA1 (usually sector 1, offset 512)
    fd.seek(512)
    
    # Read the entire GPT header (512 bytes to be safe)
    header = verify_read(fd, 512, "Failed to read GPT header")
    
    try:
        # Unpack just the fields we need using exact offsets
        signature = header[0:8]
        header_size = struct.unpack_from('<I', header, 12)[0]
        current_lba = struct.unpack_from('<Q', header, 24)[0]
        backup_lba = struct.unpack_from('<Q', header, 32)[0]
        first_usable = struct.unpack_from('<Q', header, 40)[0]
        last_usable = struct.unpack_from('<Q', header, 48)[0]
        part_entry_start_lba = struct.unpack_from('<Q', header, 72)[0]
        num_part_entries = struct.unpack_from('<I', header, 80)[0]
        part_entry_size = struct.unpack_from('<I', header, 84)[0]
    except struct.error as e:
        raise PartitionError(f"Failed to parse GPT header: {e}")

    if signature != b'EFI PART':
        raise PartitionError("Invalid GPT signature")

    # Basic sanity checks
    if header_size < 92 or header_size > 512:
        raise PartitionError(f"Invalid header size: {header_size}")
    if first_usable >= last_usable:
        raise PartitionError("Invalid usable sector range")
    if part_entry_size < 128:
        raise PartitionError("Invalid partition entry size")
    if num_part_entries < 1:
        raise PartitionError("Invalid number of partition entries")

    return {
        'first_usable': first_usable,
        'last_usable': last_usable,
        'part_entry_start_lba': part_entry_start_lba,
        'num_part_entries': num_part_entries,
        'part_entry_size': part_entry_size,
        'backup_lba': backup_lba
    }

def validate_partition_size(start: int, size: int, disk_size: int) -> None:
    """Validate partition parameters are reasonable"""
    if start < 1:
        raise PartitionError("Invalid partition start sector")
    if size < 1:
        raise PartitionError("Invalid partition size")
    if (start + size) * 512 > disk_size:
        raise PartitionError("Partition would exceed disk size")

def verify_partition_update(fd, part_num: int, start: int, size: int, 
                          is_gpt_table: bool, gpt_header: Optional[dict] = None) -> bool:
    """Verify partition was updated correctly"""
    try:
        new_start, new_size = read_gpt_partition(fd, part_num, gpt_header) if is_gpt_table \
                             else read_mbr_partition(fd, part_num)
        
        if new_start != start:
            raise PartitionError("Partition start sector verification failed")
        if new_size != size:
            raise PartitionError("Partition size verification failed")
        return True
    except Exception as e:
        raise PartitionError(f"Partition verification failed: {e}")

def read_gpt_partition(fd, part_num: int, gpt_header: dict) -> Tuple[int, int]:
    """Read start and size of a GPT partition"""
    if not 1 <= part_num <= gpt_header['num_part_entries']:
        raise PartitionError(f"Invalid partition number {part_num}")
        
    entry_offset = (gpt_header['part_entry_start_lba'] * 512) + \
                  ((part_num - 1) * gpt_header['part_entry_size'])
    
    fd.seek(entry_offset)
    entry = verify_read(fd, 128, "Failed to read GPT partition entry")
    
    first_lba, last_lba = struct.unpack_from('<QQ', entry, 32)
    
    if first_lba == 0 and last_lba == 0:
        raise PartitionError("Empty partition entry")
    if first_lba > last_lba:
        raise PartitionError("Invalid partition boundaries")
        
    return first_lba, last_lba - first_lba + 1

def update_gpt_partition(fd, part_num: int, start: int, new_size: int, gpt_header: dict):
    """Update a GPT partition size with validation"""
    # Calculate and validate entry locations
    primary_offset = (gpt_header['part_entry_start_lba'] * 512) + \
                    ((part_num - 1) * gpt_header['part_entry_size'])
    backup_offset = (gpt_header['backup_lba'] * 512) - \
                   (gpt_header['num_part_entries'] * gpt_header['part_entry_size']) + \
                   ((part_num - 1) * gpt_header['part_entry_size'])
    
    if primary_offset >= backup_offset:
        raise PartitionError("Invalid GPT table layout")
    
    # Read and verify current entry
    fd.seek(primary_offset)
    entry = bytearray(verify_read(fd, 128, "Failed to read GPT partition entry"))
    
    # Update last_lba
    last_lba = start + new_size - 1
    if last_lba > gpt_header['last_usable']:
        raise PartitionError("Partition would exceed usable space")
    
    struct.pack_into('<Q', entry, 40, last_lba)
    
    # Write and verify primary table
    fd.seek(primary_offset)
    fd.write(entry)
    fd.flush()
    
    # Verify primary write
    fd.seek(primary_offset)
    verify_entry = verify_read(fd, 128, "Failed to verify primary GPT entry")
    if verify_entry != entry:
        raise PartitionError("Primary GPT entry verification failed")
    
    # Update backup table
    fd.seek(backup_offset)
    fd.write(entry)
    fd.flush()
    
    # Verify backup write
    fd.seek(backup_offset)
    verify_backup = verify_read(fd, 128, "Failed to verify backup GPT entry")
    if verify_backup != entry:
        raise PartitionError("Backup GPT entry verification failed")
    
    # Update CRCs
    update_gpt_crcs(fd, gpt_header)

def update_gpt_crcs(fd, gpt_header: dict):
    """Update CRCs in both GPT headers"""
    # Read partition table
    fd.seek(gpt_header['part_entry_start_lba'] * 512)
    part_table = fd.read(gpt_header['num_part_entries'] * gpt_header['part_entry_size'])
    part_table_crc = zlib.crc32(part_table)
    
    # Update primary header
    fd.seek(512)  # LBA1
    header = bytearray(fd.read(92))
    struct.pack_into('<I', header, 88, part_table_crc)  # Update partition table CRC
    struct.pack_into('<I', header, 16, 0)  # Zero out header CRC
    header_crc = zlib.crc32(header)
    struct.pack_into('<I', header, 16, header_crc)
    
    fd.seek(512)
    fd.write(header)
    
    # Update backup header
    fd.seek(gpt_header['backup_lba'] * 512)
    backup_header = bytearray(header)  # Use same data but update some fields
    struct.pack_into('<Q', backup_header, 24, gpt_header['backup_lba'])  # Current LBA
    struct.pack_into('<Q', backup_header, 32, 1)  # Backup LBA
    struct.pack_into('<I', backup_header, 16, 0)  # Zero CRC
    backup_crc = zlib.crc32(backup_header)
    struct.pack_into('<I', backup_header, 16, backup_crc)
    
    fd.write(backup_header)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /dev/mmcblk0")
        sys.exit(1)
        
    device = sys.argv[1]
    
    if not os.path.exists(device):
        print(f"Error: Device {device} not found")
        sys.exit(1)
    
    try:
        with open(device, 'rb+') as fd:
            disk_size = get_disk_size(fd)
            if disk_size < 512:
                print("Error: Disk too small")
                sys.exit(1)
            
            is_gpt_table = is_gpt(fd)
            print(f"Detected {'GPT' if is_gpt_table else 'MBR'} partition table")
            
            try:
                if is_gpt_table:
                    gpt_header = read_gpt_header(fd)
                    start, current_size = read_gpt_partition(fd, 3, gpt_header)
                    max_sectors = gpt_header['last_usable'] - start + 1
                    
                    if max_sectors <= 0:
                        print("Error: Invalid partition layout")
                        sys.exit(1)
                        
                    update_gpt_partition(fd, 3, start, max_sectors, gpt_header)
                else:
                    # Original MBR code here
                    start, current_size = read_mbr_partition(fd, 3)
                    max_sectors = (disk_size // 512) - start
                    
                    if max_sectors <= 0:
                        print("Error: Invalid partition layout")
                        sys.exit(1)
                        
                    update_mbr_partition(fd, 3, start, max_sectors)
                
                print(f"Successfully expanded partition 3:")
                print(f"  Start sector: {start}")
                print(f"  New size: {max_sectors} sectors ({max_sectors * 512 // 1024 // 1024}MB)")
                
            except (ValueError, IOError) as e:
                print(f"Error processing partition: {e}")
                sys.exit(1)
                
            # Force sync
            fd.flush()
            os.fsync(fd.fileno())
            
    except PermissionError:
        print("Error: Permission denied. Are you running as root?")
        sys.exit(1)
    except IOError as e:
        print(f"I/O Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()