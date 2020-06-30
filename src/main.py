import parser
import nes
import tkinter
import sys

r = []
with open("../roms/sample1/sample1.nes", mode='rb') as nesFile:
    r = parser.parse(nesFile.read())[0]

n = nes.NES()
n.load(r)
n.start()

