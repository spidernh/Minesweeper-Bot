from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con

unknownDark = (162, 209, 73)
unknownLight = (170, 215, 81)
zeroDark = (215, 184, 153)
zeroLight = (229, 194, 159)
one = (25, 118, 210)
two = (56, 142, 60)
three = (211, 47, 47)
four = (123, 31, 162)
five = (255, 143, 0)
six = (2, 152, 167)

# Easy (210%)
region = (486, 269, (1416 - 486), (1013 - 269))
dimens = (10, 8)

# Medium (170%)
# region = (489, 271, (1413 - 489), (990 - 271))
# dimens = (18, 14)

# Hard (160%)
# region = (478, 239, (1424 - 478), (1029 - 239))
# dimens = (24, 20)

percentSearched = 0.5
searchRes = 16
pixelsPerTile = region[2] / dimens[0]
delta = (pixelsPerTile * percentSearched) / searchRes

pic = pyautogui.screenshot(region=region)

def leftClickAt(x, y):
    # Left click at the given screen coordinates.
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01) # Seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
def rightClickAt(x, y):
    # Right click at the given screen coordinates.
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.01) # Seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def move(x, y):
    # Moves the cursor to the desired position
    win32api.SetCursorPos((x, y))

def doTile(x, y, centered=True, click="left"):
    # Either click or move the mouse to the given tile.
    sCoords = getCoords(x, y, centered=centered, relativeRegion=False)
    if (click == "left"):
        leftClickAt(sCoords[0], sCoords[1])
    elif (click == "right"):
        rightClickAt(sCoords[0], sCoords[1])
    else:
        move(sCoords[0], sCoords[1])

def getCoords(x, y, centered=True, relativeRegion=False):
    # Use the pixelsPerTile variable to find the position of the tile.
    # Centered: If true, will return the center of the tile. If false, will return the top left corner of the tile.
    # Relative Region: If true, it will return the position relative to the region used for the screenshot. If false, it will return it in screen-coordinates.
    pixelsPerTile = region[2] / dimens[0]
    xPos = x
    yPos = y
    if (centered):
        xPos += 0.5
        yPos += 0.5
    if (relativeRegion):
        return (round(xPos * pixelsPerTile), round(yPos * pixelsPerTile))
    else:
        return (round(xPos * pixelsPerTile) + region[0], round(yPos * pixelsPerTile) + region[1])

def readBoard():
    # Get a screenshot of the board area and create the board variable
    pic = pyautogui.screenshot(region=region)
    board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

    # Go through every tile and detect what it is.
    for y in range(len(board)):
        for x in range(len(board[y])):
            tile = createTile(x, y)
            board[y][x] = getNum(tile)
    return board

def getNum(tile):
    # Check the tile string and return the corresponding number.
    if (tile == "unknown"):
        return -1
    elif (tile == "zero"):
        return 0
    elif (tile == "one"):
        return 1
    elif (tile == "two"):
        return 2
    elif (tile == "three"):
        return 3
    elif (tile == "four"):
        return 4
    elif (tile == "five"):
        return 5
    elif (tile == "six"):
        return 6

def createTile(x, y):
    coords = getCoords(x, y, centered=True, relativeRegion=True)
    startX = coords[0] - (delta * searchRes / 2)
    startY = coords[1] - (delta * searchRes / 2)
    tile = "zero"
    # Go through a (currently) 16x16 grid of pixels in the tile and check if any of them match a specific color.
    # If it does, set the tile to the corresponding number. (All numbers have a unique RGB value)
    for y1 in range(searchRes - 1):
        searchY = round(startY + (y1 * delta))
        for x1 in range(searchRes - 1):
            searchX = round(startX + (x1 * delta))
            pixel = pic.getpixel((searchX - 1, searchY - 1))
            if (pixel == unknownDark or pixel == unknownLight):
                tile = "unknown"
                break
            elif (pixel == one):
                tile = "one"
                break
            elif (pixel == two):
                tile = "two"
                break
            elif (pixel == three):
                tile = "three"
                break
            elif (pixel == four):
                tile = "four"
                break
            elif (pixel == five):
                tile = "five"
                break
    return tile

def analyzeTile(x, y, findRealBombs=False):
    bombsNear = 0
    if (not findRealBombs): bombsNear = board[y][x]
    unlockedNear = -1
    lockedNear = -1
    # If the tile is known, this will pass.
    if (bombsNear != -1 and bombsNear != -2):
        unlockedNear = 0
        lockedNear = 0
        # True if the tile isn't on the given edge
        up = y != 0
        down = y != dimens[1] - 1
        left = x != 0
        right = x != dimens[0] - 1
        # Check for known and unknown tiles around this tile
        if (up and left):
            if (board[y - 1][x - 1] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y - 1][x - 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (up and right):
            if (board[y - 1][x + 1] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y - 1][x + 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (down and left):
            if (board[y + 1][x - 1] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y + 1][x - 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (down and right):
            if (board[y + 1][0] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y + 1][x + 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (up):
            if (board[y - 1][x] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y - 1][x] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (down):
            if (board[y + 1][x] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y + 1][x] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (left):
            if (board[y][x - 1] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y][x - 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else:
                # print("UNLOCKED")
                unlockedNear += 1
        if (right):
            if (board[y][x + 1] == -1):
                # print("LOCKED")
                lockedNear += 1
            elif (board[y][x + 1] == -2):
                if (findRealBombs):
                    bombsNear += 1
                else:
                    lockedNear += 1
            else: 
                # print("UNLOCKED")
                unlockedNear += 1
    return (bombsNear, unlockedNear, lockedNear)

def markAllBombs(x, y, results):
    bombsNear = results[0]
    lockedNear = results[2]
    # Mark all bombs using these rules:
    # 1. If the number of unmined tiles is equal to the number of bombs around the tile, then all of the unmined tiles must be bombs.
    # 2. No other rules so far
    if (lockedNear == bombsNear and results[0] > 0):
        up = y != 0
        down = y != dimens[1] - 1
        left = x != 0
        right = x != dimens[0] - 1
        # All locked spots near are bombs, so mark all locked as bombs
        if (up and left):
            if (board[y - 1][x - 1] == -1): board[y - 1][x - 1] = -2
        if (up and right):
            if (board[y - 1][x + 1] == -1): board[y - 1][x + 1] = -2
        if (down and left):
            if (board[y + 1][x - 1] == -1): board[y + 1][x - 1] = -2
        if (down and right):
            if (board[y + 1][x + 1] == -1): board[y + 1][x + 1] = -2
        if (up):
            if (board[y - 1][x] == -1): board[y - 1][x] = -2
        if (down):
            if (board[y + 1][x] == -1): board[y + 1][x] = -2
        if (left):
            if (board[y][x - 1] == -1): board[y][x - 1] = -2
        if (right):
            if (board[y][x + 1] == -1): board[y][x + 1] = -2

def mineAllSafe(x, y, results):
    minedCounter = 0
    # Mine all non-bombs using these rules:
    # 1. Only mine if all the bombs are found (the number on the tile matches the number of bombs the program knows about)
    # 2. Mine all the non-bombs around it (like a chord)
    if (results[0] == board[y][x] and board[y][x] != -1):
        up = y != 0
        down = y != dimens[1] - 1
        left = x != 0
        right = x != dimens[0] - 1
        # All locked spots near are bombs, so mark all locked as bombs
        clickType = "left"
        if (up and left):
            if (board[y - 1][x - 1] == -1):
                doTile(x - 1, y - 1, centered=True, click=clickType)
                minedCounter += 1
        if (up and right):
            if (board[y - 1][x + 1] == -1):
                doTile(x + 1, y - 1, centered=True, click=clickType)
                minedCounter += 1
        if (down and left):
            if (board[y + 1][x - 1] == -1):
                doTile(x - 1, y + 1, centered=True, click=clickType)
                minedCounter += 1
        if (down and right):
            if (board[y + 1][x + 1] == -1):
                doTile(x + 1, y + 1, centered=True, click=clickType)
                minedCounter += 1
        if (up):
            if (board[y - 1][x] == -1):
                doTile(x, y - 1, centered=True, click=clickType)
                minedCounter += 1
        if (down):
            if (board[y + 1][x] == -1):
                doTile(x, y + 1, centered=True, click=clickType)
                minedCounter += 1
        if (left):
            if (board[y][x - 1] == -1):
                doTile(x - 1, y, centered=True, click=clickType)
                minedCounter += 1
        if (right):
            if (board[y][x + 1] == -1):
                doTile(x + 1, y, centered=True, click=clickType)
                minedCounter += 1
    return minedCounter

# The program loop, which will play until the game is done, or until it can't figure out what to do.
while (not keyboard.is_pressed("q")):
    board = readBoard()
    # Mark all the bombs
    for y in range(len(board)):
        for x in range(len(board[y])):
            results = analyzeTile(x, y)
            bombsNear = results[0]
            unlockedNear = results[1]
            lockedNear = results[2]
            markAllBombs(x, y, results)

    # Mine all of the 100% safe squares
    minedCounter = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            analysis = analyzeTile(x, y, findRealBombs=True)
            minedCounter += mineAllSafe(x, y, analysis)
    print("Mined: " + str(minedCounter))
    # If the program has no more moves it can make, stop it so it doesn't start clicking everywhere when either I click on a tile or the game is won.
    if (minedCounter == 0):
        break

    # Wait 0.7 seconds and also check if Q has been pressed. If Q is pressed, stop the script.
    stopAfterLoop = False
    startTime = time.time()
    while (time.time() - startTime < 0.7):
        if (keyboard.is_pressed("q")):
            stopAfterLoop = True
            break
    if (stopAfterLoop):
        break