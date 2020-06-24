import parser



with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
    rom = rom.ROM(parser.parse(nesFile.read())[0])

