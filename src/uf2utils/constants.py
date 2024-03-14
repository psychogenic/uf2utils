'''
Created on Mar 13, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

BlockSize = 512
MaxPayloadSize = 476
DefaultBlockPayloadSize = 256

class Magic:
    START0 = 0x0A324655 
    START1 = 0x9E5D5157 
    END    = 0x0AB16F30 

class Flags:
    NotMainFlash = 0x00000001
    FileContainer = 0x00001000
    FamilyIDPresent = 0x00002000
    MD5ChecksumPresent = 0x00004000
    ExtensionTagsPresent = 0x00008000
    
