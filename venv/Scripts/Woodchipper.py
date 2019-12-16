import pygame, sys, random, time
from pygame.locals import *
pygame.init()
# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 9  # number of columns in the board
BOARDHEIGHT = 9 # number of rows in the board
TILESIZE = 100
WINDOWWIDTH = 900
WINDOWHEIGHT = 1000
BOARDERSIZE = 5
FPS = 60
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
DARKGREY =      ( 64,  64,  64)
GREY =          (178, 178, 178)
BLUE =          ( 64,  64, 255)
LIGHTBLUE =     (178, 178, 255)
GREYTAN =       (178, 166, 153)


FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASICFONTSIZE = 40
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
ENDFONTSIZE = 100
ENDFONT = pygame.font.Font('freesansbold.ttf', ENDFONTSIZE)
SMALLENDFONTSIZE = 75
SMALLENDFONT = pygame.font.Font('freesansbold.ttf', SMALLENDFONTSIZE)
WATER = "water"
ICE = "ice"
WALL = "wall"
FLOOR = "floor"
SAD = "sad"
HAPPY = "happy"
LIMBURGER = "limburger"
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
gameBoard = []
blockList = []
enemyList = []
startX = -1
startY = -1
blkSurf = pygame.Surface((WINDOWWIDTH, 100))
blkSurf.fill(BLACK)
iceSpikes = pygame.transform.scale(pygame.image.load("iceSpikes.png"),(95,95))
inventorySpikes = pygame.transform.scale(pygame.image.load("iceSpikes.png"),(45,45))
key = pygame.transform.scale(pygame.image.load("key.png"),(95,95))
inventoryKey = pygame.transform.scale(pygame.image.load("key.png"),(45,45))
doorImg = pygame.transform.scale(pygame.image.load("door.png"),(95,95))
happyImg = pygame.transform.scale(pygame.image.load("happy.jfif"),(95,95))
sadImg = pygame.transform.scale(pygame.image.load("sad.png"),(95,95))
flippers = pygame.transform.scale(pygame.image.load("flippers.png"),(95,95))
inventoryFlippers = pygame.transform.scale(pygame.image.load("flippers.png"),(45,45))
chipImg = pygame.transform.scale(pygame.image.load("chip.png"),(95,95))
monsterImg = pygame.transform.scale(pygame.image.load("monster.png"),(95,95))
winImg = pygame.transform.scale(pygame.image.load("win.png"),(95,95))
hintImg = pygame.transform.scale(pygame.image.load("hint.png"),(95,95))
limburgerImg = pygame.transform.scale(pygame.image.load("limburger.png"),(95,95))
LEVEL1TIME = 200
SCORE = 0
hint1 = "The block will bridge the gap"
hint2 = "Run!"
levelindex = 0
levelArray = ["board1.txt", "board2.txt"]

class Tile:

    def __init__(self, _basetile, _hasblock, _hasflippers, _hasspikes, _haskey, _isdoor, _ishint, _iswin):
        self.tileSurf = pygame.Surface((95, 95))
        self.iswater = False
        self.isice = False
        self.iswall = False
        self.isfloor = False
        self.issad = False
        self.ishappy = False
        self.islimburger = False
        if _basetile == WATER:
            self.iswater = True
        elif _basetile == ICE:
            self.isice = True
        elif _basetile == WALL:
            self.iswall = True
        elif _basetile == FLOOR:
            self.isfloor = True
        elif _basetile == SAD:
            self.issad = True
        elif _basetile == HAPPY:
            self.ishappy = True
        elif _basetile == LIMBURGER:
            self.islimburger = True
        self.hasblock = _hasblock
        self.tileBlock = None
        self.hasflippers = _hasflippers
        self.hasspikes = _hasspikes
        self.haskey = _haskey
        self.isdoor = _isdoor
        self.ishint = _ishint
        self.iswin = _iswin
        self.drawBaseTile()
        


    def drawBaseTile(self):
        if self.iswater:
            self.tileSurf.fill(BLUE)
        elif self.isice:
            self.tileSurf.fill(LIGHTBLUE)
        elif self.iswall:
            self.tileSurf.fill(DARKGREY)
        elif self.isfloor:
            self.tileSurf.fill(GREY)
        elif self.issad:
            self.tileSurf.fill(GREY)
            self.tileSurf.blit(sadImg, (0,0))
        elif self.ishappy:
            self.tileSurf.blit(happyImg, (0,0))
        elif self.islimburger:
            self.tileSurf.fill(GREY)
            self.tileSurf.blit(limburgerImg, (0,0))
        if self.hasblock:
            self.tileSurf.fill(GREYTAN)
        elif self.haskey:
            self.tileSurf.blit(key, (0, 0))
        elif self.hasflippers:
            self.tileSurf.fill(GREY)
            self.tileSurf.blit(flippers, (0,0))
        elif self.hasspikes:
            self.tileSurf.blit(iceSpikes, (0,0))
        elif self.isdoor:
            self.tileSurf.blit(doorImg, (0,0))
        if self.iswin:
            self.tileSurf.blit(winImg, (0,0))
        elif self.ishint:
            self.tileSurf.blit(hintImg, (0,0))

def displayHint():
    if gameBoard[chip.xpos][chip.ypos].ishint:
        if( levelindex == 0):
            hintSurf = BASICFONT.render(hint1, True, WHITE, BLACK)
            DISPLAYSURF.blit(hintSurf, (250, 400))
        if(levelindex == 1):
            hintSurf = BASICFONT.render(hint2, True, WHITE, BLACK)
            DISPLAYSURF.blit(hintSurf, (300, 400))
            
            
            
        
            



class Player:

    def __init__(self):
        self.ypos = -1
        self.xpos = -1
        self.numKeys = 0
        self.hasFlippers = False
        self.hasSpikes = False
        self.isSad = False
        self.isSlipping = False
        self.isdead = False
        self.haswon = False

    def canMove(self, direct):
        if (direct == LEFT):
            if self.xpos > 0:
                if gameBoard[self.xpos-1][self.ypos].isfloor or gameBoard[self.xpos-1][self.ypos].islimburger:
                    self.isSlipping = False
                    if gameBoard[self.xpos-1][self.ypos].isdoor and self.numKeys > 0:
                        self.numKeys -=1
                        gameBoard[self.xpos-1][self.ypos].isdoor = False
                        return True
                    elif gameBoard[self.xpos-1][self.ypos].isdoor:
                        return False
                    if gameBoard[self.xpos-1][self.ypos].iswin:
                        self.haswon = True
                        return True
                    if gameBoard[self.xpos-1][self.ypos].hasblock:
                        if gameBoard[self.xpos-1][self.ypos].tileBlock.willMove(direct):
                            return True
                        return False
                    return True
                elif gameBoard[self.xpos-1][self.ypos].isice:
                    if self.hasSpikes:
                        self.isSlipping = False
                    else:
                        self.isSlipping = True
                    return True
                elif gameBoard[self.xpos-1][self.ypos].issad:
                    self.isSad = True
                    return True
                elif gameBoard[self.xpos-1][self.ypos].ishappy:
                    self.isSad = False
                    return True
                elif gameBoard[self.xpos-1][self.ypos].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos - 1][self.ypos].iswater:
                    if not self.hasFlippers:
                        self.isdead = True
                    return True
        elif (direct == RIGHT):
            if self.xpos < len(gameBoard) - 1:
                if gameBoard[self.xpos+1][self.ypos].isfloor or gameBoard[self.xpos+1][self.ypos].islimburger:
                    self.isSlipping = False
                    if gameBoard[self.xpos+1][self.ypos].isdoor and self.numKeys > 0:
                        self.numKeys -=1
                        gameBoard[self.xpos+1][self.ypos].isdoor = False
                        return True
                    elif gameBoard[self.xpos+1][self.ypos].isdoor:
                        return False
                    if gameBoard[self.xpos+1][self.ypos].iswin:
                        self.haswon = True
                        return True
                    if gameBoard[self.xpos+1][self.ypos].hasblock:
                        if gameBoard[self.xpos+1][self.ypos].tileBlock.willMove(direct):
                            return True
                        return False
                    return True
                elif gameBoard[self.xpos+1][self.ypos].isice:
                    if self.hasSpikes:
                        self.isSlipping = False
                    else:
                        self.isSlipping = True
                    return True
                elif gameBoard[self.xpos+1][self.ypos].issad:
                    self.isSad = True
                    return True
                elif gameBoard[self.xpos+1][self.ypos].ishappy:
                    self.isSad = False
                    return True
                elif gameBoard[self.xpos+1][self.ypos].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos + 1][self.ypos].iswater:
                    if not self.hasFlippers:
                        chip.isdead = True
                    return True
        elif (direct == UP):
            if self.ypos > 0:
                if gameBoard[self.xpos][self.ypos-1].isfloor or gameBoard[self.xpos][self.ypos-1].islimburger:
                    self.isSlipping = False
                    if gameBoard[self.xpos][self.ypos-1].isdoor and self.numKeys > 0:
                        self.numKeys -=1
                        gameBoard[self.xpos][self.ypos-1].isdoor = False
                        return True
                    elif gameBoard[self.xpos][self.ypos-1].isdoor:
                        return False
                    if gameBoard[self.xpos][self.ypos-1].iswin:
                        self.haswon = True
                        return True
                    if gameBoard[self.xpos][self.ypos-1].hasblock:
                        if gameBoard[self.xpos][self.ypos-1].tileBlock.willMove(direct):
                            return True
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos-1].isice:
                    if self.hasSpikes:
                        self.isSlipping = False
                    else:
                        self.isSlipping = True
                    return True
                elif gameBoard[self.xpos][self.ypos-1].issad:
                    self.isSad = True
                    return True
                elif gameBoard[self.xpos][self.ypos-1].ishappy:
                    self.isSad = False
                    return True
                elif gameBoard[self.xpos][self.ypos-1].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos][self.ypos-1].iswater:
                    if not self.hasFlippers:
                        chip.isdead = True
                    return True
        elif (direct == DOWN):
            if self.ypos < len(gameBoard[0]) - 1:
                if gameBoard[self.xpos][self.ypos+1].isfloor or gameBoard[self.xpos][self.ypos+1].islimburger:
                    self.isSlipping = False
                    if gameBoard[self.xpos][self.ypos+1].isdoor and self.numKeys > 0:
                        self.numKeys -=1
                        gameBoard[self.xpos][self.ypos+1].isdoor = False
                        return True
                    elif gameBoard[self.xpos][self.ypos+1].isdoor:
                        return False
                    if gameBoard[self.xpos][self.ypos+1].iswin:
                        self.haswon = True
                        return True
                    if gameBoard[self.xpos][self.ypos+1].hasblock:
                        if gameBoard[self.xpos][self.ypos+1].tileBlock.willMove(direct):
                            return True
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos+1].isice:
                    if self.hasSpikes:
                        self.isSlipping = False
                    else:
                        self.isSlipping = True
                    return True
                elif gameBoard[self.xpos][self.ypos+1].issad:
                    self.isSad = True
                    return True
                elif gameBoard[self.xpos][self.ypos+1].ishappy:
                    self.isSad = False
                    return True
                elif gameBoard[self.xpos][self.ypos+1].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos][self.ypos+1].iswater:
                    if not self.hasFlippers:
                        chip.isdead = True
                    return True

    
    def takeItem(self):
        if gameBoard[self.xpos][self.ypos].hasflippers:
            gameBoard[self.xpos][self.ypos].hasflippers = False
            self.hasFlippers = True
        elif gameBoard[self.xpos][self.ypos].hasspikes:
            gameBoard[self.xpos][self.ypos].hasspikes = False
            self.hasSpikes = True
        elif gameBoard[self.xpos][self.ypos].haskey:
            gameBoard[self.xpos][self.ypos].haskey = False
            self.numKeys +=1
        if gameBoard[self.xpos][self.ypos].iswater:
            if not self.hasFlippers:
                isded = True




interpereterdict = {
    "w": [WATER, False, False, False, False, False, False, False, False],
    "i": [ICE, False, False, False, False, False, False, False, False],
    "f": [FLOOR, False, False, False, False, False, False, False, False],
    "b": [FLOOR, True, False, False, False, False, False, False, False],
    "|": [WALL, False, False, False, False, False, False, False, False],
    ">": [FLOOR, False, True, False, False, False, False, False, False],
    "s": [FLOOR, False, False, True, False, False, False, False, False],
    "k": [FLOOR, False, False, False, True, False, False, False, False],
    "d": [FLOOR, False, False, False, False, True, False, False, False],
    "(": [SAD, False, False, False, False, False, False, False, False],
    ")": [HAPPY, False, False, False, False, False, False, False, False],
    "B" : [FLOOR, False, False, False, False, False, False, False, False],
    "e" : [FLOOR, False, False, False, False, False, False, True, False],
    "W" : [FLOOR, False, False, False, False, False, False, False, True],
    "h" : [FLOOR, False, False, False, False, False, True, False, False],
    "l" : [LIMBURGER, False, False, False, False, False, False, False, False]

}

def main():
    global chip, lastMove, FPSCLOCK, DISPLAYSURF, gameBoard, blockList, enemyList, startTime, levelindex
    DISPLAYSURF.fill(BLACK)
    gameBoard = []
    blockList = []
    enemyList = []
    levelname = levelArray[levelindex]
    makeBoard(open(levelname))
    chip = Player()
    chip.xpos = startX
    chip.ypos = startY
    lastMove = time.time()
    startTime = time.time()
    moveDirect = ""

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if not chip.isdead and not chip.haswon:
                if event.type == KEYUP:
                    if not chip.isSlipping:
                        if event.key in (K_LEFT, K_a):
                            moveDirect = LEFT
                            if chip.isSad:
                                moveDirect = sadMove(moveDirect)
                        elif event.key in (K_RIGHT, K_d):
                            moveDirect = RIGHT
                            if chip.isSad:
                                moveDirect = sadMove(moveDirect)
                        elif event.key in (K_UP, K_w):
                            moveDirect = UP
                            if chip.isSad:
                                moveDirect = sadMove(moveDirect)
                        elif event.key in (K_DOWN, K_s):
                            moveDirect = DOWN
                            if chip.isSad:
                                moveDirect = sadMove(moveDirect)
                        elif event.type == KEYUP:
                            if event.key == K_r:
                                main()
            elif chip.isdead:
                if event.type == KEYUP:
                    if event.key == K_r:

                        main()
            elif chip.haswon:
                if event.type == KEYUP:
                    if event.key == K_c:
                        if levelindex < len(levelArray) - 1:
                            levelindex += 1
                            main()

        if not chip.isdead and not chip.haswon:
            moveBlocks(moveDirect)
            if(time.time() - lastMove > 0.2) and not (moveDirect == ""):
                movePlayer(moveDirect)
                lastMove = time.time()
            moveEnemy()
            constructBoard()
            drawBoard()
            drawInventory()
            displayTimer()
            displayHint()
        elif chip.isdead:
            deadSurf = ENDFONT.render('Ya ded', True, BLACK, WHITE)
            restartSurf = ENDFONT.render('Press R to Restart', True, BLACK, WHITE)
            DISPLAYSURF.blit(deadSurf, (290 , 500))
            DISPLAYSURF.blit(restartSurf, (13, 600))
        elif chip.haswon:
            winSurf = ENDFONT.render('Ya won', True, BLACK, WHITE)
            scoreSurf = SMALLENDFONT.render('Score: ' + str(int(SCORE)), True, BLACK, WHITE)
            if levelindex < len(levelArray) - 1:
                continueSurf = SMALLENDFONT.render('Press C to Continue', True, BLACK, WHITE)
                DISPLAYSURF.blit(continueSurf, (100, 600))
            else:
                congratsSurf = ENDFONT.render('Congratulation!', True, BLACK, WHITE)
                DISPLAYSURF.blit(congratsSurf, (50, 600))
            DISPLAYSURF.blit(winSurf, (290, 500))
            DISPLAYSURF.blit(scoreSurf, (275, 425))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if not chip.isSlipping:
            moveDirect = ""


def sadMove(_moveDirect):
    moveDirect = _moveDirect
    if moveDirect == LEFT:
        choosing = True
        if random.randint(1, 4) == 1:
            while choosing:
                moveDirect = random.choice([UP, DOWN, RIGHT])
                if chip.canMove(moveDirect):
                    choosing = False
    if moveDirect == RIGHT:
        choosing = True
        if random.randint(1, 4) == 1:
            while choosing:
                moveDirect = random.choice([UP, DOWN, LEFT])
                if chip.canMove(moveDirect):
                    choosing = False
    if moveDirect == UP:
        choosing = True
        if random.randint(1, 4) == 1:
            while choosing:
                moveDirect = random.choice([LEFT, DOWN, RIGHT])
                if chip.canMove(moveDirect):
                    choosing = False
    if moveDirect == DOWN:
        choosing = True
        if random.randint(1, 4) == 1:
            while choosing:
                moveDirect = random.choice([UP, LEFT, RIGHT])
                if chip.canMove(moveDirect):
                    choosing = False
    return moveDirect





def makeBoard(textFile):
    global startX, startY, blockList, enemyList
    leveltext = []
    for line in textFile:
        leveltext.append(line.rstrip().split(","))

    for y in range(len(leveltext[0])):
        templine = []

        for x in range(len(leveltext)):
            tileList = interpereterdict[leveltext[x][y]]
            templine.append(Tile(tileList[0], tileList[1], tileList[2], tileList[3], tileList[4], tileList[5], tileList[6], tileList[8]))
            if(leveltext[x][y]=="B"):
                startX, startY = y,x
            if tileList[1]:
                newBlock = Block(x,y)
                blockList.append(newBlock)
                templine[len(templine)-1].tileBlock = newBlock
            if tileList[7]:
                newEnemy = Enemy(y,x)
                enemyList.append(newEnemy)
        gameBoard.append(templine)




def drawBoard():
    if chip.ypos <= 4:
        yWindow = 0
    elif chip.ypos >= len(gameBoard[0]) -5:
        yWindow = len(gameBoard[0]) -9
    else:
        yWindow = chip.ypos - 4
    if chip.xpos <= 4:
        xWindow = 0
    elif chip.xpos >= len(gameBoard) - 5:
        xWindow = len(gameBoard) - 9
    else:
        xWindow = chip.xpos - 4

    DISPLAYSURF.fill(BLACK)

    for x in range(0,9):
        for y in range(0,9):
            xcoord = 5+100*x
            ycoord = 105 + 100*y
            DISPLAYSURF.blit(gameBoard[x+xWindow][y+yWindow].tileSurf, (xcoord, ycoord))

def constructBoard():
    for row in gameBoard:
        for tile in row:
            if tile.iswater and tile.hasblock:
                blockList.remove(tile.tileBlock)
                tile.tileBlock = None
                tile.hasblock = False
                tile.iswater = False
                tile.isfloor = True
            tile.drawBaseTile()
    gameBoard[chip.xpos][chip.ypos].tileSurf.blit(chipImg, (0,0))
    for enemy in enemyList:
        gameBoard[enemy.xpos][enemy.ypos].tileSurf.blit(monsterImg, (0,0))

def movePlayer(direct):
    
    if chip.canMove(direct):
        if( direct == LEFT):
            chip.xpos -=1
        elif(direct == RIGHT):
            chip.xpos +=1
        elif( direct == UP):
            chip.ypos -= 1
        elif(direct == DOWN):
            chip.ypos +=1
        chip.takeItem()

def moveBlocks(direct):
    global blockList
    for block in blockList:
        if time.time() - block.lastMove > 0.2:
            if block.isSlipping:
                if block.willMove(block.slipDirect):
                    block.lastMove = time.time()
                    gameBoard[block.xpos][block.ypos].tileBlock = None
                    gameBoard[block.xpos][block.ypos].hasblock = False
                    if block.slipDirect == LEFT:
                        block.xpos -=1
                    elif block.slipDirect == RIGHT:
                        block.xpos +=1
                    elif block.slipDirect == UP:
                        block.ypos -=1
                    elif block.slipDirect == DOWN:
                        block.ypos +=1
                    gameBoard[block.xpos][block.ypos].tileBlock = block
                    gameBoard[block.xpos][block.ypos].hasblock = True
            else:
                if block.willMove(direct):
                    block.lastMove = time.time()
                    gameBoard[block.xpos][block.ypos].tileBlock = None
                    gameBoard[block.xpos][block.ypos].hasblock = False
                    if direct == LEFT:
                        block.xpos -=1
                    elif direct == RIGHT:
                        block.xpos +=1
                    elif direct == UP:
                        block.ypos -=1
                    elif direct == DOWN:
                        block.ypos +=1
                    gameBoard[block.xpos][block.ypos].tileBlock = block
                    gameBoard[block.xpos][block.ypos].hasblock = True
                        
                        
def moveEnemy():
    global enemyList, chip
    for enemy in enemyList:
        if (gameBoard[enemy.xpos][enemy.ypos].islimburger and  time.time() - enemy.movetime  > 0.2) or time.time() - enemy.movetime > 0.4:
            enemydirect = enemy.moveDirect()
            if enemydirect == LEFT:
                    enemy.xpos -= 1
                    enemy.movetime = time.time()
            elif enemydirect == RIGHT:
                    enemy.xpos += 1
                    enemy.movetime = time.time()
            elif enemydirect == UP:
                    enemy.ypos -= 1
                    enemy.movetime = time.time()
            elif enemydirect == DOWN:
                    enemy.ypos += 1
                    enemy.movetime = time.time()
    for enemy in enemyList:
        if enemy.xpos == chip.xpos and enemy.ypos == chip.ypos:
            chip.isdead = True



def drawInventory():
    DISPLAYSURF.blit(blkSurf, (0,0))
    if chip.hasSpikes:
        DISPLAYSURF.blit(inventorySpikes, (500, 5))
    if chip.numKeys > 0:
        DISPLAYSURF.blit(inventoryKey, (550, 5))
    if chip.hasFlippers:
        DISPLAYSURF.blit(inventoryFlippers, (450, 5))

class Block:

    def __init__(self, _xpos, _ypos):
        self.ypos, self.xpos = _xpos, _ypos
        self.isSlipping = False
        self.slipDirect = ""
        self.lastMove = time.time()
        
        
    def willMove(self, direct):
        if direct == LEFT:
            if self.xpos > 0 and ((chip.xpos == self.xpos + 1 and chip.ypos == self.ypos) or self.isSlipping):
                if gameBoard[self.xpos-1][self.ypos].hasblock:
                    self.isSlipping = False
                    return False
                if gameBoard[self.xpos-1][self.ypos].isfloor or gameBoard[self.xpos-1][self.ypos].ishappy or gameBoard[self.xpos-1][self.ypos].issad:
                    self.isSlipping = False
                    if gameBoard[self.xpos-1][self.ypos].isdoor or gameBoard[self.xpos-1][self.ypos].iswin:
                        return False
                    return True
                elif gameBoard[self.xpos-1][self.ypos].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos-1][self.ypos].isdoor:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos-1][self.ypos].isice:
                    self.isSlipping = True
                    self.slipDirect = direct
                    return True
                elif gameBoard[self.xpos - 1][self.ypos].iswater:
                    self.isSlipping = False
                    return True
        if direct == RIGHT:
            if self.xpos < len(gameBoard) - 1 and ((chip.xpos == self.xpos - 1 and chip.ypos == self.ypos) or self.isSlipping):
                if gameBoard[self.xpos+1][self.ypos].hasblock:
                    self.isSlipping = False
                    return False
                if gameBoard[self.xpos+1][self.ypos].isfloor or gameBoard[self.xpos+1][self.ypos].ishappy or gameBoard[self.xpos+1][self.ypos].issad:
                    self.isSlipping = False
                    if gameBoard[self.xpos+1][self.ypos].isdoor or gameBoard[self.xpos+1][self.ypos].iswin:
                        return False
                    return True
                elif gameBoard[self.xpos+1][self.ypos].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos+1][self.ypos].isice:
                    self.isSlipping = True
                    self.slipDirect = direct
                    return True
                elif gameBoard[self.xpos + 1][self.ypos].iswater:
                    self.isSlipping = False
                    return True
        if direct == UP:
            if self.ypos > 0 and ((chip.xpos == self.xpos and chip.ypos == self.ypos+1) or self.isSlipping):
                if gameBoard[self.xpos][self.ypos-1].hasblock:
                    self.isSlipping = False
                    return False
                if gameBoard[self.xpos][self.ypos-1].isfloor or gameBoard[self.xpos][self.ypos-1].ishappy or gameBoard[self.xpos][self.ypos-1].issad:
                    self.isSlipping = False
                    if gameBoard[self.xpos][self.ypos-1].isdoor or gameBoard[self.xpos][self.ypos-1].iswin:
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos-1].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos][self.ypos-1].isice:
                    self.isSlipping = True
                    self.slipDirect = direct
                    return True
                elif gameBoard[self.xpos][self.ypos-1].iswater:
                    self.isSlipping = False
                    return True
        if direct == DOWN:
            if self.ypos < len(gameBoard[0]) and ((chip.xpos == self.xpos and chip.ypos == self.ypos-1) or self.isSlipping):
                if gameBoard[self.xpos][self.ypos+1].hasblock:
                    self.isSlipping = False
                    return False
                if gameBoard[self.xpos][self.ypos+1].isfloor or gameBoard[self.xpos][self.ypos+1].ishappy or gameBoard[self.xpos][self.ypos+1].issad :
                    self.isSlipping = False
                    if gameBoard[self.xpos][self.ypos+1].isdoor or gameBoard[self.xpos][self.ypos+1].iswin:
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos+1].iswall:
                    self.isSlipping = False
                    return False
                elif gameBoard[self.xpos][self.ypos+1].isice:
                    self.isSlipping = True
                    self.slipDirect = direct
                    return True
                elif gameBoard[self.xpos][self.ypos + 1].iswater:
                    self.isSlipping = False
                    return True
        return False

def displayTimer():
    global SCORE, chip
    SCORE = (LEVEL1TIME - time.time() + startTime) * 5
    timerSurf = BASICFONT.render("Time: " + str(int(LEVEL1TIME - time.time() + startTime)), True, BLACK, WHITE)
    DISPLAYSURF.blit(timerSurf, (100, 25))
    if(LEVEL1TIME - time.time() + startTime <= 0):
        chip.isdead = True



class Enemy:

    def __init__(self, _xpos, _ypos):
        self.xpos = _xpos
        self.ypos = _ypos
        self.movetime = time.time()

    def canMove(self, direct):
        if (direct == LEFT):
            if self.xpos > 0:
                for enemy in enemyList:
                    if self.xpos - 1 == enemy.xpos and self.ypos == enemy.ypos:
                        return False
                if gameBoard[self.xpos-1][self.ypos].isfloor or gameBoard[self.xpos-1][self.ypos].islimburger:
                    if gameBoard[self.xpos-1][self.ypos].isdoor:
                        return False
                    if gameBoard[self.xpos-1][self.ypos].hasblock:
                        return False
                    return True
                elif gameBoard[self.xpos-1][self.ypos].isice:
                    return True
                elif gameBoard[self.xpos-1][self.ypos].iswall:
                    return False
                elif gameBoard[self.xpos - 1][self.ypos].iswater:
                    return False
        elif (direct == RIGHT):
            if self.xpos < len(gameBoard) - 1:
                for enemy in enemyList:
                    if self.xpos + 1 == enemy.xpos and self.xpos == enemy.xpos:
                        return False
                if gameBoard[self.xpos+1][self.ypos].isfloor or gameBoard[self.xpos+1][self.ypos].islimburger:
                    if gameBoard[self.xpos+1][self.ypos].isdoor:
                        return False
                    if gameBoard[self.xpos+1][self.ypos].hasblock:
                        return False
                    return True
                elif gameBoard[self.xpos+1][self.ypos].isice:
                    return True
                elif gameBoard[self.xpos+1][self.ypos].iswall:
                    return False

                elif gameBoard[self.xpos + 1][self.ypos].iswater:
                    return False
        elif (direct == UP):
            if self.ypos > 0:
                for enemy in enemyList:
                    if self.ypos - 1 == enemy.ypos and self.ypos == enemy.ypos:
                        return False
                if gameBoard[self.xpos][self.ypos-1].isfloor or gameBoard[self.xpos][self.ypos-1].islimburger:
                    if gameBoard[self.xpos][self.ypos-1].isdoor:
                        return False
                    if gameBoard[self.xpos][self.ypos-1].hasblock:
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos-1].isice:
                    return True
                elif gameBoard[self.xpos][self.ypos-1].iswall:
                    return False
                elif gameBoard[self.xpos][self.ypos-1].iswater:
                    return False
        elif (direct == DOWN):
            if self.ypos < len(gameBoard[0]) - 1:
                for enemy in enemyList:
                    if self.ypos + 1 == enemy.ypos and self.xpos == enemy.xpos:
                        return False
                if gameBoard[self.xpos][self.ypos+1].isfloor or gameBoard[self.xpos][self.ypos+1].islimburger:
                    if gameBoard[self.xpos][self.ypos+1].isdoor:
                        return False
                    if gameBoard[self.xpos][self.ypos+1].hasblock:
                        return False
                    return True
                elif gameBoard[self.xpos][self.ypos+1].isice:
                    return True
                elif gameBoard[self.xpos][self.ypos+1].iswall:
                    return False
                elif gameBoard[self.xpos][self.ypos+1].iswater:
                    return True

    def moveDirect(self):
        leftdist = (chip.xpos - self.xpos )**2 +  (chip.ypos - self.ypos)**2
        rightdist = (chip.xpos - self.xpos )**2 +  (chip.ypos - self.ypos)**2
        updist = (chip.xpos - self.xpos )**2 +  (chip.ypos - self.ypos)**2
        downdist = (chip.xpos - self.xpos )**2 +  (chip.ypos - self.ypos)**2
        neutraldist = (chip.xpos - self.xpos )**2 +  (chip.ypos - self.ypos)**2
        if self.canMove(LEFT):
            leftdist = (chip.xpos - (self.xpos - 1))**2 +  (chip.ypos - self.ypos)**2
        if self.canMove(RIGHT):
            rightdist = (chip.xpos - (self.xpos + 1))**2 +  (chip.ypos - self.ypos)**2
        if self.canMove(UP):
            updist = (chip.xpos - self.xpos)**2 +  (chip.ypos - (self.ypos - 1))**2
        if self.canMove(DOWN):
            downdist = (chip.xpos - self.xpos)**2 +  (chip.ypos - (self.ypos + 1))**2
            

        if leftdist <= rightdist and leftdist < updist and leftdist <= downdist and self.canMove(LEFT):
            return LEFT
        if rightdist <= updist and rightdist <= downdist and self.canMove(RIGHT):
            return RIGHT
        elif updist <= downdist and self.canMove(UP):
            return UP
        elif self.canMove(DOWN):
            return DOWN





                
        





        
        
    




main()
















