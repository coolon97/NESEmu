class RAM:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.ram = [0]*2048
    
    def read(self, addr):
        return self.ram[addr]

    def write(self, addr, data):
        self.ram[addr] = data

