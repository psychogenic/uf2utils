# uf2utils

Python UF2 file utils in a decent framework

Copyright &copy; 2024 Pat Deegan [psychogenic.com](https://psychogenic.com)


What is this insanity?  Yes, the [UF2 file format](https://github.com/microsoft/uf2) is not complex and it's a small matter to parse the thing, but *why* could I not find a library to do this intelligently?  

Anyway, here's something for this odd, filled with magic but no checksum, format.


This library allows you to:

   * read in existing UF2 files and inspect the headers and payload, as well as extract all or potions of the contents;
   
   * augment existing UF2 files, used here to include a default filesystem for the RP2040/Pi Pico type boards; and 
   
   * prepare your own UF2 files with whatever you want within, from scratch
   
and includes a sample script to dump info from a UF2 file, producing output like

```
$ python uf2utils/examples/uf2_info.py /tmp/RPI_PICO-custom.uf2
UF2 info
File /tmp/RPI_PICO-custom.uf2
        spanning 0x10000000 - 0x101fff00 in 8192 blocks
        Total payload size: 2097152 bytes
        Contains NO gaps.
        All blocks have board family value
        Board family set:
                Raspberry Pi RP2040
        Flags found
                0x2000: 8192 blocks

$ python uf2utils/examples/uf2_info.py /tmp/arcade.uf2
UF2 info
File /tmp/arcade.uf2
        spanning 0x0 - 0x807dd00 in 5270 blocks
        Total payload size: 1349120 bytes
        CONTAINS GAPS: 522726 must be generated to fill
        All blocks have board family value
        Board family set:
                Unknown board family 0x7193c
                Microchip (Atmel) SAMD51
                ST STM32F4xx
        Flags found
                0x1000: 1818 blocks
                0x2000: 3452 blocks



```
   

# Examples


You want to add files to the standard raspberry pi [MicroPython Pi Pico UF2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) file and create a customized mini distro?

Or how about leaving the uPython OS as is and just replacing the contents of entire filesystem with a drag and drop onto the bootloader?

Easy peasy.  To base an entire distro, and recursively include all the contents of `/tmp/mypython` at the root of the filesystem, you can run:

```
python uf2utils/examples/custom_pico.py \
       --fs_root /tmp/mypython \ 
       --upython /tmp/RPI_PICO-20240222-v1.22.2.uf2 \
       --out /tmp/rpi-custom.uf2
```

If you want a smaller file that you can use to update only the contents of the LittleFS filesystem with, you can instead do 

```
python uf2utils/examples/pico_fs_update.py \
     --fs_root /tmp/ttupython \
     --out /tmp/meFS.uf2
```

Either way, hold the boot button, plug in the RP2040 device and drag the resulting `--out` file to the virtual drive.  After update, the system should reboot and have your new contents.


The `uf2utils.examples` also contains a sample of extracting payloads from  UF2 files.




## Extra info about Pico/RP2040 MicroPython UF2

In addition to figuring out how to deal with the massively redundant UF2 files, some stumbling around was needed to actually get a conjoined OS + filesystem UF2 for some custom RP2040-based boards.

I include some notes and discoveries here, made through research, debugging with Uri and a lot of trial and error, in the hopes that you won't need to fumble around as much.  This all applies to the Pico/RP2040 bootloader, uncertain how general these truths may be but none of them should hurt any platform.

The block number and block total matter.  The UF2File objects have a `renumber_blocks()` that handle this simple matter, and it will be called automatically if you "dirty" the file by using `append_payload()`.

The RP2040 MicroPython filesystem is [LittleFS](https://github.com/littlefs-project/littlefs) and its a nice simple fs, with a pretty [nifty viewer online](https://tniessen.github.io/littlefs-disk-img-viewer/).  When you create it, the blocksize must be 4096 and I *think* the OS is unhappy if you have a value other that 352 blocks in there.  The [default MicroPython _boot.py](https://github.com/micropython/micropython/blob/master/ports/rp2/modules/_boot.py) will just wipe anything it's unhappy with.

With RP2040 uPython, the FS is on the flash at 0xA0000 -- and this is a value, *__vfs_start* or something, that is really painful to try and discover, or at least it was for me.  When creating the UF2 file, this offset must become relative to  `FLASH(rx) : ORIGIN = 0x10000000`, so *0x100a0000*.

The UF2 "blocksize"--each block in UF2 is fixed at 512 bytes, here I mean the size of each block's payload--needs to be 256, such that each block received by the bootloader writes a page to the flash.  So, your payload winds up in a 2x bloated file, where almost half the payload bytes are forced to be zeros and then there are the no less than 12 bytes of "magic".  So, a fat file.

The UF2 format actually is rather nice in that each block is independent and we could, in theory, skip over zones we don't care about.  But then the RP2040 bootloader really doesn't like that.  The last datablock in the current RPI_PICO-20240222-v1.22.2.uf2 is at offset 0x1004f500, and I'm adding the FS down at 0x100a0000.  Turns out, you really must pad everything to fill the gap with empty datablocks, otherwise the bootloader gets sad and you don't get your files.

For this specific case, the `UF2File` class constructor has a `fill_gaps` boolean, or you can just manually use `generate_blocks_for_gaps()` (assuming the blocks are sorted).  Files gets bigger but now we can update OS and FS in one go, great for factory.

Another option, for size or just later updates of FS, is to generate only the filesystem.  That works fine.  The start offset is 0x100a0000 and there are no gaps, and everyone is happy.  See the `pico_fs_update` module in examples for that.


## License

This library is release under the LGPL.  See the LICENSE files for details.


2024-03-14, happy Pi day, have fun/cheers,
Pat Deegan