import pygame
import os

WIDTH,HEIGTH = 50,50

CELLANONTROVATA = 0
MINA = 1
SICURA = 2


class cell:
    def __init__(self, row, col):
        pygame.font.init()
        self.font = pygame.font.SysFont(None,32)
        self.row = row
        self.col = col

        self.rect = pygame.Rect(
            col*WIDTH,
            row*HEIGTH+50,
            WIDTH,
            HEIGTH
        )
        self.active = False
        self.type = 0
        self.number=0
        self.active = False
        self.isWithFlag = False
        self.lose = False

    def disegnaNumero(self,screen):
        if self.number == 0:return

        testo = self.font.render(str(self.number), True, (0,0,0))
        testoRect = testo.get_rect()

        testoRect.center = (
            self.col * HEIGTH + HEIGTH // 2,
           ( self.row * HEIGTH + HEIGTH // 2)+50
        )
        screen.blit(testo, testoRect)

    def disegnaBandierina(self,screen):

        flag = pygame.image.load("assets/flag.png").convert_alpha()
        flagimg = pygame.transform.scale(flag, (30,30))
        flagRect = flagimg.get_rect()

        flagRect.center = (
            self.col * HEIGTH + HEIGTH//2,
           ( self.row * WIDTH+WIDTH//2)+50
        )

        screen.blit(flagimg, flagRect)

    def disegnaBomba(self,screen):

        bomb = pygame.image.load("assets/bomb.png").convert_alpha()
        bombimg = pygame.transform.scale(bomb, (30,30))
        bombRect = bombimg.get_rect()

        bombRect.center = (
            self.col * HEIGTH + HEIGTH//2,
           ( self.row * WIDTH+WIDTH//2)+50
        )

        screen.blit(bombimg, bombRect)


    def draw(self, screen):

        if not self.active:
            pygame.draw.rect(screen, (128,128,128), self.rect)
        else:
            pygame.draw.rect(screen, (255,255,255), self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
        if self.type == 0 and self.active and not self.isWithFlag:
            self.disegnaNumero(screen)
        if self.isWithFlag and not self.active:
            self.disegnaBandierina(screen)
        if self.lose and self.type==1:
            self.disegnaBomba(screen)






    def left_click(self, pos):
        if self.rect.collidepoint(pos) and not self.isWithFlag:
            print(f"Cella premuta: {self.row}:{self.col} tipo: {self.type}")
            if self.type!=1:
                self.active = True
            else:
                self.lose = True
    def right_click(self, pos)->bool:
        if self.rect.collidepoint(pos) and not self.active and not self.isWithFlag:
            self.isWithFlag = True
            return True
        return False


    def centre_click(self, pos) -> bool:
        if self.rect.collidepoint(pos) and self.isWithFlag:
            self.isWithFlag = False
            return True
        return False

    def __str__(self)->str:
        return f"Col: {self.col}\t Row: {self.row}"




