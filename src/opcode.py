LDA_IMM = 0xA9
LDA_ZERO = 0xA5
LDA_ABS = 0xAD
LDA_ZEROX = 0xB5
LDA_ABSX = 0xBD
LDA_ABSY = 0xB9
LDA_INDX = 0xA1
LDA_INDY = 0xB1

LDX_IMM = 0xA2
LDX_ZERO = 0xA6
LDX_ABS = 0xAE
LDX_ZEROY = 0xB6
LDX_ABSY = 0xBE

LDY_IMM = 0xA0
LDY_ZERO = 0xA4
LDY_ABS = 0xAC
LDY_ZEROX = 0xB4
LDY_ABSX = 0xBC

STA_ZERO = 0x85
STA_ABS = 0x8D
STA_ZEROX = 0x95
STA_ABSX = 0x9D
STA_ABSY = 0x99
STA_INDX = 0x81
STA_INDY = 0x91

STX_ZERO = 0x86
STX_ABS = 0x8E
STX_ZEROY = 0x96

STY_ZERO = 0x84
STY_ABS = 0x8C
STY_ZEROX = 0x94

TXA = 0x8A
TYA = 0x98
TXS = 0x9A
TAY = 0xA8
TAX = 0xAA
TSX = 0xBA

PHP = 0x08
PLP = 0x28
PHA = 0x48
PLA = 0x68

ADC_IMM = 0x69
ADC_ZERO = 0x65
ADC_ABS = 0x6D
ADC_ZEROX = 0x75
ADC_ABSX = 0x7D
ADC_ABSY = 0x79
ADC_INDX = 0x61
ADC_INDY = 0x71

SBC_IMM = 0xE9
SBC_ZERO = 0xE5
SBC_ABS = 0xED
SBC_ZEROX = 0xF5
SBC_ABSX = 0xFD
SBC_ABSY = 0xF9
SBC_INDX = 0xE1
SBC_INDY = 0xF1

CPX_IMM = 0xE0
CPX_ZERO = 0xE4
CPX_ABS = 0xEC

CPY_IMM = 0xC0
CPY_ZERO = 0xC4
CPY_ABS = 0xCC

CMP_IMM = 0xC9
CMP_ZERO = 0xC5
CMP_ABS = 0xCD
CMP_ZEROX = 0xD5
CMP_ABSX = 0xDD
CMP_ABSY = 0xD9
CMP_INDX = 0xC1
CMP_INDY = 0xD1

AND_IMM = 0x29
AND_ZERO = 0x25
AND_ABS = 0x2D
AND_ZEROX = 0x35
AND_ABSX = 0x3D
AND_ABSY = 0x39
AND_INDX = 0x21
AND_INDY = 0x31

EOR_IMM = 0x49
EOR_ZERO = 0x45
EOR_ABS = 0x4D
EOR_ZEROX = 0x55
EOR_ABSX = 0x5D
EOR_ABSY = 0x59
EOR_INDX = 0x41
EOR_INDY = 0x51

ORA_IMM = 0x09
ORA_ZERO = 0x05
ORA_ABS = 0x0D
ORA_ZEROX = 0x15
ORA_ABSX = 0x1D
ORA_ABSY = 0x19
ORA_INDX = 0x01
ORA_INDY = 0x11

BIT_ZERO = 0x24
BIT_ABS = 0x2C

ASL = 0x0A
ASL_ZERO = 0x06
ASL_ABS = 0x0E
ASL_ZEROX = 0x16
ASL_ABSX = 0x1E

LSR = 0x4A
LSR_ZERO = 0x46
LSR_ABS = 0x4E
LSR_ZEROX = 0x56
LSR_ABSX = 0x5E

ROL = 0x2A
ROL_ZERO = 0x26
ROL_ABS = 0x2E
ROL_ZEROX = 0x36
ROL_ABSX = 0x3E

ROR = 0x6A
ROR_ZERO = 0x66
ROR_ABS = 0x6E
ROR_ZEROX = 0x76
ROR_ABSX = 0x7E

INX = 0xE8
INY = 0xC8

INC_ZERO = 0xE6
INC_ABS = 0xEE
INC_ZEROX = 0xF6
INC_ABSX = 0xFE

DEX = 0xCA
DEY = 0x88

DEC_ZERO = 0xC6
DEC_ABS = 0xCE
DEC_ZEROX = 0xD6
DEC_ABSX = 0xDE

CLC = 0x18
CLI = 0x58
CLV = 0xB8
CLD = 0xD8
SEC = 0x38
SEI = 0x78
SED = 0xF8

NOP = 0xEA
BRK = 0x00

JSR_ABS = 0x20
JMP_ABS = 0x4C
JMP_INDABS = 0x6C

RTI = 0x40
RTS = 0x60

BPL = 0x10
BMI = 0x30
BVC = 0x50
BVS = 0x70
BCC = 0x90
BCS = 0xB0
BNE = 0xD0
BEQ = 0xF0

Cycles = [
   7, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 4, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 6, 7,
   6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 4, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 6, 7,
   6, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 3, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 6, 7,
   6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 5, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 6, 7,
   2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
   2, 6, 2, 6, 4, 4, 4, 4, 2, 4, 2, 5, 5, 4, 5, 5,
   2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
   2, 5, 2, 5, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4,
   2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
   2, 6, 3, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
   2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
]

Mode = [
    'impl', 'xind', 'impl', 'impl', 'impl', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'accum', 'impl', 'impl', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absx', 'impl',
    'abs', 'xind', 'impl', 'impl', 'zpg', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'accum', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absx', 'impl',
    'impl', 'xind', 'impl', 'impl', 'impl', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'accum', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absx', 'impl',
    'impl', 'xind', 'impl', 'impl', 'impl', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'accum', 'impl', 'ind', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absx', 'impl',
    'impl', 'xind', 'impl', 'impl', 'zpg', 'zpg', 'zpg', 'impl', 'impl', 'impl', 'impl', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'zpgx', 'zpgx', 'zpgy', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'impl', 'impl',
    'immed', 'xind', 'immed', 'impl', 'zpg', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'impl', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'zpgx', 'zpgx', 'zpgy', 'impl', 'impl', 'absy', 'impl', 'impl', 'absx', 'absx', 'absy', 'impl',
    'immed', 'xind', 'immed', 'impl', 'zpg', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'impl', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absy', 'impl',
    'immed', 'xind', 'immed', 'impl', 'zpg', 'zpg', 'zpg', 'impl', 'impl', 'immed', 'impl', 'impl', 'abs', 'abs', 'abs', 'impl',
    'rel', 'indy', 'impl', 'impl', 'impl', 'zpgx', 'zpgx', 'impl', 'impl', 'absy', 'impl', 'impl', 'impl', 'absx', 'absy', 'impl',
]

Base = {
    "LDA": [0xA9, 0xA5, 0xAD, 0xB5, 0xBD, 0xB9, 0xA1, 0xB1],
    "LDX": [0xA2, 0xA6, 0xAE, 0xB6, 0xBE],
    "LDY": [0xA0, 0xA4, 0xAC, 0xB4, 0xBC],
    "STA": [0x85, 0x8D, 0x95, 0x9D, 0x99, 0x81, 0x91],
    "STX": [0x86, 0x8E, 0x96],
    "STY": [0x84, 0x8C, 0x94],
    "TXA": [0x8A],
    "TYA": [0x98],
    "TXS": [0x9A],
    "TAY": [0xA8],
    "TAX": [0xAA],
    "TSX": [0xBA],
    "PHP": [0x08],
    "PLP": [0x28],
    "PHA": [0x48],
    "PLA": [0x68],
    "ADC": [0x69, 0x65, 0x6D, 0x75, 0x7D, 0x79, 0x61, 0x71],
    "SBC": [0xE9, 0xE5, 0xED, 0xF5, 0xFD, 0xF9, 0xE1, 0xF1],
    "CPX": [0xE0, 0xE4, 0xEC],
    "CPY": [0xC0, 0xC4, 0xCC],
    "CMP": [0xC9, 0xC5, 0xCD, 0xD5, 0xDD, 0xD9, 0xC1, 0xD1],
    "AND": [0x29, 0x25, 0x2D, 0x35, 0x3D, 0x39, 0x21, 0x31],
    "EOR": [0x49, 0x45, 0x4D, 0x55, 0x5D, 0x59, 0x41, 0x51],
    "ORA": [0x09, 0x05, 0x0D, 0x15, 0x1D, 0x19, 0x01, 0x11],
    "BIT": [0x24, 0x2C],
    "ASL": [0x0A, 0x06, 0x0E, 0x16, 0x1E],
    "LSR": [0x4A, 0x46, 0x4E, 0x56, 0x5E],
    "ROL": [0x2A, 0x26, 0x2E, 0x36, 0x3E],
    "ROR": [0x6A, 0x66, 0x6E, 0x76, 0x7E],
    "INX": [0xE8],
    "INY": [0xC8],
    "INC": [0xE6, 0xEE, 0xF6, 0xFE],
    "DEX": [0xCA],
    "DEY": [0x88],
    "DEC": [0xC6, 0xCE, 0xD6, 0xDE],
    "CLC": [0x18],
    "CLI": [0x58],
    "CLV": [0xB8],
    "CLD": [0xD8],
    "SEC": [0x38],
    "SEI": [0x78],
    "SED": [0xF8],
    "NOP": [
        0xEA, 0x1A, 0x3A, 0x5A, 0x7A, 0xDA, 0xFA, 0x02, 0x12, 0x22, 0x32, 0x42,
        0x52, 0x62, 0x72, 0x92, 0xB2, 0xD2, 0xF2, 0x80, 0x82, 0x89, 0xC2, 0xE2,
        0x04, 0x44, 0x64, 0x14, 0x34, 0x54, 0x74, 0xD4, 0xF4, 0x0C, 0x1C, 0x3C,
        0x5C, 0x7C, 0xDC, 0xFC
        ],
    "BRK": [0x00],
    "JSR": [0x20],
    "JMP": [0x4C, 0x6C],
    "RTI": [0x40],
    "RTS": [0x60],
    "BPL": [0x10],
    "BMI": [0x30],
    "BVC": [0x50],
    "BVS": [0x70],
    "BCC": [0x90],
    "BCS": [0xB0],
    "BNE": [0xD0],
    "BEQ": [0xF0]
}
