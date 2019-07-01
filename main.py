import random

import pygame, sys
from pygame.locals import *
from autoclass import autoclass

import spritesheets


pygame.init()

IS_FULLSCREEN = False

TILE_W = 12 # Tile size, in pixels
TILE_H = 12
CHAR_W = 48 # Screen size, in tiles
CHAR_H = 18    

# Screen size, in pixels
SCREEN_W = TILE_W * CHAR_W
SCREEN_H = TILE_H * CHAR_H

# this is a 2-dimensional array for the z-index of things:
# i.e., the player has to be drawn above grass
zindex_buf = [[-100 for _ in range(CHAR_H)] for _ in range(CHAR_W)]

# I made a way to add foreground and background colors to entitities easily
# i'll call it "Color notation" here
# It works as follows:
#   - A colored tile is represented by a string
#   - The string has the format [foreground[:background]:]character
#   - Examples:
#       - R:@ = Red "@"
#       - B:G:w = Blue "w" with a green background

COLOR_MAP = {
    "0": (0,0,0),
    "R": (255,0,0),
    "G": (0,255,0),
    "Y": (255,255,0),
    "B": (0,0,255),
    "M": (255,0,255),
    "C": (0,255,255),
    "W": (255,255,255)
}

SPRT_RECT_X = 12 * 4  
SPRT_RECT_Y = 12 * 4
# This is where the sprite is found on the sheet

LEN_SPRT_X = 12
LEN_SPRT_Y = 12
# This is the length of the sprite
screen = None
def update_mode():
    global screen
    flags = RESIZABLE
    flags |= FULLSCREEN if IS_FULLSCREEN else 0
    screen = pygame.display.set_mode((SCREEN_H, SCREEN_W), flags) # Create the screen

update_mode()

sheet = spritesheets.spritesheet('tileset.png') # Load the sheet
backdrop = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)

# Gets the surface in the tileset for a specific character
def get_surf(pos, fgcol = 'W', bgcol = '0'):
    if type(pos) == str:
        pos = ord(pos)
    fgcol = COLOR_MAP[fgcol]
    bgcol = COLOR_MAP[bgcol]
    upper = (pos & 0xF0) / 16 # Upper bits determine row
    lower = pos & 0x0F # Lower bits determine column
    surf = sheet.image_at(((TILE_H * lower), (TILE_W * upper), TILE_W, TILE_H))
    arr = pygame.PixelArray(surf)
    arr.replace((255,0,255), bgcol)
    arr.replace((255,255,255), fgcol)
    del arr
    return surf

# Prints a character at a tile
def blit_char_at(char, tx, ty, fgcol = 'W', bgcol = '0'):
    global screen
    rect = pygame.Rect(tx * TILE_W, ty * TILE_H, TILE_W, TILE_H)
    screen.blit(get_surf(char,fgcol,bgcol), rect)

# Calls blit_char_at, but uses color notation
def char_notation_blit(col, tx, ty):
    global screen
    k = col.split(':')
    if len(k) == 1:
        blit_char_at(col,tx,ty)
    elif len(k) == 2:
        blit_char_at(k[1],tx,ty,k[0])
    elif len(k) == 3:
        blit_char_at(k[2],tx,ty,k[0], k[1])
    return True

@autoclass
class Entity:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, passable = False, draw_index = 0):
        pass
    def print(self):
        #log(self.x,self.y,self.z)
        if CHAR_H <= self.z:
            return
        elif CHAR_W <= self.x:
            return
        if self.draw_index < zindex_buf[self.x][self.z]:
            return
        zindex_buf[self.x][self.z] = self.draw_index
        char_notation_blit(self.char, self.x, self.z)

# Makes a grass entity
def Grass(x,y,z):
    ch = random.choice([',','\'','"'])
    ch = 'G:0:' + ch
    return Entity(ch, x, y, z, True, -1)

# Create the cute world the player is in
mapw = 64
maph = 64

player = Entity('@',5,1,5)
evil   = Entity('R:E',10,1,5)
entities = [player, evil]
for i in range(0,mapw):
    for j in range(0,maph):
        entities.append(Grass(i,0,j))
for i in entities:
    i.print()


# Variables for the loop
pygame.display.flip()
clock = pygame.time.Clock()


tick = True

# These two are to avoid having to redraw the screen every tick the screen is being resized
videoResizeWasHappening = False
timeSinceVideoResize = 0
# Direction in a keypad 
# 7 8 9
# 4 5 6 # 5 means the player is still
# 1 2 3
direction = 5
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            SCREEN_H = event.h
            SCREEN_W = event.w
            CHAR_H = int(SCREEN_H / TILE_H)
            CHAR_W = int(SCREEN_W / TILE_W)
            videoResizeWasHappening = True
            timeSinceVideoResize = 0
            zindex_buf = [[-100 for _ in range(CHAR_H)] for _ in range(CHAR_W)]
            update_mode()
            for i in entities:
                i.print()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                direction = 8
            elif event.key == K_DOWN:
                direction = 2
            elif event.key == K_LEFT:
                direction = 4
            elif event.key == K_RIGHT:
                direction = 6
        elif event.type == KEYUP:
            if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                direction = 5

            if event.key == K_F11:
                IS_FULLSCREEN = not IS_FULLSCREEN
                update_mode()
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    timeSinceVideoResize += 1
    if direction != 5:
        tick = True
    if timeSinceVideoResize > 10 and videoResizeWasHappening:
        tick = True
        videoResizeWasHappening = False
    if tick:
        if direction == 2:
            player.z += 1
        if direction == 4:
            player.x -= 1
            
        if direction == 6:
            player.x += 1
            
        if direction == 8:
            player.z -= 1
    if tick: # Graphics tick, redrawing and stuff
        zindex_buf = [[-100 for _ in range(CHAR_H)] for _ in range(CHAR_W)]

        for i in entities:
            i.print()
            

        pygame.display.update()
    tick = False
    clock.tick(30)