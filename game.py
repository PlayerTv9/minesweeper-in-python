import pygame
import sys
import random
import time

from cell import cell

ROWS,COLS = 10,10
NUM_MINE = 20

WIDTH_C,HEIGTH_C = 50,50



class game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None,32)
        self.font2 = pygame.font.SysFont(None,80)

        self.WIDTH,self.HEIGHT = 500, 550
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Minesweeper!")

        self.clock = pygame.time.Clock()

        self.Running = True
        self.gameover = False

        self.griglia:list[cell] = []
        self.spawnCella()
        self.numMinesDisp = NUM_MINE

        self.win = False
        self.startTime = 0.0
        self.time = 0
        self.mTime = 0
        self.sTime = 0

        self.startGame = False
        self.timeStarted = False




    def updateTime(self):
        if self.startGame and not self.timeStarted:
            self.startTime = time.time()
            self.timeStarted = True

        if self.timeStarted:
            self.time = int(time.time()-self.startTime)
            self.mTime = self.time//60
            self.sTime = self.time%60



    def spawnCella(self):
        for row in range(ROWS):
            for col in range(COLS):

                self.griglia.append(cell(row,col))

        posizioni = random.sample(range(ROWS*COLS), NUM_MINE)

        for index in posizioni:
            self.griglia[index].type = 1

        for cella in self.griglia:
            numAMine = 0
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    if dx==0 and dy==0:continue

                    nx = cella.row+dx
                    ny = cella.col+dy
                    if 0<=nx<ROWS and 0<=ny<COLS:
                        index = nx*COLS + ny
                        if self.griglia[index].type == 1:
                            numAMine+=1

            cella.number = numAMine
            for x in self.griglia:
                print(x)



    def timeText(self):
        testo = self.font.render(f"{self.mTime:02d}:{self.sTime:02d}", True, (0,0,0))
        testoRect = testo.get_rect()
        testoRect.center = (
            450,
            25
        )
        self.screen.blit(testo, testoRect)
    def bandierina(self):
        flag = pygame.image.load("assets/flag.png").convert_alpha()
        flagimg = pygame.transform.scale(flag, (50,50))
        flagRect = flagimg.get_rect()

        flagRect.center = (
           self.WIDTH//2-25,
           25
        )

        self.screen.blit(flagimg, flagRect)

    def text(self):
        testo = self.font.render(f"x{self.numMinesDisp}", True, (0,0,0))
        testoRect = testo.get_rect()
        testoRect.center = (
            self.WIDTH//2+25,
            25
        )
        self.screen.blit(testo, testoRect)

    def winText(self):
        testo = self.font2.render("You win!", True, (0, 153, 0))
        rect = testo.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.screen.blit(testo, rect)

    def loseText(self):
        testo = self.font2.render("You lose!", True, (153, 0, 0))
        rect = testo.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.screen.blit(testo, rect)


    def aggiornamentoGriglia(self):

         for cella in self.griglia:
            for dx in (-1,1):
                nx = cella.row+dx
                if 0<=nx<ROWS:
                    index = nx*COLS+cella.col
                    if self.griglia[index].active and cella.type!=1:
                        cella.active = True
            for dy in (-1,1):
                ny = cella.col+dy
                if 0<=ny<COLS:
                    index = cella.row*COLS + ny
                    if self.griglia[index].active and cella.type!=1 and cella.number<=0:
                        cella.active = True

    def goGameover(self):
        for cella in self.griglia:
            if cella.lose:
                self.gameover = True

        if self.gameover:
            for cella in self.griglia:
                cella.lose = True

    def update(self):
        self.aggiornamentoGriglia()
        self.goGameover()
        self.updateTime()





    def draw(self):
        self.screen.fill((255,255,255))
        for cell in self.griglia:
            cell.draw(self.screen)
        self.bandierina()
        self.text()
        if self.win:
            self.winText()
        if self.gameover:
            self.loseText()
        self.timeText()

            #if cell.type == 0 and cell.number>0:
                #self.disegnaNumero(cell.number, cell.row, cell.col)


    def reloadGameEvent(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.win = False
            self.gameover = False
            self.griglia.clear()
            self.numMinesDisp = NUM_MINE
            self.spawnCella()
            self.time = 0
            self.mTime = 0
            self.sTime = 0
            self.startTime = 0.0
            self.startGame = False
            self.timeStarted = False



    def keyboardEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.gameover and not self.win:

                if event.button == 1:
                    self.startGame = True
                    for cell in self.griglia:
                        cell.left_click(event.pos)
                elif event.button == 3 and self.numMinesDisp>0:
                    self.startGame = True
                    for cell in self.griglia:
                        if cell.right_click(event.pos) :
                            self.numMinesDisp-=1

                    print(f"Bandiere ora disponibili: {self.numMinesDisp}")
                elif event.button == 2:
                    self.startGame = True
                    for cell in self.griglia:
                        if cell.centre_click(event.pos):
                            self.numMinesDisp+=1

                    print(f"Bandiere ora disponibili: {self.numMinesDisp}")
                self.winTheGame()

    '''def disegnaNumero(self,n,row,col):
        if n==0:return

        testo = self.font.render(str(n), True, (0,0,0))
        rect = testo.get_rect()

        rect.center = (
            col * HEIGTH_C + HEIGTH_C // 2,
            row * HEIGTH_C + HEIGTH_C // 2
        )

        self.screen.blit(testo, rect)'''

    def winTheGame(self):
        numTrueFlag = 0
        for cella in self.griglia:
            if cella.type==1 and cella.isWithFlag:
                numTrueFlag+=1
        if numTrueFlag==NUM_MINE:
            print("You win!")
            self.win = True
    def run(self):
        while self.Running:
            if not self.gameover and not self.win:
                self.update()

            self.draw()
            self.reloadGameEvent()
            pygame.display.flip()
            self.clock.tick(60)

            self.keyboardEvent()

        pygame.quit()
        sys.exit()
