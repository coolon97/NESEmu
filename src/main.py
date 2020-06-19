import CPU
import ROM
import parser

cpu = CPU.CPU()
with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
    rom = ROM.ROM(parser.parse(nesFile.read())[0])
cpu.load()
