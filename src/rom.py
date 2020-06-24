class ROM:
    def __init__(self, data):
        self.rom = data
        self.size = len(data)

    def sizeOf(self):
        return self.size

    def read(self, addr):
        return self.rom[addr]
