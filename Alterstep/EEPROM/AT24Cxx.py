import smbus

EEPROMbus = smbus.SMBus(1)
Device_Address = 0x57  # note EEPROM address may be 0X56
'''
Check your EEPROM address using: sudo i2c detect -y 1

  AT24C32 Code
  datasheet: atmel.com/Images/doc0336.pdf
  '''


def set_current_AT24C32_address(EEPROM_Memory_Address):
    a1 = int(EEPROM_Memory_Address / 256)
    a0 = int(EEPROM_Memory_Address % 256)

    EEPROMbus.write_i2c_block_data(Device_Address, a1, [a0])
    return;


def read_AT24C32_byte(EEPROM_Memory_Address):
    set_current_AT24C32_address(EEPROM_Memory_Address)
    return EEPROMbus.read_byte(Device_Address);


def write_AT24C32_block(EEPROM_Address, value):
    a1 = int(EEPROM_Address / 256)
    a0 = int(EEPROM_Address % 256)

    EEPROMbus.write_i2c_block_data(Device_Address, a1, [a0, value])
    time.sleep(0.20)
    return;


def write_AT24C32_byte(EEPROM_Memory_Address, value):
    EEPROMbus.write_byte_data(Device_Address, EEPROM_Memory_Address, value)
    time.sleep(0.20)
    return;


# example of storing string values into the EEPROM
sString = "Bad Boys Race Our Young Girls Over Victory Garden Walls Get Started Now"
byteArray = bytearray()
byteArray.extend(sString.encode())

iStartingAddress = 0  # next starting address
iEndingAddress = 0

'''
write

'''
for byteVal in byteArray:
    write_AT24C32_block(iEndingAddress, byteVal)
    iEndingAddress = iEndingAddress + 1

print("Ending Address, used as starting address of next data: " + str(iEndingAddress))

'''
read

'''
sString = ""
sTemp = b""
for iX in range(iStartingAddress, iEndingAddress):
    sTemp = bytes([read_AT24C32_byte(iX)])  # note the [ ]
    sString = sString + sTemp.decode('utf-8')

print(sString)
