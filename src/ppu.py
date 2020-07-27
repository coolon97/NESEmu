"""
  // PPU power up state
  // see. https://wiki.nesdev.com/w/index.php/PPU_power_up_state
  //
  // Memory map
  /*
  | addr           |  description               |
  +----------------+----------------------------+
  | 0x0000-0x0FFF  |  Pattern table#0           |
  | 0x1000-0x1FFF  |  Pattern table#1           |
  | 0x2000-0x23BF  |  Name table                |
  | 0x23C0-0x23FF  |  Attribute table           |
  | 0x2400-0x27BF  |  Name table                |
  | 0x27C0-0x27FF  |  Attribute table           |
  | 0x2800-0x2BBF  |  Name table                |
  | 0x2BC0-0x2BFF  |  Attribute table           |
  | 0x2C00-0x2FBF  |  Name Table                |
  | 0x2FC0-0x2FFF  |  Attribute Table           |
  | 0x3000-0x3EFF  |  mirror of 0x2000-0x2EFF   |
  | 0x3F00-0x3F0F  |  background Palette        |
  | 0x3F10-0x3F1F  |  sprite Palette            |
  | 0x3F20-0x3FFF  |  mirror of 0x3F00-0x3F1F   |
  */

  /*
    Control Register1 0x2000
  | bit  | description                                 |
  +------+---------------------------------------------+
  |  7   | Assert NMI when VBlank 0: disable, 1:enable |
  |  6   | PPU master/slave, always 1                  |
  |  5   | Sprite size 0: 8x8, 1: 8x16                 |
  |  4   | Bg pattern table 0:0x0000, 1:0x1000         |
  |  3   | sprite pattern table 0:0x0000, 1:0x1000     |
  |  2   | PPU memory increment 0: +=1, 1:+=32         |
  |  1-0 | Name table 0x00: 0x2000                     |
  |      |            0x01: 0x2400                     |
  |      |            0x02: 0x2800                     |
  |      |            0x03: 0x2C00                     |
  */

  /*
    Control Register2 0x2001
  | bit  | description                                 |
  +------+---------------------------------------------+
  |  7-5 | Background color  0x00: Black               |
  |      |                   0x01: Green               |
  |      |                   0x02: Blue                |
  |      |                   0x04: Red                 |
  |  4   | Enable sprite                               |
  |  3   | Enable background                           |
  |  2   | Sprite mask       render left end           |
  |  1   | Background mask   render left end           |
  |  0   | Display type      0: color, 1: mono         |
  */
"""
#import numpy as np


COLORS = [
    [0x80, 0x80, 0x80], [0x00, 0x3D, 0xA6], [0x00, 0x12, 0xB0], [0x44, 0x00, 0x96],
    [0xA1, 0x00, 0x5E], [0xC7, 0x00, 0x28], [0xBA, 0x06, 0x00], [0x8C, 0x17, 0x00],
    [0x5C, 0x2F, 0x00], [0x10, 0x45, 0x00], [0x05, 0x4A, 0x00], [0x00, 0x47, 0x2E],
    [0x00, 0x41, 0x66], [0x00, 0x00, 0x00], [0x05, 0x05, 0x05], [0x05, 0x05, 0x05],
    [0xC7, 0xC7, 0xC7], [0x00, 0x77, 0xFF], [0x21, 0x55, 0xFF], [0x82, 0x37, 0xFA],
    [0xEB, 0x2F, 0xB5], [0xFF, 0x29, 0x50], [0xFF, 0x22, 0x00], [0xD6, 0x32, 0x00],
    [0xC4, 0x62, 0x00], [0x35, 0x80, 0x00], [0x05, 0x8F, 0x00], [0x00, 0x8A, 0x55],
    [0x00, 0x99, 0xCC], [0x21, 0x21, 0x21], [0x09, 0x09, 0x09], [0x09, 0x09, 0x09],
    [0xFF, 0xFF, 0xFF], [0x0F, 0xD7, 0xFF], [0x69, 0xA2, 0xFF], [0xD4, 0x80, 0xFF],
    [0xFF, 0x45, 0xF3], [0xFF, 0x61, 0x8B], [0xFF, 0x88, 0x33], [0xFF, 0x9C, 0x12],
    [0xFA, 0xBC, 0x20], [0x9F, 0xE3, 0x0E], [0x2B, 0xF0, 0x35], [0x0C, 0xF0, 0xA4],
    [0x05, 0xFB, 0xFF], [0x5E, 0x5E, 0x5E], [0x0D, 0x0D, 0x0D], [0x0D, 0x0D, 0x0D],
    [0xFF, 0xFF, 0xFF], [0xA6, 0xFC, 0xFF], [0xB3, 0xEC, 0xFF], [0xDA, 0xAB, 0xEB],
    [0xFF, 0xA8, 0xF9], [0xFF, 0xAB, 0xB3], [0xFF, 0xD2, 0xB0], [0xFF, 0xEF, 0xA6],
    [0xFF, 0xF7, 0x9C], [0xD7, 0xE8, 0x95], [0xA6, 0xED, 0xAF], [0xA2, 0xF2, 0xDA],
    [0x99, 0xFF, 0xFC], [0xDD, 0xDD, 0xDD], [0x11, 0x11, 0x11], [0x11, 0x11, 0x11],
]


class PPU:            
    def __init__(self, characterRom):
        self.characterRom = characterRom
        self.reset()

    def reset(self):
        self.registers = {
                "PPUCTRL": 0x40,
                "PPUMASK": 0x10,
                "PPUSTATUS": 0x00,
                "OAMADDR": 0x00,
                "OMADATA": 0x00,
                "PPUSCROLL": 0x00,
                "PPUADDR": 0x00,
                "PPUDATA": 0x00
        }
        self.cycles = 0
        self.line = 0
        self.iobuf = 0x00
        self.vram = [0]*0xFFFF
        #self.background = np.zeros((240 ,256, 3)).astype(np.uint8)
        self.fps = 0

    def read(self, addr):
        if addr==0x06:
            return self.vram[self.iobuf]
        return list(self.registers.values())[addr]

    def write(self, addr, data):
        if addr==0x06:
            self.iobuf = ((self.iobuf << 8) + data) & 0xFFFF
            if data!=0x00:
                self.vram[self.iobuf] = data
            return 
        list(self.registers.values())[addr % 8] = bool(data)

    def run(self, cycle):
        self.cycles += cycle
        if self.cycles >= 341:
            self.cycles -= 341
            self.line += 1

            if self.line == 262:
                self.line = 0
                self.fps += 1
                if self.fps >= 60:
                    import png
                    p = png.Png()
                    p.write_binary(self.buildBackground(), 256, 240)
                    exit()
                return self.buildBackground()

        return None

    def buildSprite(self, spriteId):
        sprite = np.zeros((8,8)).astype(np.uint8)
        for i in range(16):
            for j in range(8):
                addr = spriteId * 16 + i
                rom = self.readCharacterROM(addr)
                if bool(rom & (0x80 >> j)):
                    sprite[i % 8:j] += 0x01 << ~~(i / 8)

        return sprite

    def buildBackground(self):
        for i in range(0, 240, 16):
            for j in range(0, 256, 16):
                self.background[i:i+16, j:j+16] = self.buildTile(i, j)

    def buildTile(self, tileX, tileY):
        tile = np.zeros((16,16,3)).astype(np.uint8)
        for i in range(4):
            spriteId = self.getSpriteId(tileX, tileY)
            attr = self.getAttribute(tileX, tileY)
            paletteId = (attr >> (i * 2)) & 0x03
            sprite = self.buildSprite(spriteId) 
            tile[i%2*8:(i%2+1)*8, i//2*8:(i//2+1)*8] = self.applyPalette(sprite, paletteId)
        return tile
    
    def getSpriteId(self, x, y):
        return self.vram[0x2000 + y*0x20 + x]
    
    def getAttribute(self, x, y):
        return self.vram[0x23C0 + y//16*8 + x//16]

    def getPalette(self, paletteId):
        return self.vram[0x3F00+0x04*paletteId:0x3F00+0x04*paletteId+0x04]

    def applyPalette(self, sprite, paletteId):
        palette = self.getPalette(paletteId)
        applied = np.zeros((8,8,3)).astype(np.uint8)
        for i in range(8):
            for j in range(8):
                applied[i, j] = COLORS[palette[sprite[i, j]]]
        return applied

    def readCharacterROM(self, addr):
        return self.characterRom[addr]
