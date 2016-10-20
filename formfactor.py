import random, pygame, sys, time
from pygame.locals import *

FPS = 100
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
SCORE = 0
SCORPLUS = 50
SCORMINUS = 80
SHAPESIZE = 160
GAPSIZE = 40
BOARDWIDTH = 3
BOARDHEIGHT = 3
TIMESPLAYED = 0
MOD = [ 'placeholder' ]
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (SHAPESIZE + GAPSIZE))) / 2)
YMARGIN = int ((WINDOWHEIGHT - (BOARDHEIGHT * (SHAPESIZE + GAPSIZE))) / 2)
NULL = ( '' , '' )   # empty space
TIME = [10, 0]

# C U L O R I

# Scherma Veche

#BLACK     = (  0,   0,   0)
#RED       = (186,  24,  24)
#GREEN     = ( 90, 204,  78)
#BLUE      = ( 12, 189, 247)
#YELLOW    = (214, 209,  49)
#WHITE     = (255, 255, 255)
#DARKGREEN = (  0, 102,   0)
#DARKRED   = (154,   0,   0)

# Scherma Nova

BLACK     = (  0,   0,   0)
RED       =  (252,  88,  88)
GREEN     = ( 90, 204,  78)
BLUE      = ( 122, 207,233)
YELLOW    = (222, 205,  49)
WHITE     = (255, 255, 255)
DARKGREEN = (  52, 77,  52)
DARKRED   = (111,   47, 47)

# S P A T I I
spatii = [ [0, 1], [1, 0], [1, 1], [1, 2], [2, 1] ]

# W A L L P A P E R E
BGGOODCOLOR = DARKGREEN
BGBADCOLOR = DARKRED
BGCOLOR = BGGOODCOLOR

# F O R M E
SQUARE = 'square'
TRIANGLE = 'triangle'
ROMB = 'romb'
CERC = 'cerc'

ALLCOLORS = (RED, GREEN,  BLUE, YELLOW)
ALLSHAPES = (SQUARE, TRIANGLE, ROMB, CERC)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSCLOCK = pygame.time.Clock()

GAMELOOP = True

def main(argument):
	global FPSCLOCK, DISPLAYSURF, GAMELOOP
	pygame.font.init()
	font = pygame.font.Font('freesansbold.ttf', 24)
	pygame.display.set_caption("Form Factor")
	
	mainBoard = getRandomizedBoard(argument)
	#print mainBoard
	
	DISPLAYSURF.fill(BGCOLOR)
	
	while GAMELOOP:
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(mainBoard, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)
		text = font.render("Score: %d" % SCORE, True, pygame.Color('white'))
		DISPLAYSURF.blit(text, (5, 5))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_BACKSPACE:
					menu()
				if event.key == pygame.K_UP:
					checkCorrect(mainBoard[1][1], mainBoard[1][0], argument)
				if event.key == pygame.K_DOWN:
					checkCorrect(mainBoard[1][1], mainBoard[1][2], argument)
				if event.key == pygame.K_LEFT:
					checkCorrect(mainBoard[1][1], mainBoard[0][1], argument)
				if event.key == pygame.K_RIGHT:
					checkCorrect(mainBoard[1][1], mainBoard[2][1], argument)
					
		timer_update(argument)
		timer_draw()
			
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def menu():
	global MOD, TIMESPLAYED, TIME, SCORE, GAMELOOP
	intro = True
	
	largeText = pygame.font.Font('freesansbold.ttf', 115)
	smallText = pygame.font.Font('freesansbold.ttf', 20)
	instructText = pygame.font.Font('freesansbold.ttf', 30)
	TextSurf, TextRect = text_objects("Form Factor", largeText)
	PlaySurf, PlayRect = text_objects("Press 1 for Shape AND Color, 2 for Shape, 3 for Color or Escape to exit.", smallText)
	InstructSurf, InstructRect = text_objects("Match the colour or shape using the arrow keys!", instructText)
	TextRect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 4))
	PlayRect.center = ((WINDOWWIDTH / 2), (5 * (WINDOWHEIGHT / 6)))
	InstructRect.center = ((WINDOWWIDTH / 2) , (3 * (WINDOWHEIGHT / 4)))
		
	while intro:
		DISPLAYSURF.fill(DARKGREEN)
		DISPLAYSURF.blit(TextSurf, TextRect)
		DISPLAYSURF.blit(PlaySurf, PlayRect)
		DISPLAYSURF.blit(InstructSurf, InstructRect)
	
		for event in pygame.event.get():
			#print event
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_1:
					TIME = [10, 0]
					if (TIMESPLAYED >= 1 and MOD[TIMESPLAYED] == 'both'):
						TIME[0] += (SCORE / 100)
					SCORE = 0
					GAMELOOP = True
					intro = False
					main('both')
					
				if event.key == pygame.K_2:
					TIME = [10, 0]
					if (TIMESPLAYED > 1 and MOD[TIMESPLAYED] == 'shapes'):				# primesti bonus doar daca modul de joc a ramas acelasi
						TIME[0] += (SCORE / 100)
					SCORE = 0
					GAMELOOP = True
					intro = False
					main('shapes')
					
				if event.key == pygame.K_3:
					TIME = [10, 0]
					if (TIMESPLAYED > 1 and MOD[TIMESPLAYED] == 'colors'):
						TIME[0] += (SCORE / 100)
					SCORE = 0
					GAMELOOP = True
					intro = False
					main('colors')

		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
def getRandomizedBoard(argument):
	icons = []
	for color in ALLCOLORS:
		for shape in ALLSHAPES:
			icons.append( (shape, color) )
	
	random.shuffle(icons)
	central = icons[0]
	del(icons[0])
	
	board = []
	common = []
	notcommon = []
	boardlist = []
	
	for icon in icons:
		if argument == 'both':
			if icon[0] == central[0] or icon[1] == central[1]:
				common.append(icon)
			else:
				notcommon.append(icon)
		elif argument == 'shapes':
			if icon[0] == central[0] and icon[1] != central[1]:
				common.append(icon)
			elif icon[0] != central[0] and icon[1] != central[1]:
				notcommon.append(icon)
		elif argument == 'colors':
			if icon[0] != central[0] and icon[1] == central[1]:
				common.append(icon)
			elif icon[0] != central[0] and icon[1] != central[1]:
				notcommon.append(icon)
				
	nr = random.randrange(5)
	if nr == 2: nr += random.randrange(1,3) # putin hacky, ca sa ma asigur ca nu coincid central si iconita corecta
	
	for i in range(5):
		if i == nr: 
			boardlist.append(common[0])
		elif i == 2:
			boardlist.append(central)
		else: 
			boardlist.append(notcommon[0])
			del notcommon[0]
			
	for x in range(BOARDWIDTH):
		column = []
		for y in range(BOARDHEIGHT):
			if [x, y] in spatii:
				column.append(boardlist[0])
				del(boardlist[0])
			else: column.append(NULL)
		board.append(column)
	
	return board
	
def drawBoard(board, boardwidth, boardheight, xmargin, ymargin):
	for boxx in range(boardwidth):
		for boxy in range(boardheight):
			if board[boxx][boxy] != NULL:
				left, top = leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin)
				shape, color = getShapeAndColor(board, boxx, boxy)
				drawIcon(shape, color, boxx, boxy, xmargin, ymargin)
	
def leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin):
	left = boxx * (SHAPESIZE + GAPSIZE) + xmargin
	top  = boxy * (SHAPESIZE + GAPSIZE) + ymargin
	return (left, top)
	
def drawIcon(shape, color, boxx, boxy, xmargin, ymargin): # size 120
	quarter = int(SHAPESIZE * 0.25)
	half    = int(SHAPESIZE * 0.5) # pentru coordonate
	left, top = leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin) # stanga sus in cutie
	
	if shape == SQUARE: pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, SHAPESIZE - half, SHAPESIZE - half))
	elif shape == TRIANGLE: pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top + quarter), (left + quarter, top + half + quarter), (left + half + quarter, top + half + quarter)))
	elif shape == ROMB: pygame.draw.polygon(DISPLAYSURF, color, ((left + half + quarter, top + half), (left + half, top + quarter), (left + quarter, top + half), (left + half, top + half + quarter)))
	elif shape == CERC: pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), quarter - 5)
	
def getShapeAndColor(board, boxx, boxy):
	return board[boxx][boxy][0], board[boxx][boxy][1]	  
				
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def checkCorrect(s1, s2, argument):
	global SCORE, BGCOLOR, TIME
	if s1[0] == s2[0] or s1[1] == s2[1]:
		SCORE += SCORPLUS
		BGCOLOR = BGGOODCOLOR
		TIME[1] += 20
		if TIME[1] > 99: 
			TIME[0] += 1
			TIME[1] -= 100
		pygame.time.wait(210)
		main(argument)
	else:							
		SCORE -= SCORMINUS
		BGCOLOR = BGBADCOLOR
		TIME[0] -= 1
		pygame.time.wait(210)
		main(argument)
		
def game_over(argument):
	global GAMELOOP, TIME, SCORE, BGCOLOR, MOD, TIMESPLAYED
	gameover = True
	
	MOD.append(argument)
	TIMESPLAYED += 1
	#print MOD
	#print "ori: %d" % TIMESPLAYED
	
	scorfont = pygame.font.Font('freesansbold.ttf', 24)
	bonusfont = pygame.font.Font('freesansbold.ttf', 24)
	ScoreSurf, ScoreRect = text_objects("Final score: %d" % SCORE, scorfont)
	BonusSurf, BonusRect = text_objects("You get a bonus of %d seconds!" % (SCORE / 100) , bonusfont)
	ScoreRect.center = ((WINDOWWIDTH / 2), (3 * (WINDOWHEIGHT / 7)))
	BonusRect.center = ((WINDOWWIDTH / 2), (3 * (WINDOWHEIGHT / 5)))
	
	while gameover:
		
		DISPLAYSURF.fill(BLACK)
		DISPLAYSURF.blit(ScoreSurf, ScoreRect)
		DISPLAYSURF.blit(BonusSurf, BonusRect)
		
		for event in pygame.event.get():
			#print event
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_RETURN:
					BGCOLOR = BGGOODCOLOR
					gameover = False				# reinitializam variabile importante
					menu()
		
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
	
	
# TIMER FUNCTIONS BELOW	

def timer_update(argument):
	global TIME, GAMELOOP
	if TIME[0] < 0: 
		game_over(argument)
	TIME[1] -= 1
	#print "%s : %s" % (TIME[0], TIME[1])
	
	if TIME[1] < 0:
		TIME[1] = 99
		TIME[0] -= 1
		if TIME[0] < 0:
			TIME = [0,0]
			game_over(argument)
			
				
def timer_draw():
	timerfont = pygame.font.Font('freesansbold.ttf', 24)
	
	t1 = str(TIME[0])
	if len(t1) == 1: t1 = "0"+t1
	t2 = str(TIME[1])
	if len(t2) == 1: t2 = "0"+t2
	string = t1 + " : " + t2
	
	timertext = timerfont.render(string, True, pygame.Color('white'))
	DISPLAYSURF.blit(timertext, (666, 5))
	
# TIMER FUNCTIONS ABOVE

menu()
pygame.quit()
quit()