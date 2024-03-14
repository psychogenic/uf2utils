'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com

python uf2utils/examples/custom_pico.py \
    --fs_root /tmp/ttupython \
    --upython /tmp/RPI_PICO-20240222-v1.22.2.uf2 \
    --out /tmp/RPI_PICO-CUSTOM.uf2
    

RP2040 particularities (maybe more generalized?)

The FamilyIDPresent flag must be set and, in order to function 

   * blocks have a payload of 256 bytes, so each block writes a page
   * any filesystem included needs to have a valid number of blocks of 4096 bytes (352 works well)
   * the entire uf2 file can't have any gaps in the addresses (though UF2 would support it,
   the bootloader gets rather unhappy)
   * the mem mapping of the blocks has flash 0 address at 0x10000000
   * filesystem address offset is 0xa0000, so in UF2 starts at 0x100a0000
   
    
'''
import logging
import argparse
import os
import tempfile

from littlefs import LittleFS
from uf2utils.file import UF2File

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# the 0xa0000 is the spot in flash where 
# the fs actually resides.  The 0x10000000
# is the memory map to the flash base 
# within the pico bootloader
DefaultFSBaseAddress = 0x10000000 + 0xa0000

PicoUpythonFSBlocksize = 4096
PicoUpythonFSBlockCount = 352 # this MUST be 352, nooooo, don't think of changing it noooooo
PicoUpythonFSProgSize = 256

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--fs_root', required=True,
                        help='directory to use as root of filesystem')
    parser.add_argument('--upython', required=True,
                        help='MicroPython UF2 to use as base OS')
    parser.add_argument('--out', required=True,
                                help='output UF2 file with fs to create')
    parser.add_argument('--fs_offset', default=hex(DefaultFSBaseAddress), 
                        required=False,   
                        help="base offset in UF2 for filesystem")
    
    return parser.parse_args()

    

def prep_filesystem(files_from_dir:str, to_base_dir:str='/'):
    lfs = LittleFS(block_size=PicoUpythonFSBlocksize, 
                   block_count=PicoUpythonFSBlockCount, 
                   prog_size=PicoUpythonFSProgSize)
    for root, dir_names, file_names in os.walk(files_from_dir):
        lfs_base = root.replace(f'{files_from_dir}', to_base_dir).replace('//', '/')
        for new_dir in dir_names:
            ndir = os.path.join(lfs_base, new_dir).replace('//', '/')
            log.info(f'mkdir {ndir}')
            lfs.mkdir(ndir)
            
        log.info('Copying files...')
        for f in file_names:
            dest = os.path.join(lfs_base, f).replace('//', '/')
            log.debug(f'cp {os.path.join(root,f)} {lfs_base}')
            with open(os.path.join(root,f), 'rb') as src_file:
                with lfs.open(dest, 'wb') as lfs_file:
                    lfs_file.write(src_file.read())
        
    
    return lfs


def write_filesystem(lfs:LittleFS, tmp_file:str):
    log.info(f'Writing LFS filesystem to {tmp_file.name}')
    tmp_file.write(lfs.context.buffer)
    tmp_file.close()


def append_fs_to(uf2:UF2File, path_to_image:str, start_offset):
    log.info(f'Injecting fs from {path_to_image} @ {hex(start_offset)}')
    with open(path_to_image, 'rb') as img:
        uf2.append_payload(img.read(), start_offset) 
    

    
def get_offset(args):
    v = 0
    try:
        v = int(args.fs_offset)
    except ValueError:
        v = int(args.fs_offset, 16)
    
    return v
    
def main():
    args = get_args()
    
    print
    lfs = prep_filesystem(args.fs_root)
    tmp = tempfile.NamedTemporaryFile('wb', delete=False)
    write_filesystem(lfs, tmp)
    
    log.info(f'Loading {args.upython}')
    uf2 = UF2File(args.upython, fill_gaps=True)
    append_fs_to(uf2, tmp.name, get_offset(args))
    uf2.to_file(args.out)
    
    print(f'Resulting UF2 file: {args.out}')
    
if __name__ == '__main__':
    main()
