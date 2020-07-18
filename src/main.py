import parser
import nes
import sys

r = []
with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
    r = parser.parse(nesFile.read())
    nesFile.close()
n = nes.NES()
n.load(r)
n.start()
