'''
Created on Mar 14, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''



import logging
import argparse

from uf2utils.file import UF2File
from uf2utils.family import Family

logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', 
                        help='UF2 input file')
    
    return parser.parse_args()


def main():
    args = get_args()
    uf2 = UF2File(args.infile, fill_gaps=False)
    
    uf2.sort_blocks()
    # uf2.renumber_blocks()
    
    payload_size = 0
    all_have_family = True
    all_flags = dict()
    all_families = dict()
    for blk in uf2:
        payload_size += blk.header.payload_size
        if blk.header.board_family:
            if blk.header.board_family not in all_families:
                all_families[blk.header.board_family] = Family.byId(blk.header.board_family)
        else:
            all_have_family = False
        
        if blk.header.flags not in all_flags:
            all_flags[blk.header.flags] = 1
        else: 
            all_flags[blk.header.flags] += 1
        
    num_blocks = len(uf2)
    print('\n\nUF2 info')
    print(f"File {args.infile}")
    if num_blocks:
        print(f"\tspanning {hex(uf2[0].header.address)} - {hex(uf2[-1].header.address)} in {num_blocks} blocks")
        print(f'\tTotal payload size: {payload_size} bytes')
        # uf2.generate_blocks_for_gaps()
        num_blocks_after = len(uf2)
        if num_blocks_after != num_blocks:
            print(f'\tCONTAINS GAPS: {num_blocks_after - num_blocks} must be generated to fill')
        else:
            print(f'\tContains NO gaps.')
        if len(all_families):
            if all_have_family:
                print('\tAll blocks have board family value')
            else:
                print('\tSome blocks have NO board family value')
                
            print('\tBoard family set:')
            for id,fam in all_families.items():
                if fam is not None:
                    print(f'\t\t{fam.description}')
                else:
                    print(f'\t\tUnknown board family {hex(id)}')
        else:
            print('\tBoard family NOT SET')
            
        
        print('\tFlags found')
        for k,v in all_flags.items():
            print(f'\t\t{hex(k)}: {v} blocks')
        
    else:
        print('Contains NO BLOCKS')
        
    print('\n\n')
    
if __name__ == '__main__':
    main()
    
    