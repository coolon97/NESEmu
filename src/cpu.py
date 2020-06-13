import opcode


class CPU:
    class Registers:
        def __init__(self):
            self.reset()

        def reset(self):
            self.A = 0x00
            self.X = 0x00
            self.Y = 0x00
            self.S = 0x00
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
    
    def __init__(self):
        print('initialize...')
        self.registers = self.Registers()
        self.reset()

    def reset(self):
        print('cpu reset...')
        self.registers.reset()
        self.registers.PC = self.read(0xFFFC)

    def read(self, addr):
        print('ok')

    def write(self, addr, data):
        print('ok')
        
    def push(self, data):
        self.write(0x100 | (self.registers.S & 0xFF), data)
        self.registers.S -= 1

    def pop(self):
        self.registers.S += 1
        return self.read(0x100 | (self.registers.S & 0xFF))
    
    def pushP(self):
        status = self.registers.P["negative"] << 7 | self.registers.P["overflow"] << 6 | self.registers.P["reserved"] << 5 | self.registers.P["break"] << 4 | self.registers.P["decimal"] << 3 | self.registers.P["interrupt"] << 2 | self.registers.P["zero"] << 1 | self.registers.P["carry"]
        self.push(status)

    def popP(self):
        status = self.pop()
        self.registers.P["negative"] = status & 0x80
        self.registers.P["overflow"] = status & 0x40
        self.registers.P["reserved"] = status & 0x20
        self.registers.P["break"] = status & 0x10
        self.registers.P["decimal"] = status & 0x08
        self.registers.P["interrupt"] = status & 0x04
        self.registers.P["zero"] = status & 0x02
        self.registers.P["carry"] = status & 0x01

    def fetch(self, addr):
        self.registers.PC += 1
        return self.read(self.registers.PC)

    def fetchOpeland(self, addressing):
        if addressing == 'accum':
            return
        elif addressing == 'impl':
            return
        elif addressing == 'immed':
            return self.fetch()
        elif addressing == 'zpg':
            return self.fetch()
        elif addressing == 'zpgx':
            addr = self.fetch()
            return (addr + self.registers.X) & 0xFF
        elif addressing == 'zpgy':
            addr = self.fetch()
            return (addr + self.registers.Y) & 0xFF
        elif addressing == 'absx':
            addr = self.fetchWord()
            return (addr + self.registers.X) & 0xFFFF
        elif addressing == 'absy':
            addr = self.fetchWord()
            return (addr + self.registers.Y) & 0xFFFF
        elif addressing == 'xind':
            base = (self.fetch() + self.registers.X) & 0xFF
            addr = self.read(base) + (self.read(base + 0x01) & 0xFF) << 8
            return addr & 0xFFFF
        elif addressing == 'indy':
            data = self.fetch()
            base = self.read(data) + (self.read((data + 0x01) & 0xFF) << 8)
            addr = base + self.registers.Y
            return addr & 0xFFFF
        elif addressing == 'ind':
            data = self.fetchWord()
            addr = self.read(data) + (self.read((data & 0xFF00) | (((data & 0xFF) + 0x01) & 0xFF)) << 8)
            return addr & 0xFFFF

    def exec(self, code, operand, mode):
        if code in opcode.Base["LDA"]:
            self.registers.A = operand if mode == 'immed' else self.read(operand)
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in opcode.Base["LDX"]:
            self.registers.X = operand if mode == 'immed' else self.read(operand)
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in opcode.Base["LDY"]:
            self.registers.Y = operand if mode == 'immed' else self.read(operand)
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in opcode.Base["STA"]:
            self.write(operand, self.registers.A)
        
        elif code in opcode.Base["STX"]:
            self.write(operand, self.registers.X)
        
        elif code in opcode.Base["STY"]:
            self.write(operand, self.registers.Y)

        elif code in opcode.Base["TAX"]:
            self.registers.X = self.registers.A
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in opcode.Base["TAY"]:
            self.registers.Y = self.registers.A
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in opcode.Base["TSX"]:
            self.registers.X = self.registers.S
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in opcode.Base["TXA"]:
            self.registers.A = self.registers.X
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in opcode.Base["TXS"]:
            self.registers.S = self.registers.X
            self.registers.P["negative"] = bool(self.registers.S & 0x80)
            self.registers.P["zero"] = not bool(self.registers.S)

        elif code in opcode.Base["TYA"]:
            self.registers.A = self.registers.Y
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)

        elif code in opcode.Base["ADC"]:
            data = operand if mode == 'immed' else self.read(operand) 
            op = self.registers.A + operand + self.registers.P["carry"]
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["overflow"] = True if bool((self.registers ^ data) & 0x80) and bool((self.registers ^ self.registers.P["negative"]) & 0x80) != 0 else False
            self.registers.P["carry"] = op > 0xFF
            self.registers.P["zero"] = not bool(op & 0xFF)
            self.registers.A = op & 0xFF
        
        elif code in opcode.Base["AND"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A & data
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)
            self.registers.A = op & 0xFF
        
        elif code in opcode.Base["ASL"]:
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

        elif code in opcode.Base["BIT"]:
            data = self.read(operand)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["overflow"] = bool(data & 0x40)
            self.registers.P["zero"] = not bool(self.registers.A & data)

        elif code in opcode.Base["CMP"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.A == data
            self.registers.P["carry"] = op

        elif code in opcode.Base["CPX"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.X >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.X == data
            self.registers.P["carry"] = op

        elif code in opcode.Base["CPY"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.Y >= data
            self.registers.P["negative"] = op
            self.registers.P["zero"] = self.registers.Y == data
            self.registers.P["carry"] = op

        elif code in opcode.Base["DEC"]:
            data = (self.read(operand) + 0xFF) & 0xFF
            self.write(operand, data)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in opcode.Base["DEX"]:
            data = (self.registers.X + 0xFF) & 0xFF
            self.registers.X = data
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in opcode.Base["DEY"]:
            data = (self.registers.Y + 0xFF) & 0xFF
            self.registers.Y = data
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in opcode.Base["EOR"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A ^ data
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["zero"] = not bool(op)
            self.registers.A = op & 0xFF
            
        elif code in opcode.Base["INC"]:
            data = (self.read(operand) + 1) & 0xFF
            self.write(operand, data)
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)

        elif code in opcode.Base["INX"]:
            self.registers.X = (self.registers.X + 1) & 0xFF
            self.registers.P["negative"] = bool(self.registers.X & 0x80)
            self.registers.P["zero"] = not bool(self.registers.X)

        elif code in opcode.Base["INY"]:
            self.registers.Y = (self.registers.Y + 1) & 0xFF
            self.registers.P["negative"] = bool(self.registers.Y & 0x80)
            self.registers.P["zero"] = not bool(self.registers.Y)

        elif code in opcode.Base["LSR"]:
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

        elif code in opcode.Base["ORA"]:
            data = operand if mode == 'immed' else self.read(operand)
            op = self.registers.A | data
            self.registers.P["negative"] = bool(op & 0x80)
            self.registers.P["zero"] = not bool(op)
            self.registers.A = op & 0xFF

        elif code in opcode.Base["ROL"]:
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
                self.write(data)

        elif code in opcode.Base["ROR"]:
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
                self.write(data)
        
        elif code in opcode.Base["SBC"]:
            data = operand if mode == 'immed' else self.read()
            op = (self.registers.A + ~data + (0xFF if self.registers.P["carry"] else 0x00))
            self.registers.P["overflow"] = (((self.registers.A ^ op) & 0x80) != 0 and ((self.registers.A ^ ~data) & 0x80) != 0)
            self.registers.A = op & 0xFF
            self.registers.P["negative"] = bool(self.registers.A & 0x80)
            self.registers.P["zero"] = not bool(self.registers.A)
            self.registers.P["carry"] = op >= 0xFF

        elif code in opcode.Base["PHA"]:
            self.stack.push(self.registers.A)

        elif code in opcode.Base["PLA"]:
            data = self.stack.pop()
            self.registers.P["negative"] = bool(data & 0x80)
            self.registers.P["zero"] = not bool(data)
            self.registers.A = data

        elif code in opcode.Base["PHP"]:
            self.registers.P["break"] = True
            self.pushP()

        elif code in opcode.Base["PLP"]:
            data = self.popP()
            self.registers.P["reserved"] = True

        elif code in opcode.Base["JMP"]:
            self.registers.PC = operand

        elif code in opcode.Base["JSR"]:
            pc = (self.registers.PC + 0xFF) & 0xFF
            self.push((pc >> 8) & 0xFF)
            self.push(pc & 0xFF)
            self.registers.PC = operand

        elif code in opcode.Base["RTS"]:
            pc = self.pop()
            pc += (self.pop() << 8)
            self.registers.PC = pc
            self.registers.PC += 1

        elif code in opcode.Base["RTI"]:
            self.popP()
            pc = self.pop()
            pc += (self.pop() << 8)
            self.registers.PC = pc
            self.registers.P.reserved = True
        
        elif code in opcode.Base["BCC"]:
            if not self.registers.P["carry"]:
                self.branch(operand)

        elif code in opcode.Base["BCS"]:
            if self.registers.P["carry"]:
                self.branch(operand)

        elif code in opcode.Base["BEQ"]:
            if self.registers.P["zero"]:
                self.branch(operand)

        elif code in opcode.Base["BMI"]:
            if self.registers.P["negative"]:
                self.branch(operand)

        elif code in opcode.Base["BNE"]:
            if not self.registers.P["zero"]:
                self.branch(operand)

        elif code in opcode.Base["BPL"]:
            if not self.registers.P["negative"]:
                self.branch(operand)

        elif code in opcode.Base["BVC"]:
            if not self.registers.P["overflow"]:
                self.branch(operand)
            
        elif code in opcode.Base["BVS"]:
            if self.registers.P["overflow"]:
                self.branch(operand)

        elif code in opcode.Base["CLC"]:
            self.registers.P["carry"] = False

        elif code in opcode.Base["CLI"]:
            self.registers.P["interrupt"] = False

        elif code in opcode.Base["CLV"]:
            self.registers.P["overflow"] = False
        
        elif code in opcode.Base["SEC"]:
            self.registers.P["carry"] = True
        
        elif code in opcode.Base["SEI"]:
            self.registers.P["interrupt"] = True

        elif code in opcode.Base["BRK"]:
            interrupt = self.registers.P["interrupt"]
            self.registers.PC += 1
            self.push((self.registers.PC >> 8) & 0xFF)
            self.push(self.registers.PC & 0xFF)
            self.registers.P["break"] = True
            self.pushP()
            self.registers.P["interrupt"] = True
            if not interrupt:
                self.registers.PC = self.read(0xFFFE, "Word")
            self.registers.PC -= 1

        elif code in opcode.Base["NOP"]:
            pass




