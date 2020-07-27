import oplist

class CPU:
    def __init__(self, ppu):
        self.ppu = ppu
        self.reset()

    def reset(self):
        self.A = 0x00
        self.X = 0x00
        self.Y = 0x00
        self.S = 0x01FF
        self.PC = 0x0000
        self.P = {
            "negative": False,
            "overflow": False,
            "reserved": True,
            "break": True,
            "decimal": False,
            "interrupt": True,
            "zero": False,
            "carry": False
        }
        self.rom = None
        self.ram = [0 for i in range(2048)]

    def load(self, rom):
        self.rom = rom
        self.PC = (((self.read(0xFFFD) << 8) | self.read(0xFFFC)) & 0xFFFF ) - 1
    
    def read(self, addr):
        if addr >= 0x8000:
            return self.rom[addr-0x8000]
        elif addr < 0x2000:
            return self.ram[addr]
        elif addr < 0x4000:
            return self.ppu.vram[(addr - 0x2000) % 8]
    
    def fetch(self):
        self.PC += 1
        return self.read(self.PC)

    def write(self, addr, data):
        if addr < 0x2000:
            self.ram[addr] = data
        elif addr < 0x4000:
            pass
            #self.ppu.vram[(addr - 0x2000) % 8] = data

    def push(self, data):
        self.write(0x100 | (self.S & 0xFF), data)
        self.S -= 1

    def pop(self):
        self.S += 1
        return self.read(0x100 | (self.S & 0xFF))

    def pushP(self):
        status = self.P["negative"] << 7 | self.P["overflow"] << 6 | self.P["reserved"] << 5 | self.P[
            "break"] << 4 | self.P["decimal"] << 3 | self.P["interrupt"] << 2 | self.P["zero"] << 1 | self.P["carry"]
        self.push(status)

    def popP(self):
        status = self.pop()
        self.P["negative"] = bool(status & 0x80)
        self.P["overflow"] = bool(status & 0x40)
        self.P["reserved"] = bool(status & 0x20)
        self.P["break"] = bool(status & 0x10)
        self.P["decimal"] = bool(status & 0x08)
        self.P["interrupt"] = bool(status & 0x04)
        self.P["zero"] = bool(status & 0x02)
        self.P["carry"] = bool(status & 0x01)

    def branch(self, addr):
        self.PC = addr
    
    def zeropage_indexedX(self, addr):
        return (addr + self.X) & 0xFFFF

    def zeropage_indexedY(self, addr):
        return (addr + self.Y) & 0xFFFF

    def relative(self, addr):
        return self.PC + (addr if addr<=0x7F else addr-256) 

    def absolute(self, addr):
        return (addr | (self.fetch() << 8)) & 0xFFFF

    def absolute_indexedX(self, addr):
        return ((addr | (self.fetch() << 8)) + self.X) & 0xFFFF

    def absolute_indexedY(self, addr):
        return ((addr | (self.fetch() << 8)) + self.Y) & 0xFFFF

    def indexed_indirect(self, addr):
        base = (addr + self.X) & 0xFFFF
        addr = self.read(base) + (self.read(base + 0x01) & 0xFFFF) << 8
        return addr & 0xFFFF
        
    def indirect_indexed(self, addr):
        addr = (self.read(addr) | (self.read(addr + 0x01)  << 8))
        return (addr + self.Y) & 0xFFFF
            
    def absolute_indirect(self, addr):
        base = self.absolute(addr)
        addr = (self.read(base) | (self.read(base + 0x01) << 8))
        return addr & 0xFFFF

    #opcode LDA
    def ope_0xa9(self):
        self.A = self.fetch()
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xa5(self):
        self.A = self.read(self.fetch())
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xad(self):
        self.A = self.read(self.absolute(self.fetch()))
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xb5(self):
        self.A = self.read(self.zeropage_indexedX(self.fetch()))
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xbd(self):
        self.A = self.read(self.absolute_indexedX(self.fetch()))
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xb9(self):
        self.A = self.read(self.absolute_indexedY(self.fetch()))
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
    
    def ope_0xa1(self):
        self.A = self.read(self.indexed_indirect(self.fetch())) 
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0xb1(self):
        self.A = self.read(self.indirect_indexed(self.fetch())) 
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    #opcode LDA
    def ope_0xa2(self):
        self.X = self.fetch()
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)
    
    def ope_0xa6(self):
        self.X = self.read(self.fetch())
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)
    
    def ope_0xae(self):
        self.X = self.read(self.absolute(self.fetch))
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)

    def ope_0xb6(self):
        self.X = self.read(self.zeropage_indexedY(self.fetch()))
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)

    def ope_0xbe(self):
        self.X = self.read(self.absolute_indexedX(self.fetch()))
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)

    #opcode LDY
    def ope_0xa0(self):
        self.Y = self.fetch()
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    def ope_0xa4(self):
        self.Y = self.read(self.fetch())
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    def ope_0xac(self):
        self.Y = self.read(self.absolute(self.fetch()))
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    def ope_0xb4(self):
        self.Y = self.read(self.zeropage_indexedY(self.fetch()))
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    def ope_0xbc(self):
        self.Y = self.read(self.absolute_indexedX(self.fetch()))
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    #opcode STA
    def ope_0x85(self):
        self.write(self.read(self.fetch()), self.A)
    
    def ope_0x8d(self):
        self.write(self.read(self.absolute(self.fetch())), self.A)

    def ope_0x95(self):
        self.write(self.read(self.zeropage_indexedX(self.fetch())), self.A)

    def ope_0x9d(self):
        self.write(self.read(self.absolute_indexedX(self.fetch())), self.A)

    def ope_0x99(self):
        self.write(self.read(self.absolute_indexedY(self.fetch())), self.A)

    def ope_0x81(self):
        self.write(self.read(self.indexed_indirect(self.fetch())), self.A)

    def ope_0x91(self):
        self.write(self.read(self.indirect_indexed(self.fetch())), self.A)

    #opcode STX
    def ope_0x86(self):
        self.write(self.read(self.fetch()), self.X)

    def ope_0x8e(self):
        self.write(self.read(self.absolute(self.fetch())), self.X)

    def ope_0x96(self):
        self.write(self.read(self.zeropage_indexedY(self.fetch())), self.X)

    #opcode STY
    def ope_0x84(self):
        self.write(self.read(self.fetch()), self.Y)

    def ope_0x8c(self):
        self.write(self.read(self.absolute(self.fetch())), self.Y)

    def ope_0x94(self):
        self.write(self.read(self.zeropage_indexedY(self.fetch())), self.Y)

    #opcode TAX
    def ope_0xaa(self):
        self.X = self.A
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)

    #opcode TAY
    def ope_0xa8(self):
        self.Y = self.A
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)
            
    #opcode TSX
    def ope_0xba(self):
        self.X = self.S & 0xFF
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)

    #opcode TXA
    def ope_0x8a(self):
        self.A = self.X
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    #opcode TYA
    def ope_0x98(self):
        self.S = (0x0100 | self.X) & 0xFFFF
        self.P["negative"] = bool(self.S & 0x80)
        self.P["zero"] = not bool(self.S)
            
    #opcode TXS
    def ope_0x9a(self):
        self.A = self.Y
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    #opcode ADC
    def ope_0x69(self):
        data = self.fetch()
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x65(self):
        data = self.read(self.fetch())
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x6d(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x75(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x7d(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x79(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x61(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    def ope_0x71(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = self.A + data + self.P["carry"]
        self.P["negative"] = bool(op & 0x80)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.P["carry"] = op > 0xFF
        self.P["zero"] = not bool(op & 0xFF)
        self.A = op & 0xFF

    #opcode AND
    def ope_0x29(self):
        data = self.fetch()
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF
    
    def ope_0x25(self):
        data = self.read(self.fetch())
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x2d(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x35(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x3d(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x39(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x21(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    def ope_0x31(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = self.A & data
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.A = op & 0xFF

    #opcode ASL
    def ope_0xa(self):
        acc = self.A
        self.P["carry"] = bool(acc & 0x80)
        self.A = (acc << 1) & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)

    def ope_0x6(self):
        addr = self.fetch()
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x80)
        op = (data << 1) & 0xFF
        self.write(addr, op)
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)

    def ope_0xe(self):
        addr = self.absolute(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x80)
        op = (data << 1) & 0xFF
        self.write(addr, op)
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)

    def ope_0x16(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x80)
        op = (data << 1) & 0xFF
        self.write(addr, op)
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)

    def ope_0x1e(self):
        addr = self.absolute_indexedX(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x80)
        op = (data << 1) & 0xFF
        self.write(addr, op)
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)

    #opcode BIT
    def ope_0x24(self):
        data = self.read(self.fetch())
        self.P["negative"] = bool(data & 0x80)
        self.P["overflow"] = bool(data & 0x40)
        self.P["zero"] = not bool(self.A & data)

    def ope_0x2c(self):
        data = self.read(self.absolute(self.fetch()))
        self.P["negative"] = bool(data & 0x80)
        self.P["overflow"] = bool(data & 0x40)
        self.P["zero"] = not bool(self.A & data)
            
    #opcode CMP
    def ope_0xc9(self):
        data = self.fetch()
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op
    
    def ope_0xc5(self):
        data = self.read(self.fetch())
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xcd(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xd5(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xdd(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xd9(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xc1(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op

    def ope_0xd1(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = self.A >= data
        self.P["negative"] = op
        self.P["zero"] = self.A == data
        self.P["carry"] = op
            
    #opcode CPX
    def ope_0xe0(self):
        data = self.fetch()
        op = self.X >= data
        self.P["negative"] = op
        self.P["zero"] = self.X == data
        self.P["carry"] = op
    
    def ope_0xe4(self):
        data = self.read(self.fetch())
        op = self.X >= data
        self.P["negative"] = op
        self.P["zero"] = self.X == data
        self.P["carry"] = op

    def ope_0xec(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.X >= data
        self.P["negative"] = op
        self.P["zero"] = self.X == data
        self.P["carry"] = op

    #opcode CPY
    def ope_0xc0(self):
        data = self.fetch()
        op = self.Y >= data
        self.P["negative"] = op
        self.P["zero"] = self.Y == data
        self.P["carry"] = op

    def ope_0xc4(self):
        data = self.read(self.fetch())
        op = self.Y >= data
        self.P["negative"] = op
        self.P["zero"] = self.Y == data
        self.P["carry"] = op

    def ope_0xcc(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.Y >= data
        self.P["negative"] = op
        self.P["zero"] = self.Y == data
        self.P["carry"] = op

    #opcode DEC
    def ope_0xc6(self):
        addr = self.fetch()
        data = (self.read(addr) + 0xFF) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
    
    def ope_0xce(self):
        addr = self.absolute(self.fetch())
        data = (self.read(addr) + 0xFF) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    def ope_0xd6(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = (self.read(addr) + 0xFF) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    def ope_0xde(self):
        addr = self.absolute_indexedX(self.fetch())
        data = (self.read(addr) + 0xFF) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    #opcode DEX
    def ope_0xca(self):
        data = (self.X + 0xFF) & 0xFF
        self.X = data
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    #opcode DEY
    def ope_0x88(self):
        data = (self.Y + 0xFF) & 0xFF
        self.Y = data
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
    
    #opcode EOR
    def ope_0x49(self):
        data = self.fetch()
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x45(self):
        data = self.read(self.fetch())
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x4d(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x55(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x5d(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x59(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x41(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x51(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = self.A ^ data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    #opcode INC
    def ope_0xe6(self):
        addr = self.fetch()
        data = (self.read(addr) + 1) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
    
    def ope_0xee(self):
        addr = self.absolute(self.fetch())
        data = (self.read(addr) + 1) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
    
    def ope_0xf6(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = (self.read(addr ) + 1)& 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    def ope_0xfe(self):
        addr = self.absolute_indexedX(self.fetch())
        data = (self.read(addr) + 1) & 0xFF
        self.write(addr, data)
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)

    #opcode INX
    def ope_0xe8(self):
        self.X = (self.X + 1) & 0xFF
        self.P["negative"] = bool(self.X & 0x80)
        self.P["zero"] = not bool(self.X)
    
    #opcode INY
    def ope_0xc8(self):
        self.Y = (self.Y + 1) & 0xFF
        self.P["negative"] = bool(self.Y & 0x80)
        self.P["zero"] = not bool(self.Y)

    #opcode LSR
    def ope_0x4a(self):
        self.P["carry"] = bool(self.A & 0x01)
        self.A = (self.A >> 1) & 0xFF
        self.P["zero"] = not bool(self.A)
        self.P["negative"] = False
    
    def ope_0x46(self):
        addr = self.fetch()
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x01)
        data = (data >> 1) & 0xFF
        self.P["zero"] = not bool(data)
        self.write(addr, data)
        self.P["negative"] = False

    def ope_0x4e(self):
        addr = self.absolute(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x01)
        data = (data >> 1) & 0xFF
        self.P["zero"] = not bool(data)
        self.write(addr, data)
        self.P["negative"] = False
    
    def ope_0x56(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x01)
        data = (data >> 1) & 0xFF
        self.P["zero"] = not bool(data)
        self.write(addr, data)
        self.P["negative"] = False

    def ope_0x5e(self):
        addr = self.absolute_indexedY(self.fetch())
        data = self.read(addr)
        self.P["carry"] = bool(data & 0x01)
        data = (data >> 1) & 0xFF
        self.P["zero"] = not bool(data)
        self.write(addr, data)
        self.P["negative"] = False

    #opcode ORA
    def ope_0x9(self):
        data = self.fetch()
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0x5(self):
        data = self.read(self.fetch())
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF
    
    def ope_0xd(self):
        data = self.read(self.absolute(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x15(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x1d(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x19(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x1(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    def ope_0x11(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = self.A | data
        self.P["negative"] = bool(op & 0x80)
        self.P["zero"] = not bool(op)
        self.A = op & 0xFF

    #opcode ROL
    def ope_0x2a(self):
        carry = self.P["carry"]
        self.P["carry"] = bool(self.A & 0x80)
        self.A = ((self.A << 1) + carry) & 0xFF
        self.P["zero"] = not bool(self.A)
        self.P["negative"] = bool(self.A & 0x80)
    
    def ope_0x26(self):
        addr = self.fetch()
        data = self.read(addr)
        carry = self.P["carry"]
        self.P["carry"] = bool(data & 0x80)
        data = ((data << 1) + carry) & 0xFF
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
        self.write(addr, data)
    
    def ope_0x2e(self):
        addr = self.absolute(self.fetch())
        data = self.read(addr)
        carry = self.P["carry"]
        self.P["carry"] = bool(data & 0x80)
        data = ((data << 1) + carry) & 0xFF
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
        self.write(addr, data)
    
    def ope_0x36(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = self.read(addr)
        carry = self.P["carry"]
        self.P["carry"] = bool(data & 0x80)
        data = ((data << 1) + carry) & 0xFF
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    def ope_0x3e(self):
        addr = self.absolute_indexedX(self.fetch())
        data = self.read(addr)
        carry = self.P["carry"]
        self.P["carry"] = bool(data & 0x80)
        data = ((data << 1) + carry) & 0xFF
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    #opcode ROR
    def ope_0x6a(self):
        if self.P["carry"]:
            self.P["carry"] = bool(self.A & 0x01)
            self.A = ((self.A >> 1) + 0x80) & 0xFF
            self.P["negative"] = True
        else:
            self.A = (self.A >> 1) & 0x7F
            self.P["negative"] = False
        self.P["zero"] = not bool(self.A)

    def ope_0x66(self):
        addr = self.read(self.fetch())
        data = self.read(addr)
        if self.P["carry"]:
            self.P["carry"] = bool(data & 0x01)
            data = ((data >> 1) + 0x80) & 0xFF
            self.P["negative"] = True
        else:
            self.P["carry"] = bool(data & 0x01)
            data = (data >> 1) & 0xFF
            self.P["negative"] = False
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    def ope_0x6e(self):
        addr = self.absolute(self.fetch())
        data = self.read(addr)
        if self.P["carry"]:
            self.P["carry"] = bool(data & 0x01)
            data = ((data >> 1) + 0x80) & 0xFF
            self.P["negative"] = True
        else:
            self.P["carry"] = bool(data & 0x01)
            data = (data >> 1) & 0xFF
            self.P["negative"] = False
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    def ope_0x76(self):
        addr = self.zeropage_indexedX(self.fetch())
        data = self.read(addr)
        if self.P["carry"]:
            self.P["carry"] = bool(data & 0x01)
            data = ((data >> 1) + 0x80) & 0xFF
            self.P["negative"] = True
        else:
            self.P["carry"] = bool(data & 0x01)
            data = (data >> 1) & 0xFF
            self.P["negative"] = False
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    def ope_0x7e(self):
        addr = self.absolute_indexedX(self.fetch())
        data = self.read(addr)
        if self.P["carry"]:
            self.P["carry"] = bool(data & 0x01)
            data = ((data >> 1) + 0x80) & 0xFF
            self.P["negative"] = True
        else:
            self.P["carry"] = bool(data & 0x01)
            data = (data >> 1) & 0xFF
            self.P["negative"] = False
        self.P["zero"] = not bool(data)
        self.write(addr, data)

    #opcode SBC
    def ope_0xe9(self):
        data = self.fetch()
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF
    
    def ope_0xe5(self):
        data = self.read(self.fetch())
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xed(self):
        data = self.read(self.absolute(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xf5(self):
        data = self.read(self.zeropage_indexedX(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xfd(self):
        data = self.read(self.absolute_indexedX(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xf9(self):
        data = self.read(self.absolute_indexedY(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xe1(self):
        data = self.read(self.indexed_indirect(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    def ope_0xf1(self):
        data = self.read(self.indirect_indexed(self.fetch()))
        op = (self.A + ~data+1 + ~self.P["carry"]+1)
        self.P["overflow"] = (((self.A ^ op) & 0x80) != 0 and ((self.A ^ ~data) & 0x80) != 0)
        self.A = op & 0xFF
        self.P["negative"] = bool(self.A & 0x80)
        self.P["zero"] = not bool(self.A)
        self.P["carry"] = op >= 0xFF

    #PHA
    def ope_0x48(self):
        self.push(self.A)

    #PLA 
    def ope_0x68(self):
        data = self.pop()
        self.P["negative"] = bool(data & 0x80)
        self.P["zero"] = not bool(data)
        self.A = data

    #PHP
    def ope_0x8(self):
        self.pushP()

    #PLP
    def ope_0x28(self):
        self.popP()

    #JMP
    def ope_0x4c(self):
        self.PC = self.absolute(self.fetch()) - 1

    def ope_0x6c(self):
        self.PC = self.absolute_indirect(self.fetch()) - 1

    #JSR
    def ope_0x20(self):
        addr = self.read(self.absolute(self.fetch()))
        self.push((self.PC >> 8) & 0xFF)
        self.push(self.PC & 0xFF)
        self.PC = addr - 1

    #RTS
    def ope_0x60(self):
        self.PC = (self.pop() | self.pop() << 8) & 0xFFFF + 1

    #RTI
    def ope_0x40(self):
        self.popP()
        self.PC = (self.pop() | self.pop() << 8) & 0xFFFF + 1
        self.P["reserved"] = True
    
    #BCC
    def ope_0x90(self):
        if not self.P["carry"]:
            self.branch(self.relative(self.fetch()))

    #BCS
    def ope_0xb0(self):
        if self.P["carry"]:
            self.branch(self.relative(self.fetch()))

    #BEQ
    def ope_0xF0(self):
        if self.P["zero"]:
            self.branch(self.relative(self.fetch()))

    #BMI
    def ope_0x30(self):
        if self.P["negative"]:
            self.branch(self.relative(self.fetch()))

    #BNE
    def ope_0xd0(self):
        if not self.P["zero"]:
            self.branch(self.relative(self.fetch()))

    #BPL
    def ope_0x10(self):
        if not self.P["negative"]:
            self.branch(self.relative(self.fetch()))

    #BVC
    def ope_0x50(self):
        if not self.P["overflow"]:
            self.branch(self.relative(self.fetch()))

    #BVS
    def ope_0x70(self):
        if self.P["overflow"]:
            self.branch(self.relative(self.fetch()))

    #CLC
    def ope_0x18(self):
        self.P["carry"] = False

    #CLI
    def ope_0x58(self):
        self.P["interrupt"] = False

    #CLV
    def ope_0xbb(self):
        self.P["overflow"] = False

    #SEC
    def ope_38(self):
        self.P["carry"] = True

    #SEI
    def ope_0x78(self):
        self.P["interrupt"] = True

    #BRK
    def ope_0x0(self):
        interrupt = self.P["interrupt"]
        if not interrupt:
            self.P["break"] = True
            self.PC += 1
            self.push((self.PC >> 8) & 0xFF)
            self.push(self.PC & 0xFF)
            self.pushP()
            self.P["interrupt"] = True
            self.PC = ((self.read(0xFFFF) << 8) | self.read(0xFFFE)) & 0xFFFF
    
    def run(self):
        code = self.fetch()
        cycle, mode = oplist.CYCLES[code], oplist.MODE[code]
        try:
            self.__getattribute__("ope_" + hex(code))()
        except Exception as e:
            name = "NOP"
            for key, value in zip(oplist.BASE.keys(), oplist.BASE.values()):
                if code in value:
                    name = key
            print('operation {"' + name + '", mode:' + mode + ' }.')
        return cycle

    def debugRun(self):
        code = self.fetch()
        mode = oplist.MODE[code]
        try:
            self.__getattribute__("ope_" + hex(code))()
        except Exception as e:
            name = "NOP"
            for key, value in zip(oplist.BASE.keys(), oplist.BASE.values()):
                if code in value:
                    name = key
            print('operation {"' + name + '", mode:' + mode + ' }.')
        name = "NOP"
        for key, value in zip(oplist.BASE.keys(), oplist.BASE.values()):
            if code in value:
                name = key
        return 'operation {"' + name + '", mode:' + mode + ' }.'
    
