#import parser
import nes
import sys

NES_HEADER_SIZE = 0x0010
PROGRAM_ROM_SIZE = 0x4000
CHARACTER_ROM_SIZE = 0x2000

def parse(buf):
    if buf[:3] != b'NES':
        print("This file is not NES ROM.")
        return False

    characterROMPages = buf[5]
    characterROMStart = NES_HEADER_SIZE + buf[4] * PROGRAM_ROM_SIZE
    characterROMEnd = characterROMStart + characterROMPages * CHARACTER_ROM_SIZE
    print(buf[4], buf[5], characterROMStart, characterROMEnd)
    return [buf[NES_HEADER_SIZE:characterROMStart - 1], buf[characterROMStart:characterROMEnd]]

if __name__ == "__main__":
    r = []
    with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
        #r = parser.parse(nesFile.read())
        r = parse(nesFile.read())
        nesFile.close()
    n = nes.NES()

    #n.load(r)
    n.nload(r)
    #n.debug()
    #n.ndebug()
    #n.start()
    n.nstart()
