'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
import struct
from uf2utils.constants import MaxPayloadSize, BlockSize, Magic
from uf2utils.header import Header 


class DataBlock:
    '''
        A UF2 data block, including header and payload.
        May be constructed from raw data (fromBlock classmethod)
        or instantiated manually from payload and header
    '''
    @classmethod 
    def fromBlock(cls, data: bytes):
        hdr = Header.fromBlock(data) 
        payload = data[32:32 + hdr.payload_size]
        return cls(payload, hdr)
    
    def __init__(self, payload:bytearray, header:Header=None, magic_start1:int=None, magic_end:int=None):
        self.payload = payload 
        self.header = header 
        self.magic_start1 = magic_start1 
        self.magic_end = magic_end
        
        
    @property 
    def as_bytes(self):
        '''
            Return the block as raw bytes, with all magiks handled.
            Assumes the block number and totals are valid (which requires
            global knowledge of things, thus a higher level up).
        '''
        target = bytearray(BlockSize)
        magic_start1 = self.magic_start1 if self.magic_start1 is not None else Magic.START1
        magic_end = self.magic_end if self.magic_end is not None else Magic.END
        struct.pack_into('<IIIIIIII', target, 0, 
                         Magic.START0, magic_start1, 
                         self.header.flags, 
                         self.header.address, 
                         len(self.payload), 
                         self.header.block_number, 
                         self.header.total_blocks, 
                         self.header.board_family)
        target[32: 32+len(self.payload)] = self.payload
        struct.pack_into('<I', target, BlockSize - 4, magic_end)
        return target
    
    
    def __repr__(self):
        return f'<DataBlock {self.header.block_number + 1}/{self.header.total_blocks} ({self.header.payload_size} bytes @ {hex(self.header.address)})'