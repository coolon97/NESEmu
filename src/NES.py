import cpu
import rom
import ram
import nesio
import ppu
import apu
import bus


class NES:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.io = nesio.NesIO()
        self.ram = ram.RAM()
        self.ppu = ppu.PPU()
        self.apu = apu.APU()
        self.rom = False
        self.cpu = False

    def load(self, data):
        self.rom = rom.ROM(data)
        
    def start(self):
        self.bus = bus.BUS(self.ram, self.rom, self.ppu, self.apu, self.io)
        self.cpu = cpu.CPU(self.bus)
        self.cpu.start()
