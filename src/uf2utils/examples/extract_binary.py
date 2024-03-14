'''
Created on Mar 14, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

import logging
import argparse

from uf2utils.file import UF2File

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fill_gaps', required=False, default=False, 
                        action='store_true',
                        help='pad any gaps in offsets with 0 bytes')
    parser.add_argument('--out', required=True,
                                help='output file for contents')
    
    parser.add_argument('--offset_start', required=False, 
                                default='0',
                                type=str,
                                help='restrict output to blocks starting at this offset')
    parser.add_argument('--offset_end', required=False, 
                                default=None,
                                help='restrict output to blocks below this offset')
    
    parser.add_argument('infile', 
                        help='UF2 input file')
    
    return parser.parse_args()

def get_offset_value(vs:str):
    v = 0
    try:
        v = int(vs)
    except ValueError:
        v = int(vs, 16)
    
    return v

def main():
    args = get_args()
    
    log.info(f'Loading {args.infile}')
    uf2 = UF2File(args.infile)
    uf2.sort_blocks() # force the payloads to be sorted
    
    if args.fill_gaps:
        # fill in any gaps
        uf2.generate_blocks_for_gaps()
        
    off_start = get_offset_value(args.offset_start)
    off_end = None 
    if args.offset_end is not None:
        off_end = get_offset_value(args.offset_end)
        
    # get the bytes
    bts = uf2.extract_payload(off_start, off_end)
    log.info(f'Extracted {len(bts)} bytes of payload')
    with open(args.out, 'wb') as outfile:
        outfile.write(bts)
        
    log.info(f'Wrote payload to {args.out}')
        
    
if __name__ == '__main__':
    main()
    

    