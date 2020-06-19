class ROM:
    def __init__(self, data):
        self.rom = data

    def size(self):
        return len(self.rom)

    def read(self, addr):
        return self.rom[addr]
