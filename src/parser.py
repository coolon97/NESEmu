NES_HEADER_SIZE = 0x0010
PROGRAM_ROM_SIZE = 0x4000
CHARACTER_ROM_SIZE = 0x2000


def parse(buf):
    if buf[:3] != b'NES':
        print("This file is not NES ROM.")
        return False

    characterROMPages = buf[4]
    characterROMStart = NES_HEADER_SIZE + buf[3] * PROGRAM_ROM_SIZE
    characterROMEnd = characterROMStart + characterROMPages * CHARACTER_ROM_SIZE
    print(buf[3], buf[4], characterROMStart, characterROMEnd)
    return [buf[NES_HEADER_SIZE:characterROMStart - 1], buf[characterROMStart:characterROMEnd]]
