import struct

NES_HEADER_SIZE = 0x0010
PROGRAM_ROM_SIZE = 0x4000
CHARACTER_ROM_SIZE = 0x2000


def parse(buf):
    byte = []
    for b in iter(lambda: buf.read(1), b''):
        byte.append(struct.unpack('c', b)[0])
    print(''.join(map(lambda x: x.decode("utf8"), byte[:3])))
    if ''.join(map(lambda x: x.decode("utf8"), byte[:3])) != "NES":
        print("This file is not .nes file.")
    characterROMPages = buf[5]
    characterROMStart = NES_HEADER_SIZE + buf[4] * PROGRAM_ROM_SIZE
    characterROMEnd = characterROMStart + characterROMPages * CHARACTER_ROM_SIZE
    return characterROMStart, characterROMEnd
