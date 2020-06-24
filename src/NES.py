import cpu
import rom
import ram
import io
import ppu
import apu


class Nes:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.io = io.IO()
        self.ram = ram.RAM()
        self.ppu = ppu.PPU()
        self.apu = apu.APU()
        self.cpu = cpu.CPU()

    def load(self, data):
        self.rom = rom.ROM(data)
        
    def start(self):
        cpu.run()
