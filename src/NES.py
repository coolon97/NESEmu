import cpu
import rom
import ram
import nesio
import ppu
import apu
import bus
import pygame
import sys


class NES:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.io = nesio.NesIO()
        self.ram = ram.RAM()
        self.ppu = ppu.PPU()
        self.apu = apu.APU()
        self.rom = False
        self.cpu = False

    def load(self, data):
        self.rom = rom.ROM(data)
        
    def start(self):
        self.bus = bus.BUS(self.ram, self.rom, self.ppu, self.apu, self.io)
        self.cpu = cpu.CPU(self.bus)
        self.cpu.start()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((320, 240))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("test")

    bg = pygame.image.load("../assets/test.png").convert_alpha()
    rect = bg.get_rect()

    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
