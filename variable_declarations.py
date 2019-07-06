TILE_W = 12 # Tile size, in pixels
TILE_H = 12
CHAR_W = 18 # Screen size, in tiles
CHAR_H = 18    

# Screen size, in pixels
SCREEN_W = TILE_W * CHAR_W
SCREEN_H = TILE_H * CHAR_H

# If the player should move when an arrow key is held
MOVE_WHEN_HELD = True

# Default map width and height for a local map
mapw = 64
maph = 64

# Player position in local map
playerx = 10
playery = 10
playerz = 10

# Player position in the world
playerworldx = 2
playerworldy = 2

# Camera position
camerax = 0
cameraz = 0

# Size in local maps of the whole world
# (the world is supposed to be round, not yet implemented)
worldw = 48
worldh = 48

# this is a 2-dimensional array for the z-index of things:
# i.e., the player has to be drawn above grass
zindex_buf = [[-100 for _ in range(maph)] for _ in range(mapw)]
# I made a way to add foreground and background colors to entitities easily
# i'll call it "Color notation" here
# It works as follows:
#   - A colored tile is represented by a string
#   - The string has the format [foreground[:background]:]character
#   - If the character starts with whitespace, then interpret the rest of string as an hexadecimal representation of the character
#   - Examples:
#       - R:@ = Red "@"
#       - B:G:w = Blue "w" with a green background
#       - Y: 2741 = a yellow Unicode 0x2741: Flower emoji

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
