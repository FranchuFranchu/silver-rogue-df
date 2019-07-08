import pygame
import spritesheets
# This should be imported after pygame is initialized

sheet = spritesheets.spritesheet('tileset.png')
# Gets the surface in the tileset for a specific character
def get_surf(pos, fgcol = 'W', bgcol = '0'):
    if type(pos) == str:
        pos = ord(pos)
    fgcol = game.COLOR_MAP[fgcol]
    bgcol = game.COLOR_MAP[bgcol]
    upper = (pos & 0xF0) / 16 # Upper bits determine row
    lower = pos & 0x0F # Lower bits determine column
    surf = sheet.image_at(((game.TILE_H * lower), (game.TILE_W * upper), game.TILE_W, game.TILE_H))
    arr = pygame.PixelArray(surf)
    arr.replace((255,0,255), bgcol)
    arr.replace((255,255,255), fgcol)
    del arr
    return surf

# Prints a character at a tile
def blit_char_at(char, tx, ty, fgcol = 'W', bgcol = '0'):
    rect = pygame.Rect(tx * game.TILE_W, ty * game.TILE_H, game.TILE_W, game.TILE_H)
    game.screen.blit(get_surf(char,fgcol,bgcol), rect)

# Calls blit_char_at, but uses color notation
def char_notation_blit(col, tx, ty):
    if type(col) == int:
        blit_char_at(col,tx,ty)
        return True

    k = col.split(':')
    if k[-1][0] == ' ' and len(k[-1]) > 1:
        k[-1] = chr(int(k[-1][1:], 16)) # Convert to base-16 int, then get the corresponding character
    if len(k) == 1:
        blit_char_at(col,tx,ty)
    elif len(k) == 2:
        blit_char_at(k[1],tx,ty,k[0])
    elif len(k) == 3:
        blit_char_at(k[2],tx,ty,k[0], k[1])
    return True
