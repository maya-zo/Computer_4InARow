import numpy as np
import pygame
from copy import deepcopy
N = 6
M = 7
COMP = 1
PLAYER = -1





class Board:
    def __init__(self, matrix = np.zeros((N,M) ,dtype=int) ):
        self.matrix = matrix
        self.Highest = np.full(M,N-1,dtype=int)
        self.isFinished = 0


    def updateFinished(self,col):
        if self.isFinished==0:
            player=self.matrix[self.Highest[col]+1][col]
            for a, b in [[0, 1], [1, 1], [-1, 0], [-1, 1]]:
                count=0
                plus=0
                minus=1
                stop = False
                while (not stop) and count!=4:
                    stop = True
                    if (self.Highest[col]+1 + a*plus)<N and (self.Highest[col]+1 + a*plus)>=0 and (col + b*plus)<M and (col + b*plus)>=0:
                        if self.matrix[self.Highest[col]+1 + a*plus][col + b*plus]==player:
                            count+=1
                            plus+=1
                            stop = False
                    if (self.Highest[col]+1 - a*minus)>=0 and (self.Highest[col]+1 - a*minus)<N and (col - b*minus)>=0 and (col - b*minus)<M:
                        if self.matrix[self.Highest[col]+1 - a*minus][col - b*minus]==player:
                            count += 1
                            minus += 1
                            stop = False

                if count==4:
                    self.isFinished = player
                    return

            x=0
            for i in range(M):
                if self.Highest[i]<0:
                    x+=1
            if x==M:
                self.isFinished = 2
                return


    def Operation(self, col, player):
        if col< 0 or col >=M:
            return False
        if self.Highest[col] < 0 or self.Highest[col] >= N:
            return False
        self.matrix[self.Highest[col]][col]=player
        self.Highest[col]-=1
        self.updateFinished(col)
        return True



    def checkStatus(self):
        return self.isFinished



class BoardNode:
    def __init__(self,Turn=COMP,Board=Board(),Father=None):
        self.board = Board
        self.father = Father
        self.turn = Turn

    # out of bound case
    def h(self):
        if self.board.checkStatus()!=0:
            if self.board.checkStatus()!=2:
                return self.board.checkStatus()*100000000
            else:
                return 0
        else:
            count = 0
            for i in range(N):
                for j in range(M):
                    for a, b in [[0, 1], [1, 1], [-1, 0], [-1, 1]]:
                        sum = 0
                        zeroes = 0

                        for y in range(4):
                            if i+a*y<N and i+a*y>=0 and j+b*y<M and j+b*y>=0:
                                sum += self.board.matrix[i+a*y][j+b*y]
                                if self.board.matrix[i+a*y][j+b*y]==0:
                                    zeroes+=1
                            else:
                                sum=0
                                zeroes = 0


                            if abs(sum) + zeroes == 4:
                                count+=sum

            return count



    def getSons(self):
        l=[]
        for i in range(M):
            x=deepcopy(self)
            x.father=self
            x.turn=self.turn*(-1)
            if x.board.Operation(i,self.turn):
                l.append(x)

        return l

def minmax(boardNode,d=4):
    if d==0  or boardNode.board.checkStatus()!=0:
        return boardNode.h(), boardNode
    x=boardNode.getSons()
    BoardOp=0
    if boardNode.turn==1:
        currMax = -100000000
        for i in x:
            v = minmax(i,d - 1)[0]
            if v>currMax or currMax == -100000000 :
                currMax = v
                BoardOp = i
        return currMax, BoardOp
    else:
        currMin = 1000000000
        for i in x:
            v = minmax(i, d - 1)[0]
            if v < currMin or currMin == 1000000000:
                currMin = v
                BoardOp = i
        return currMin, BoardOp

WINDOW_WIDTH=M*100
WINDOW_HEIGHT=N*100
LEFT = 1

pygame.init()
size=(WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
BLUE = (0,0,205)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

screen.fill(BLUE)
pygame.display.flip()

#text
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS',20)

def columnCalc(posX):
    return int(posX/100)



def drawBoard(BoardNode):
    screen.fill(BLUE)
    pygame.display.flip()
    for i in range(N):
        for j in range(M):
            colour = BLACK
            if BoardNode.board.matrix[i][j]==1:
                colour = RED
            elif BoardNode.board.matrix[i][j]==-1:
                colour = YELLOW
            pygame.draw.circle(screen, colour, [50+ 100*(j),50+ 100*(i)], 45)
    pygame.display.update()

textWelcome = myfont.render("Hello and welcome to Connect4! Are you ready to play??", True, WHITE)
screen.blit(textWelcome,(90,100))

pygame.display.update()

pygame.draw.rect(screen, WHITE, [[100,200],[200,150]])
youStart = myfont.render("You Start", True, BLACK)
screen.blit(youStart,(150,250))

pygame.draw.rect(screen, WHITE, [[400,200],[200,150]])
compStart = myfont.render("Computer Starts", True, BLACK)
screen.blit(compStart,(420,250))

pygame.display.update()

i=0
finish = False
pressed = False
while not pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            pressed = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            if pygame.mouse.get_pos()[0] < 300 and pygame.mouse.get_pos()[0] > 100 and pygame.mouse.get_pos()[1] < 350 and pygame.mouse.get_pos()[1] > 200 :
                i=-1
                finish = False
                pressed = True
            elif pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[0] > 400 and pygame.mouse.get_pos()[1] < 350 and pygame.mouse.get_pos()[1] > 200 :
                i=1
                finish = False
                pressed = True

b = BoardNode(i)
drawBoard(b)

while(b.board.checkStatus()==0):
    drawBoard(b)
    if b.turn == -1:
        x=True
        while x:
            pressed = False
            while not pressed:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                        i = columnCalc(pygame.mouse.get_pos()[0])
                        pressed = True
            bounds = b.board.Operation(i,b.turn)
            if bounds==False:
                outBound = myfont.render("Out of Bounds!", True, WHITE)
                screen.blit(outBound, (280, 280))
                pygame.display.update()
            else:
                b.turn *= -1
                x=False
    elif b.turn == 1:
        b = minmax(b)[1]
drawBoard(b)
if b.board.checkStatus()==1:
    Lose = myfont.render("You Lose!", True, WHITE)
    screen.blit(Lose, (300, 280))
    pygame.display.update()

elif b.board.checkStatus()==-1:
    Win = myfont.render("You Win!", True, WHITE)
    screen.blit(Win, (300, 280))
    pygame.display.update()
else:
    Draw = myfont.render("It's a Draw!", True, WHITE)
    screen.blit(Draw, (280, 280))
    pygame.display.update()
pygame.time.wait(3000)



