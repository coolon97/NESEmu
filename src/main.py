import NES
import parser

with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
    nes = NES.Nes()
    nes.load(parser.parse(nesFile.read()))
    nes.start()
