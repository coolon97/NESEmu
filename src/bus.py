class BUS:
    def __init__(self, ram, rom, ppu, apu, io):
        self.ram = ram
        self.rom = rom
        self.ppu = ppu
        self.apu = apu
        self.io = io

    def read(self, addr):
        if addr < 0x0800:
            return self.ram.read(addr)
        elif addr < 0x2000:
            return self.ram.read(addr - 0x0800)
        elif addr < 0x4000:
            return self.ppu.read((addr - 0x2000) % 8)
        elif addr == 0x4016:
            return self.io.read()
        elif addr >= 0xC000:
            if self.rom.sizeOf() <= 0x4000:
                return self.rom.read(addr - 0xC000)
            return self.rom.read(addr - 0x8000)
        elif addr >= 0x08000:
            return self.rom.read(addr - 0x8000)
        else:
            return 0

    def write(self, addr, data):
        if addr < 0x0800:
            return self.ram.write(addr, data)
        elif addr < 0x2000:
            return self.ram.write(addr - 0x0800, data)
        elif addr < 0x4008:
            return self.ppu.write((addr - 0x2000), data)
        elif addr == 0x4016:
            return self.io.write()
        else:
            self.apu.write(addr - 0x4000, data)
