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
    parser.add_argument('--pico-flash', required=False, 
                            type=int,
                            default=cust_pico.PICO_FLASH_SIZE_BYTES_DEFAULT,
                            help="Size of flash chip on board (bytes) [%(default)s]")
    
    parser.add_argument('--fs-bytes', required=False, 
                            type=int,
                            default=cust_pico.MICROPY_HW_FLASH_STORAGE_BYTES_DEFAULT,
                            help="Size reserved on chip for uPython FS (bytes) [%(default)s]")
    parser.add_argument('--family', default=cust_pico.DefaultFamilyName, 
                        required=False,   
                        help=f"Chip family name [{cust_pico.DefaultFamilyName}]")
    
    return parser.parse_args()

    
def main():
    args = get_args()
    
    lfs = cust_pico.prep_filesystem(args.fs_root, cust_pico.get_blockcount(args))
    tmp = tempfile.NamedTemporaryFile('wb', delete=False)
    cust_pico.write_filesystem(lfs, tmp)
    
    uf2 = UF2File()
    uf2.header.flags = uf2const.Flags.FamilyIDPresent
    uf2.header.family = Family.byName(args.family)
    if uf2.header.family is None:
        print(f"Invalid family '{args.family}'")
        return
    cust_pico.append_fs_to(uf2, tmp.name, cust_pico.get_offset(args))
    uf2.to_file(args.out)
    
if __name__ == '__main__':
    main()
