import pygame
import colorspy as color
import random
pygame.init()

size = 10
mines = 5
dimensions = 600
gap = dimensions // size

#color themes
themeLight = {
    "mine" : color.red,
    "background" : color.white,
    "text" : color.black,
    "closedTile" : color.gray,
    "openTile" : color.light_gray,
    "gridLine" : color.light_gray
}
themeDark = {
    "mine" : color.red,
    "background" : (18, 18, 18),
    "text" : (255, 255, 255),
    "closedTile" : (24, 24, 24),
    "openTile" : (64, 64, 64),
    "gridLine" : (40, 40, 40)
}
themes = [themeLight, themeDark]
theme = themes[1]

# inputs for the user to select features
size = int(input("Enter the size: "))
mines = int(input("Enter the amount of mines: "))
theme = themes[int(input("Enter theme code (0 for light, 1 for dark): "))]



#init all text
window = pygame.display.set_mode((dimensions, dimensions))
pygame.display.set_caption("Pysweeper")
fontObj = pygame.font.Font(None, gap)
numbers = [fontObj.render('', True, theme["text"])]
for i in range(1, 9):
    numbers.append(fontObj.render(str(i), True, theme["text"]))

#init the board
field = []
fieldOpen = []
fieldProximity = []
fieldFlags = []
for i in range(size):
    field.append([])
    fieldOpen.append([])
    fieldProximity.append([])
    fieldFlags.append([])
for i in range(size):
    for j in range(size):
        field[i].append(False)
        fieldOpen[i].append(False)
        fieldFlags[i].append(False)
        fieldProximity[i].append(False)
#init all mines
fieldMines = 0
while fieldMines < mines:
    xBomb = random.randint(0, size-1)
    yBomb = random.randint(0, size-1)
    if not field[xBomb][yBomb]:
        field[xBomb][yBomb] = True
        fieldMines += 1

#calculate proximity
#   array was initially initalized with "False" 
#   -1 means the spot is a bomb
#   0-8 represents amount of bombs surrounding it
for x in range(size):
    for y in range(size):
        if field[x][y]:
            fieldProximity[x][y] = -1
        else:
            proximity = 0
            #top row
            #   left
            if x - 1 >= 0 and y - 1 >= 0 and field[x - 1][y - 1]:
                proximity += 1
            #   middle
            if y - 1 >= 0 and field[x][y - 1]:
                proximity += 1
            #   right
            if x + 1 < len(field) and y - 1 >= 0 and field[x + 1][y - 1]:
                proximity += 1

            #middle row
            #   left
            if x - 1 >= 0 and field[x - 1][y]:
                proximity += 1
            #   right
            if x + 1 < len(field) and field[x + 1][y]:
                proximity += 1
            
            #bottom row
            #   left 
            if x - 1 >= 0 and y + 1 < len(field) and field[x - 1][y + 1]:
                proximity += 1
            #   middle
            if y + 1 < len(field) and field[x][y + 1]:
                proximity += 1
            #   right
            if x + 1 < len(field) and y + 1 < len(field) and field[x + 1][y + 1]:
                proximity += 1
            
            fieldProximity[x][y] = proximity

def openSurroundings(x, y):
    fieldOpen[x][y] = True
    opened = 1
    if fieldProximity[x][y] == 0:
        #top row
        #   left
        if x - 1 >= 0 and y - 1 >= 0:   
            if not fieldOpen[x - 1][y - 1]:
                fieldOpen[x - 1][y - 1] = True
                if fieldProximity[x - 1][y - 1] == 0:
                    openSurroundings(x - 1, y - 1)
            opened += 1
        #   middle
        if y - 1 >= 0:
            if not fieldOpen[x][y - 1]:
                fieldOpen[x][y - 1] = True
                if fieldProximity[x][y - 1] == 0:
                    openSurroundings(x, y - 1)
            opened += 1
        #   right
        if x + 1 < len(field) and y - 1 >= 0:  
            if not fieldOpen[x + 1][y - 1]:
                fieldOpen[x + 1][y - 1] = True
                if fieldProximity[x + 1][y - 1] == 0:
                    openSurroundings(x + 1, y - 1)
            opened += 1

        #middle row
        #   left
        if x - 1 >= 0:
            if not fieldOpen[x - 1][y]:
                fieldOpen[x - 1][y] = True
                if fieldProximity[x - 1][y] == 0:
                    openSurroundings(x - 1, y)
            opened += 1
        #   right
        if x + 1 < len(field): 
            if not fieldOpen[x + 1][y]:
                fieldOpen[x + 1][y] = True
                if fieldProximity[x + 1][y] == 0:
                    openSurroundings(x + 1, y)
            opened += 1
        
        #bottom row
        #   left 
        if x - 1 >= 0 and y + 1 < len(field):  
            if not fieldOpen[x - 1][y + 1]:
                fieldOpen[x - 1][y + 1] = True
                if fieldProximity[x - 1][y + 1] == 0:
                    openSurroundings(x - 1, y + 1)
            opened += 1
        #   middle
        if y + 1 < len(field):  
            if not fieldOpen[x][y + 1]:
                fieldOpen[x][y + 1] = True
                if fieldProximity[x][y + 1] == 0:
                    openSurroundings(x, y + 1)
            opened += 1
        #   right
        if x + 1 < len(field) and y + 1 < len(field):
            if not fieldOpen[x + 1][y + 1]:
                fieldOpen[x + 1][y + 1] = True
                if fieldProximity[x + 1][y + 1] == 0:
                    openSurroundings(x + 1, y + 1)
            opened += 1
    return opened

def draw(win, lose):
    # clear screen
    window.fill(theme["background"])

    # draw tiles
    rectColor = theme["closedTile"]
    for i in range(size):
        for j in range(size):
            if fieldOpen[j][i]:
                rectColor = theme["openTile"]
            if field[j][i] and (win or lose):
                rectColor = theme["mine"]
            pygame.draw.rect(window, rectColor, (i * gap, j * gap, gap, gap))
            rectColor = theme["closedTile"]
    # draw numbers
    for y in range(size):
        for x in range(size):
            if fieldOpen[x][y]:
                window.blit(numbers[fieldProximity[x][y]], (((gap * y)+(gap//2.75)), ((gap * x)+(gap//2.75))))
    # draw grid
    for i in range(size + 1):
        pygame.draw.line(window, theme["gridLine"], (0, i * gap), (dimensions, i * gap)) 
        for j in range(size):
            pygame.draw.line(window, theme["gridLine"], (j * gap, 0), (j * gap, dimensions))

def clickPos(pos, rows, dimensions):
    gap = dimensions // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row,col

def main():
    quit = False
    win = False
    lose = False
    timer = False
    timeS = 0
    timeMS = 0
    while not quit:
        #handling mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1]:
                timer = True
                position = pygame.mouse.get_pos()
                row, col = clickPos(position, size, dimensions)
                if pygame.mouse.get_pressed()[0]:
                    if field[col][row]:
                        lose = True
                        break
                    if not fieldOpen[col][row]:
                        openSurroundings(col, row)
                    opened = 0
                    for i in fieldOpen:
                        for j in i:
                            if j:
                                opened += 1
                    if opened == size**2 - mines:
                        win = True
                            

                if pygame.mouse.get_pressed()[1]:
                    break
        #updating the screen
        draw(win, lose)
        pygame.display.update()



main()