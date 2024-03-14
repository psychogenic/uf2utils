'''
Created on Mar 14, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com

python uf2utils/examples/custom_pico.py \
    --fs_root /tmp/ttupython \
    --upython /tmp/RPI_PICO-20240222-v1.22.2.uf2 \
    --out /tmp/RPI_PICO-CUSTOM.uf2
    
'''
import logging
import argparse
import tempfile

import uf2utils.constants as uf2const
from uf2utils.family import Family
from uf2utils.file import UF2File
import uf2utils.examples.custom_pico as cust_pico

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--fs_root', help='directory to use as root of filesystem', required=True)
    parser.add_argument('--out', help='output UF2 file with fs to create', required=True)
    parser.add_argument('--fs_offset', default=hex(cust_pico.DefaultFSBaseAddress), 
                        required=False,   
                        help="base offset in UF2 for filesystem")
    
    return parser.parse_args()

    

def get_offset(args):
    v = 0
    try:
        v = int(args.fs_offset)
    except ValueError:
        v = int(args.fs_offset, 16)
    
    return v
    
def main():
    args = get_args()
    
    lfs = cust_pico.prep_filesystem(args.fs_root)
    tmp = tempfile.NamedTemporaryFile('wb', delete=False)
    cust_pico.write_filesystem(lfs, tmp)
    
    uf2 = UF2File()
    uf2.header.flags = uf2const.Flags.FamilyIDPresent
    uf2.header.family = Family.byName('RP2040')
    cust_pico.append_fs_to(uf2, tmp.name, get_offset(args))
    uf2.to_file(args.out)
    
if __name__ == '__main__':
    main()
