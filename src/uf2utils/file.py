'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
import os
from uf2utils.constants import BlockSize, DefaultBlockPayloadSize, Flags, Magic
from uf2utils.header import Header, UF2EncodeError, UF2DecodeError
from uf2utils.block import DataBlock
from uf2utils.family import Family


import logging 
log = logging.getLogger(__name__)



class UF2File:
    '''
        Main handle to UF2 functionality.
        
        If you pass it's constructor the path to a UF2 file, it will read it in during init.
        
        Once a UF2 file has been parsed and/or after appending payload contents, the blocks
        are accessible by treating the UF2File object as an array
        
        uf2 = UF2File('/tmp/whatever.uf2')
        for block in uf2:
            print(block.header.address)
            print(block.payload)
        
        or
        
        print(uf2[-1].header.family)
        
        
        
        
        
        Writing a new file 
        
        uf2 = UF2File()
        uf2.header.flags = uf2const.Flags.FamilyIDPresent
        uf2.header.family = Family.byName('RP2040')
        # get some_bytearray somewhere
        uf2.append_payload(some_bytearray, start_offset) 
        # you can add more bytes, offsets don't need to start at 0
        # or cover the entire span (you can hop around)
        
        
        uf2.to_file(args.out)
    
    '''
    
    @classmethod 
    def setMagic(cls, start:int, end:int):
        cls.setMarkerStart(start)
        cls.setMarkerEnd(end)
        
    @classmethod
    def setMarkerStart(cls, start:int):
        Magic.START1 = start 
        
    @classmethod 
    def setMarkerEnd(cls, end:int):
        Magic.END = end
        
    
    @classmethod 
    def readBlocks(cls, filepath:str):
        blocks = []
        if not os.path.exists(filepath):
            raise UF2DecodeError(f'Cannot find {filepath}')
        if not os.path.isfile(filepath):
            raise UF2DecodeError(f'{filepath} not a file')
            
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BlockSize)
                if data is not None and len(data):
                    blocks.append(DataBlock.fromBlock(data))
                else:
                    break

        return blocks
    
    def __init__(self, fpath:str='', board_family:int=None, 
                 fill_gaps:bool=False,
                 magic_start:int=None, 
                 magic_end:int = None):
        '''
            UF2File constructor
            @param fpath: path to file (will read in automatically, if passed)
            @param board_family: default board family id (will use from file, if read)
            @param fill_gaps: boolean, if true will ensure no gaps present on write
             
        
        '''
        if board_family is None:
            # set some sane default
            board_family = Family.byName('RP2040').id
            
        self.magic_start1 = magic_start 
        self.magic_end = magic_end
        
        self._setupMagic()
        # the uf2file header is a prototype for cases where we
        # are writing from scratch (i.e. no example to copy from 
        # a parsed in file)
        self._header = Header(Flags.FamilyIDPresent, 0, 0, 0, 0, board_family)
        self._blocks = []
        self._payload = None
        self._dirty = False
        self._fpath = fpath
        self.cleanup_resort = False
        self.overwrite_prototype_header_on_read = True
        self.fill_gaps = fill_gaps
        
        
        if len(fpath):
            self.from_file(fpath)
        
    def append_datablock(self, dblock:DataBlock):
        '''
            Append a valid data block object to the list of blocks
        '''
        if dblock.header is None:
            UF2EncodeError('Can only append datablocks with a header')
        self._blocks.append(dblock)
        self._dirty = True 
        
    def append_payload(self, payload_bytes:bytes, start_offset:int, 
                       block_payload_size:int=DefaultBlockPayloadSize):
        '''
            Append arbitrary binary payload, creating blocks and setting 
            offsets as required.
            
            @param payload_bytes: actual contents to append
            @param start_offset: offset start point for this content
            @param block_payload_size: if payload_bytes len > block size, will
            be split into multiple blocks
        '''
        pcount = 0
        cur_offset = start_offset
        while pcount < len(payload_bytes):
            end_count = pcount + block_payload_size
            
            if end_count > len(payload_bytes):
                end_count = len(payload_bytes)
                
            
            bts = payload_bytes[pcount:end_count]
            
            hdr = Header.deep_copy(self.header)
            hdr.block_number = self.num_blocks
            hdr.payload_size = len(bts)
            hdr.address = cur_offset
            cur_offset += hdr.payload_size
            self.append_datablock(DataBlock(bts, hdr,
                                                magic_start1=self.magic_start1,
                                                magic_end=self.magic_end))
            
            pcount = end_count
            
        
    @property 
    def header(self) -> Header:
        '''
            The prototype header for new blocks.
            Mostly useful when creating UF2 from scratch.
            
            Unless overwrite_prototype_header_on_read is False,
            this prototype will be configured according to first block
            read when calling from_file() (or constructing with a filepath
            argument). 
        '''
        return self._header
    
    @property 
    def num_blocks(self):
        return len(self._blocks)
    
    
    @property 
    def flags(self):
        return self.header.flags 
    
    @flags.setter 
    def flags(self, set_to:int):
        self.header.flags = set_to 
        
        
    @property 
    def family(self):
        return self.header.family
    
    @family.setter 
    def family(self, set_to:int):
        self.header.family = set_to 
    
    @property 
    def start_address(self):
        return self.header.address
    
    @start_address.setter 
    def start_address(self, set_to:int):
        self.header.address = set_to 
        
        
    def from_file(self, file_path:str):
        '''
            Replace any contents of current file object with
            data from file_path.
        
        '''
        self._setupMagic()
        blks = self.readBlocks(file_path)
        if self.overwrite_prototype_header_on_read:
            self.header.address = blks[0].header.address 
            self.header.flags = blks[0].header.flags 
            self.header.board_family = blks[0].header.board_family 
            
        self.header.total_blocks = len(blks)
        
        self._blocks = blks
        
        self._fpath = file_path
        
    def renumber_blocks(self):
        '''
            Blocks have both a number and a total, which 
            must be correct for things to work out.
            This method renumbers everything.
        '''
        num_total = self.num_blocks
        for i in range(0, num_total):
            self._blocks[i].header.block_number = i
            self._blocks[i].header.total_blocks = num_total 
    
    def generate_blocks_for_gaps(self):
        '''
            Since each block has it's own offset, it is possible
            to have gaps between block addresses.
            This method fills those gaps with empty blocks.
            The RP2040 gets pretty unhappy when you add in the 
            filesystem 0xa0000 away from the start.
            This is sad, because that's probably the one and only
            beautiful thing about the UF2 format -- being able to 
            hop around and not deal with big files full of empty.
            Ah well.
            
            @note: just be sure the blocks are in order before calling this.
            
            @see: sort_blocks()
        '''
        all_blocks = []
        for i in range(0, len(self) - 1):
            cur_block = self[i]
            next_block = self[i+1]
            
            all_blocks.append(cur_block)
            if (cur_block.header.address + cur_block.header.payload_size) < next_block.header.address:
                log.info(f'Empty space found between {cur_block}  and {next_block}, fill_gaps enabled')
                log.info(f'{next_block.header.address - cur_block.header.address} bytes to pad in {cur_block.header.payload_size} byte chunks')
            while (cur_block.header.address + cur_block.header.payload_size) < next_block.header.address:
                hdr = Header.deep_copy(cur_block.header)
                hdr.address = cur_block.header.address + cur_block.header.payload_size
                hdr.block_number = cur_block.header.block_number + 1
                log.debug(hdr)
                empty_payload = bytearray(cur_block.header.payload_size)
                cur_block = DataBlock(empty_payload, hdr)
                all_blocks.append(cur_block)
                #print(len(all_blocks), end='')
                
        if (len(self) > 1):
            all_blocks.append(self[-1]) # last block
        
        self._blocks = all_blocks
        
    def sort_blocks(self):
        '''
            Does what it says on the box.  Blocks will be sorted according to their (header) address 
        '''
        sorted_blocks = sorted(self._blocks, key=lambda b: b.header.address)
        self._blocks = sorted_blocks 
        
    def _setupMagic(self):
        if self.magic_start1 is not None:
            self.setMarkerStart(self.magic_start1)
        if self.magic_end is not None:
            self.setMarkerEnd(self.magic_end)
            
    def _cleanup(self):
        if self.fill_gaps or self.cleanup_resort:
            self.sort_blocks()
            
        self.renumber_blocks()

        if self.fill_gaps:
            self.generate_blocks_for_gaps()
            self.renumber_blocks()
            
    def to_file(self, file_path:str):
        '''
            Generate a valid UF2 file based on current set of blocks.
            
            This may lead to renumbering of blocks and setting 
            total as required.
        '''
        self._fpath = file_path
        if self._dirty:
            self._cleanup()
            self._dirty = False
            
        with open(file_path, 'wb') as f:
            for blk in self._blocks:
                f.write(blk.as_bytes)
            f.close()
            
        
    def extract_payload(self, offset_start:int=0, offset_end:int=None):
        '''
            Get a hold of the payload bytes, without all the magic and 
            the headers.
            @param offset_start: optionally start higher up than beginning address
            @param offset_end: optionally cap return to values < than this
            
            @return: a bytearray of the payload
        '''
        sorted_blocks = sorted(self._blocks, key=lambda b: b.header.address)
        included_blocks = []
        for blk in sorted_blocks:
            if blk.header.address < offset_start:
                continue 
            
            if offset_end is not None and blk.header.address >= offset_end:
                continue 
            
            included_blocks.append(blk)
            
        bts = bytearray()
        for blk in included_blocks:
            bts += blk.payload
        return bts
        
    @property 
    def payload(self):
        '''
        This is just a fat data blob, in the order of the address--i.e. does NOT
        account for address offsets (which may insert "spacing"
        between the bytes, unless you've generated blocks for the gaps).
        
        To actually extract payload in a sane manner, use extract_payload with 
        explicit parameters.
        '''
        if self._payload is not None:
            return self._payload 
        
        if self._blocks is None:
            return None 

        self._payload = self.extract_payload(0)
        return self._payload
    
    def __len__(self):
        return self.num_blocks
    
    def __getitem__(self, k:int) -> DataBlock:
        try:
            idx = int(k)
        except ValueError:
            raise Exception('Only accessible by [INT] index')
        
        if idx >= self.num_blocks:
            raise IndexError(f'Only have {self.num_blocks} blocks available')
        
        return self._blocks[idx]
    
    def __repr__(self):
        return f'<UF2File {self._fpath} {self.num_blocks} blocks>'
        