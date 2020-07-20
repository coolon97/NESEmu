import parser
import nes
import sys

if __name__ == "__main__":
    r = []
    with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
        r = parser.parse(nesFile.read())
        nesFile.close()
    n = nes.NES()

    n.load(r)
    #n.debug()
    n.start()
