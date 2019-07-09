import pygame
import spritesheets
from builtins import *
# This should be imported after pygame is initialized

sheet = spritesheets.spritesheet('tileset.png')
# Gets the surface in the tileset for a specific character
def get_surf(game, pos, fgcol = 'W', bgcol = '0'):
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
def blit_char_at(game, char, tx, ty, fgcol = 'W', bgcol = '0'):
    rect = pygame.Rect(tx * game.TILE_W, ty * game.TILE_H, game.TILE_W, game.TILE_H)
    game.screen.blit(get_surf(game, char,fgcol,bgcol), rect)

# Converts color notation to a (char, fg, bg) tuple
def char_not_to_cfg(col):
    if type(col) == int:
        return col, 'W', '0'

    k = col.split(':')
    if k[-1][0] == ' ' and len(k[-1]) > 1:
        k[-1] = chr(int(k[-1][1:], 16)) # Convert to base-16 int, then get the corresponding character
    if len(k) == 1:
        return (col, 'W', '0')
    elif len(k) == 2:
        return (k[1],k[0],'0')
    elif len(k) == 3:
        return (k[2],k[0], k[1])
# Calls blit_char_at, but uses color notation
def char_notation_blit(game, col, tx, ty):
    cfg = char_not_to_cfg(col)
    tx = int(tx)
    ty = int(ty)
    if type(cfg[0]) == int:
        blit_char_at(game, cfg[0], tx, ty, cfg[1], cfg[2])
    else:
        for x, char in zip( \
            range(tx, tx + len(cfg[0])), \
            cfg[0] \
            ):
            blit_char_at(game, char, x, ty, cfg[1], cfg[2])
