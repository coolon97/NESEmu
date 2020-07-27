import oplist


class CPU:
    class Registers:
        def __init__(self):
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

    def __init__(self, bus):
        print('initialize...')
        self.registers = self.Registers()
        self.bus = bus
        self.reset()

    def reset(self):
        print('cpu reset...')
        self.registers.reset()
        self.registers.PC = (((self.read(0xFFFD) << 8) | self.read(0xFFFC)) & 0xFFFF ) - 1

    def read(self, addr):
        if addr == None:
            return 0xFF
        return self.bus.read(addr)

    def write(self, addr, data):
        self.bus.write(addr, data)

    def push(self, data):
        self.write(0x100 | (self.registers.S & 0xFF), data)
        self.registers.S -= 1

    def pop(self):
        self.registers.S += 1
        return self.read(0x100 | (self.registers.S & 0xFF))

    def pushP(self):
        status = self.registers.P["negative"] << 7 | self.registers.P["overflow"] << 6 | self.registers.P["reserved"] << 5 | self.registers.P[
            "break"] << 4 | self.registers.P["decimal"] << 3 | self.registers.P["interrupt"] << 2 | self.registers.P["zero"] << 1 | self.registers.P["carry"]
        self.push(status)

    def popP(self):
        status = self.pop()
        self.registers.P["negative"] = bool(status & 0x80)
        self.registers.P["overflow"] = bool(status & 0x40)
        self.registers.P["reserved"] = bool(status & 0x20)
        self.registers.P["break"] = bool(status & 0x10)
        self.registers.P["decimal"] = bool(status & 0x08)
        self.registers.P["interrupt"] = bool(status & 0x04)
        self.registers.P["zero"] = bool(status & 0x02)
        self.registers.P["carry"] = bool(status & 0x01)

    def branch(self, addr):
        self.registers.PC = addr

    def fetch(self):
        self.registers.PC += 1
        return self.read(self.registers.PC)

    def fetchOperand(self, addressing):
        if addressing == 'accum':
            return None
        elif addressing == 'impl':
            return None
        elif addressing == 'immed':
            return self.fetch()
        elif addressing == 'zpg':
            return self.fetch()
        elif addressing == 'zpgx':
            addr = self.fetch()
            return (addr + self.registers.X) & 0xFFFF
        elif addressing == 'zpgy':
            addr = self.fetch()
            return (addr + self.registers.Y) & 0xFFFF
        elif addressing == 'rel':
            addr = self.fetch()
            return self.registers.PC + (addr if addr<=0x7F else addr-256) 
        elif addressing == 'abs':
            addrL = self.fetch() 
            addrH = self.fetch() << 8
            return (addrL | addrH) & 0xFFFF
        elif addressing == 'absx':
            addrL = self.fetch()
            addrH = self.fetch() << 8
            addr = (addrL | addrH) & 0xFFFF
            return (addr + self.registers.X) & 0xFFFF
        elif addressing == 'absy':
            addrL = self.fetch()
            addrH = self.fetch() << 8
            addr = (addrL | addrH) & 0xFFFF
            return (addr + self.registers.Y) & 0xFFFF
        elif addressing == 'xind':
            self.registers.PC += 1
            base = (self.read(self.registers.PC) + self.registers.X) & 0xFFFF
            addr = self.read(base) + (self.read(base + 0x01) & 0xFFFF) << 8
            return addr & 0xFFFF
        elif addressing == 'indy':
            data = self.fetch()
            base = (self.read(data) << 8) + self.read(data + 0x01) & 0xFFFF
            addr = base + self.registers.Y
            return addr & 0xFFFF
        elif addressing == 'ind':
            data = self.fetch()
            addr = self.read(data) + (self.read((data & 0xFF00)
                                                | (((data & 0xFF) + 0x01) & 0xFF)) << 8)
            return addr & 0xFFFF

    def exec(self, code, operand, mode):
        if code in oplist.BASE["LDA"]:
            self.registers.A = operand if mode == 'immed' else self.read(
                operand)
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in oplist.BASE["LDX"]:
            self.registers.X = operand if mode == 'immed' else self.read(
                operand)
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in oplist.BASE["LDY"]:
            self.registers.Y = operand if mode == 'immed' else self.read(
                operand)
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in oplist.BASE["STA"]:
            self.write(operand, self.registers.A)

        elif code in oplist.BASE["STX"]:
            self.write(operand, self.registers.X)

        elif code in oplist.BASE["STY"]:
            self.write(operand, self.registers.Y)

        elif code in oplist.BASE["TAX"]:
            self.registers.X = self.registers.A
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in oplist.BASE["TAY"]:
            self.registers.Y = self.registers.A
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in oplist.BASE["TSX"]:
            self.registers.X = self.registers.S & 0xFF
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in oplist.BASE["TXA"]:
            self.registers.A = self.registers.X
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in oplist.BASE["TXS"]:
            self.registers.S = (0x0100 | self.registers.X) & 0xFFFF
            self.registers.P["negative"] = bool(self.registers.S & 0x80)
            self.registers.P["zero"] = not bool(self.registers.S)

        elif code in oplist.BASE["TYA"]:
            self.registers.A = self.registers.Y
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in oplist.BASE["ADC"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A + data + self.registers.P["carry"]
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["overflow"] = (((self.registers.A ^ op) & 0x80) != 0 and (
                (self.registers.A ^ ~data) & 0x80) != 0)
            self.registers.P["carry"] = op > 0xFF
            self.registers.P["zero"] = not bool(op & 0xFF)
            self.registers.A = op & 0xFF

        elif code in oplist.BASE["AND"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A & data
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)
            self.registers.A = op & 0xFF

        elif code in oplist.BASE["ASL"]:
            if mode == 'accum':
                acc = self.registers.A
                self.registers.P["carry"] = bool(acc & 0x80)
                self.registers.A = (acc << 1) & 0xFF
                self.registers.P["negative"] = bool(self.registers.A & 0x80)
                self.registers.P["zero"] = not bool(self.registers.A)
            else:
                data = self.read(operand)
                self.registers.P["carry"] = bool(data & 0x80)
                op = (data << 1) & 0xFF
                self.write(operand, op)
                self.registers.P["negative"] = bool(op & 0x80)
                self.registers.P["zero"] = not bool(op)

        elif code in oplist.BASE["BIT"]:
            data = self.read(operand)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["overflow"] = bool(data & 0x40)
            self.registers.P["zero"] = not bool(self.registers.A & data)

        elif code in oplist.BASE["CMP"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.A == data
            self.registers.P["carry"] = op

        elif code in oplist.BASE["CPX"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.X >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.X == data
            self.registers.P["carry"] = op

        elif code in oplist.BASE["CPY"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.Y >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.Y == data
            self.registers.P["carry"] = op

        elif code in oplist.BASE["DEC"]:
            data = (self.read(operand) + 0xFF) & 0xFF
            self.write(operand, data)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in oplist.BASE["DEX"]:
            data = (self.registers.X + 0xFF) & 0xFF
            self.registers.X = data
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in oplist.BASE["DEY"]:
            data = (self.registers.Y + 0xFF) & 0xFF
            self.registers.Y = data
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in oplist.BASE["EOR"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A ^ data
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["zero"] = not bool(op)
            self.registers.A = op & 0xFF

        elif code in oplist.BASE["INC"]:
            data = (self.read(operand) + 1) & 0xFF
            self.write(operand, data)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in oplist.BASE["INX"]:
            self.registers.X = (self.registers.X + 1) & 0xFF
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in oplist.BASE["INY"]:
            self.registers.Y = (self.registers.Y + 1) & 0xFF
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in oplist.BASE["LSR"]:
            if mode == 'accum':
                self.registers.P["carry"] = bool(self.registers.A & 0x01)
                self.registers.A = (self.registers.A >> 1) & 0xFF
                self.registers.P["zero"] = not bool(self.registers.A)
            else:
                data = self.read(operand)
                self.registers.P["carry"] = bool(data & 0x01)
                data = (data >> 1) & 0xFF
                self.registers.P["zero"] = not bool(data)
                self.write(operand, data)
            self.registers.P["negative"] = False

        elif code in oplist.BASE["ORA"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A | data
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["zero"] = not bool(op)
            self.registers.A = op & 0xFF

        elif code in oplist.BASE["ROL"]:
            carry = self.registers.P["carry"]
            if mode == 'accum':
                self.registers.P["carry"] = bool(self.registers.A & 0x80)
                self.registers.A = ((self.registers.A << 1) + carry) & 0xFF
                self.registers.P["zero"] = not bool(self.registers.A)
                self.registers.P["negative"] = bool(self.registers.A & 0x80)
            else:
                data = self.read(operand)
                self.registers.P["carry"] = bool(data & 0x80)
                data = ((data << 1) + carry) & 0xFF
                self.registers.P["negative"] = bool(data & 0x80)
                self.registers.P["zero"] = not bool(data)
                self.write(operand, data)

        elif code in oplist.BASE["ROR"]:
            carry = self.registers.P["carry"]
            if mode == 'accum':
                self.registers.P["carry"] = bool(self.registers.A & 0x01)
                if carry:
                    self.registers.A = ((self.registers.A >> 1) + 0x80) & 0xFF
                    self.registers.P["negative"] = True
                else:
                    self.registers.A = (self.registers.A >> 1) & 0x7F
                    self.registers.P["negative"] = False
                self.registers.P["zero"] = not bool(self.registers.A)
            else:
                data = self.read(operand)
                self.registers.P["carry"] = bool(data & 0x01)
                if carry:
                    data = ((data >> 1) + 0x80) & 0xFF
                    self.registers.P["negative"] = True
                else:
                    data = (data >> 1) & 0xFF
                    self.registers.P["negative"] = False
                self.registers.P["zero"] = not bool(data)
                self.write(operand, data)

        elif code in oplist.BASE["SBC"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = (self.registers.A + ~data+1 + ~self.registers.P["carry"]+1)
            self.registers.P["overflow"] = (((self.registers.A ^ op) & 0x80) != 0 and (
                (self.registers.A ^ ~data) & 0x80) != 0)
            self.registers.A = op & 0xFF
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)
            self.registers.P["carry"] = op >= 0xFF

        elif code in oplist.BASE["PHA"]:
            self.push(self.registers.A)

        elif code in oplist.BASE["PLA"]:
            data = self.pop()
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)
            self.registers.A = data

        elif code in oplist.BASE["PHP"]:
            self.pushP()

        elif code in oplist.BASE["PLP"]:
            self.popP()

        elif code in oplist.BASE["JMP"]:
            self.registers.PC = operand - 1

        elif code in oplist.BASE["JSR"]:
            pc = self.registers.PC
            self.push((pc >> 8) & 0xFF)
            self.push(pc & 0xFF)
            self.registers.PC = operand - 1

        elif code in oplist.BASE["RTS"]:
            pc = self.pop()
            pc += (self.pop() << 8)
            self.registers.PC = pc
            self.registers.PC += 1

        elif code in oplist.BASE["RTI"]:
            self.popP()
            pc = self.pop()
            pc += (self.pop() << 8)
            self.registers.PC = pc & 0xFFFF
            self.registers.P["reserved"] = True

        elif code in oplist.BASE["BCC"]:
            if not self.registers.P["carry"]:
                self.branch(operand)

        elif code in oplist.BASE["BCS"]:
            if self.registers.P["carry"]:
                self.branch(operand)

        elif code in oplist.BASE["BEQ"]:
            if self.registers.P["zero"]:
                self.branch(operand)

        elif code in oplist.BASE["BMI"]:
            if self.registers.P["negative"]:
                self.branch(operand)

        elif code in oplist.BASE["BNE"]:
            if not self.registers.P["zero"]:
                self.branch(operand)

        elif code in oplist.BASE["BPL"]:
            if not self.registers.P["negative"]:
                self.branch(operand)

        elif code in oplist.BASE["BVC"]:
            if not self.registers.P["overflow"]:
                self.branch(operand)

        elif code in oplist.BASE["BVS"]:
            if self.registers.P["overflow"]:
                self.branch(operand)

        elif code in oplist.BASE["CLC"]:
            self.registers.P["carry"] = False

        elif code in oplist.BASE["CLI"]:
            self.registers.P["interrupt"] = False

        elif code in oplist.BASE["CLV"]:
            self.registers.P["overflow"] = False

        elif code in oplist.BASE["SEC"]:
            self.registers.P["carry"] = True

        elif code in oplist.BASE["SEI"]:
            self.registers.P["interrupt"] = True

        elif code in oplist.BASE["BRK"]:
            interrupt = self.registers.P["interrupt"]
            if not interrupt:
                self.registers.P["break"] = True
                self.registers.PC += 1
                self.push((self.registers.PC >> 8) & 0xFF)
                self.push(self.registers.PC & 0xFF)
                self.pushP()
                self.registers.P["interrupt"] = True
                self.registers.PC = ((self.read(0xFFFF) << 8) | self.read(0xFFFE)) & 0xFFFF

        elif code in oplist.BASE["NOP"]:
            pass

    def run(self):
        code = self.fetch()
        cycle, mode = oplist.CYCLES[code], oplist.MODE[code]
        operand = self.fetchOperand(mode)
        self.exec(code, operand, mode)
        return cycle
    
    def debugRun(self):
        codename = ''
        code = self.fetch()
        mode = oplist.MODE[code]
        operand = self.fetchOperand(mode)
        for key in oplist.BASE.keys():
            if code in oplist.BASE[key]:
                codename = key
        if codename == '':
            codename = "NOP"
        self.exec(code, operand, mode)
        return 'operation {"' + str(hex(code)) + '", mode:' + mode + ', operand:' + ("None" if operand is None else str(hex(operand))) + '}.'

    def start(self):
        count = 0
        while(True):
            count += 1
            self.run()
            if count > 500000:
                print("ok")
                count = 0
