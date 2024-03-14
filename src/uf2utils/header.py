'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com

 UF2 file consists of 512 byte blocks. Each block starts with a 32 byte header, followed by data, and a final magic number. All fields, except for data, are 32 bit unsigned little endian integers.

Offset    Size    Value
0         4    First magic number, 0x0A324655 ("UF2\n")
4         4    Second magic number, 0x9E5D5157
8         4    Flags
12        4    Address in flash where the data should be written
16        4    Number of bytes used in data (often 256)
20        4    Sequential block number; starts at 0
24        4    Total number of blocks in file
28        4    File size or board family ID or zero
32        476  Data, padded with zeros
508       4    Final magic number, 0x0AB16F30

'''
import struct 
from uf2utils.constants import Magic, BlockSize
from uf2utils.family import Family

class UF2DecodeError(Exception):
    pass

class UF2EncodeError(Exception):
    pass


class Header:
    
    @classmethod 
    def fromBlock(cls, data: bytes):
        '''
            Construct and return a UF2 header from raw data bytes
        '''
        if len(data) != BlockSize:
            raise UF2DecodeError(f"Invalid UF2 block size. Block size must be exactly {BlockSize} bytes.")
        
        if struct.unpack_from("<I", data, 0)[0] != Magic.START0:
            UF2DecodeError(f"Invalid START0 magic value: expected 0x{Magic.START0:08x}")
        
        if struct.unpack_from("<I", data, 4)[0] != Magic.START1:
            UF2DecodeError(f"Invalid START1 magic value: expected 0x{Magic.START1:08x}")
        
        return cls(*struct.unpack_from("<IIIIII", data, 8))
    
    @classmethod 
    def deep_copy(cls, other):
        return cls(other.flags, other.address, other.payload_size, other.block_number, other.total_blocks, other.board_family)
    
    def __init__(self, flags:int, flash_address:int, payload_size:int, block_number:int, total_blocks:int, board_family:int):
        self.flags = flags 
        self.address = flash_address
        self.payload_size = payload_size
        self.block_number = block_number
        self.total_blocks = total_blocks 
        self.board_family = board_family
        
    @property 
    def family(self) -> Family:
        return Family.byId(self.board_family)
    
    @family.setter 
    def family(self, set_to:Family):
        self.board_family = set_to.id
        
    def __repr__(self):
        return f'<Header #{self.block_number} @ {hex(self.address)}>'
        
        