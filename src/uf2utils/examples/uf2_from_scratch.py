'''
Created on Mar 14, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
from uf2utils.file import UF2File
from uf2utils.family import Family

def get_payload_contents():
    
    # return whatever you want in here
    bts = bytearray()
    with open('/dev/random', 'rb') as infile:
        while len(bts) < 1000:
            bts += infile.read(100)
    
    return bts

def get_new_uf2(for_board:Family):
    uf2 = UF2File(board_family=for_board.id, fill_gaps=False)
    # uf2.header.flags is already Flags.FamilyIDPresent
    # you may want to add more, but if you do, probably good 
    # to preserve the FamilyIDPresent bit
    
    return uf2


def main():
    uf2 = get_new_uf2(Family.byName('ESP32H2'))
    
    
    payload_bytes = get_payload_contents()
    
    uf2.append_payload(payload_bytes, 
                       start_offset=0x1000000, 
                       block_payload_size=256)
    
    uf2.to_file('/tmp/mystuff.uf2')
    