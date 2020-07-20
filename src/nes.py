import cpu
import rom
import ram
import nesio
import ppu
import apu
import bus
#from PySide2 import QtCore, QtGui, QtWidgets
#from PySide2.QtUiTools import QUiLoader
import sys
import time


class NES:
    def __init__(self):
        self.reset()

    def reset(self):
        self.io = nesio.NesIO()
        self.ram = ram.RAM()
        self.apu = apu.APU()
        self.rom = False
        self.cpu = False
        self.cycles = 0

    def load(self, data):
        self.rom = rom.ROM(data[0])
        self.ppu = ppu.PPU(data[1])

    def start(self):
        self.bus = bus.BUS(self.ram, self.rom, self.ppu, self.apu, self.io)
        self.cpu = cpu.CPU(self.bus)

        while(True):
            self.cycles = self.cpu.run()
            background = self.ppu.run(self.cycles * 3)
            if background is not None:
                print("OK!")

    def debug(self):
        def printRegister():
            print("RegisterA: " + str(self.cpu.registers.A))
            print("RegisterX: "+ str(self.cpu.registers.X))
            print("RegisterY: "+ str(self.cpu.registers.Y))
            print("RegisterS: "+ str(self.cpu.registers.S))
            print("RegisterP: "+ str(self.cpu.registers.P))
            print("RegisterPC: "+str(self.cpu.registers.PC)+"\n")

        self.bus = bus.BUS(self.ram, self.rom, self.ppu, self.apu, self.io)
        self.cpu = cpu.CPU(self.bus)

        msg = ''
        while(True):
            argv = input("(debug) cmd: ").split(" ")
            argc = len(argv)

            if argv[0] == "run":
                if argc>1:
                    for i in range(int(argv[1])):
                        msg = self.cpu.run()
                    print(msg)
                    printRegister()
                else:
                    msg = self.cpu.run()
                    print(msg)
                    printRegister()
                    
            if argv[0] == "register":
                printRegister()

            if argv[0] == "quit":
                exit()
            



'''
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((320, 240))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("test")

    bg = pygame.image.load("../assets/test.png")
    rect = bg.get_rect()

    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
'''

'''
class UISmaple(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UISmaple, self).__init__(parent)
        self.img1 = QtGui.QImage('../assets/test.png')
        self.img2 = QtGui.QImage('../assets/test.jpg')
        self.png = QtGui.QPixmap.fromImage(self.img1)
        self.one = 'one'
        self.resize(640, 480)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.png)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def flip(self):
        if self.one == 'one':
            self.one = 'two'
            self.png = QtGui.QPixmap.fromImage(self.img2)

        else:
            self.one = 'one'
            self.png = QtGui.QPixmap.fromImage(self.img1)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = UISmaple()
    a.show()
    sys.exit(app.exec_())
'''