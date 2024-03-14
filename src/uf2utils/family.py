'''
Created on Mar 13, 2024


Based on https://github.com/microsoft/uf2/blob/master/utils/uf2families.json


@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
FamilyDescriptions = [
  {
    'id': 0x16573617,
    'name': 'ATMEGA32',
    'description': 'Microchip (Atmel) ATmega32',
  },
  {
    'id': 0x1851780a,
    'name': 'SAML21',
    'description': 'Microchip (Atmel) SAML21',
  },
  {
    'id': 0x1b57745f,
    'name': 'NRF52',
    'description': 'Nordic NRF52',
  },
  {
    'id': 0x1c5f21b0,
    'name': 'ESP32',
    'description': 'ESP32',
  },
  {
    'id': 0x1e1f432d,
    'name': 'STM32L1',
    'description': 'ST STM32L1xx',
  },
  {
    'id': 0x202e3a91,
    'name': 'STM32L0',
    'description': 'ST STM32L0xx',
  },
  {
    'id': 0x21460ff0,
    'name': 'STM32WL',
    'description': 'ST STM32WLxx',
  },
  {
    'id': 0x2abc77ec,
    'name': 'LPC55',
    'description': 'NXP LPC55xx',
  },
  {
    'id': 0x300f5633,
    'name': 'STM32G0',
    'description': 'ST STM32G0xx',
  },
  {
    'id': 0x31d228c6,
    'name': 'GD32F350',
    'description': 'GD32F350',
  },
  {
    'id': 0x04240bdf,
    'name': 'STM32L5',
    'description': 'ST STM32L5xx',
  },
  {
    'id': 0x4c71240a,
    'name': 'STM32G4',
    'description': 'ST STM32G4xx',
  },
  {
    'id': 0x4fb2d5bd,
    'name': 'MIMXRT10XX',
    'description': 'NXP i.MX RT10XX',
  },
  {
    'id': 0x53b80f00,
    'name': 'STM32F7',
    'description': 'ST STM32F7xx',
  },
  {
    'id': 0x55114460,
    'name': 'SAMD51',
    'description': 'Microchip (Atmel) SAMD51',
  },
  {
    'id': 0x57755a57,
    'name': 'STM32F4',
    'description': 'ST STM32F4xx',
  },
  {
    'id': 0x5a18069b,
    'name': 'FX2',
    'description': 'Cypress FX2',
  },
  {
    'id': 0x5d1a0a2e,
    'name': 'STM32F2',
    'description': 'ST STM32F2xx',
  },
  {
    'id': 0x5ee21072,
    'name': 'STM32F1',
    'description': 'ST STM32F103',
  },
  {
    'id': 0x621e937a,
    'name': 'NRF52833',
    'description': 'Nordic NRF52833',
  },
  {
    'id': 0x647824b6,
    'name': 'STM32F0',
    'description': 'ST STM32F0xx',
  },
  {
    'id': 0x68ed2b88,
    'name': 'SAMD21',
    'description': 'Microchip (Atmel) SAMD21',
  },
  {
    'id': 0x6b846188,
    'name': 'STM32F3',
    'description': 'ST STM32F3xx',
  },
  {
    'id': 0x6d0922fa,
    'name': 'STM32F407',
    'description': 'ST STM32F407',
  },
  {
    'id': 0x6db66082,
    'name': 'STM32H7',
    'description': 'ST STM32H7xx',
  },
  {
    'id': 0x70d16653,
    'name': 'STM32WB',
    'description': 'ST STM32WBxx',
  },
  {
    'id': 0x7eab61ed,
    'name': 'ESP8266',
    'description': 'ESP8266',
  },
  {
    'id': 0x7f83e793,
    'name': 'KL32L2',
    'description': 'NXP KL32L2x',
  },
  {
    'id': 0x8fb060fe,
    'name': 'STM32F407VG',
    'description': 'ST STM32F407VG',
  },
  {
    'id': 0xada52840,
    'name': 'NRF52840',
    'description': 'Nordic NRF52840',
  },
  {
    'id': 0xbfdd4eee,
    'name': 'ESP32S2',
    'description': 'ESP32-S2',
  },
  {
    'id': 0xc47e5767,
    'name': 'ESP32S3',
    'description': 'ESP32-S3',
  },
  {
    'id': 0xd42ba06c,
    'name': 'ESP32C3',
    'description': 'ESP32-C3',
  },
  {
    'id': 0x2b88d29c,
    'name': 'ESP32C2',
    'description': 'ESP32-C2',
  },
  {
    'id': 0x332726f6,
    'name': 'ESP32H2',
    'description': 'ESP32-H2',
  },
  {
    'id': 0xe48bff56,
    'name': 'RP2040',
    'description': 'Raspberry Pi RP2040',
  },
  {
    'id': 0x00ff6919,
    'name': 'STM32L4',
    'description': 'ST STM32L4xx',
  },
  {
    'id': 0x9af03e33,
    'name': 'GD32VF103',
    'description': 'GigaDevice GD32VF103',
  },
  {
    'id': 0x4f6ace52,
    'name': 'CSK4',
    'description': 'LISTENAI CSK300x/400x',
  },
  {
    'id': 0x6e7348a8,
    'name': 'CSK6',
    'description': 'LISTENAI CSK60xx',
  },
  {
    'id': 0x11de784a,
    'name': 'M0SENSE',
    'description': 'M0SENSE BL702',
  }
]

class Family:
    
    @classmethod
    def byId(cls, id:int):
        for fam in FamilyDescriptions:
            if fam['id'] == id:
                return cls(fam['id'], fam['name'], fam['description'])
            
        return None
    
    @classmethod 
    def byName(cls, name:str):
        for fam in FamilyDescriptions:
            if fam['name'] == name:
                return cls(fam['id'], fam['name'], fam['description'])
            
        return None
        
    
    def __init__(self, id:int, name:str, description:str):
        self.id = id 
        self.name = name 
        self.description = description
        
    def __repr__(self):
        return f'<Family {self.name} {hex(self.id)}>'
        
        