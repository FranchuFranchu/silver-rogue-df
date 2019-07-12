import random
import runpy
import importlib
import builtins
import math

import pygame, sys
from pygame.locals import *
from autoclass import autoclass
from dict import dict

import spritesheets
import generate
import variable_declarations
from game_classes import BaseEntity, Map
from time import perf_counter
import nonblockingchinput

def runpy_import(file, globals_ = {}): # runpy.run_module, but delete special variables
    d = __import__(file).__dict__
    del d['__name__'] 
    del d['__spec__'] 
    del d['__file__']  
    del d['__cached__'] 
    del d['__loader__'] 
    del d['__package__'] 
    del d['__builtins__']
    del d['__doc__']
    return d

game = dict(**{
    "IS_FULLSCREEN": False,
    })
game.update(**runpy_import("variable_declarations"))


# Makes a grass entity
def Grass(x,y,z):
    ch = random.choice([',','\'','"'])
    ch = 'G:0:' + ch
    e = Entity(ch, x, y, z, True, -1)
    e.attrs.add('terrain')
    return e

class Entity(BaseEntity):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and kwargs == {}:
            if type(args[0]) == BaseEntity:
                e = args[0]
                self.char , self.x , self.y , self.z , self.passable , self.draw_index , self.slope , self.attrs =  e.char , e.x , e.y , e.z , e.passable , e.draw_index , e.slope , e.attrs 
                return
        BaseEntity.__init__(self, *args, **kwargs)
    def print(self):
        #log(self.x,self.y,self.z)
        global game
        if game.CHAR_H <= self.z + game.cameraz:
            return
        elif game.CHAR_W <= self.x + game.camerax:
            return
        if self.draw_index < game.zindex_buf[self.x][self.z]:
            return
        game.zindex_buf[self.x][self.z] = self.draw_index
        game.char_notation_blit(game,self.char, self.x + game.camerax, self.z + game.cameraz)
 

def update_mode():
    global game
    flags = 0
    flags |= pygame.FULLSCREEN if game.IS_FULLSCREEN else 0
    game.screen = pygame.display.set_mode((game.SCREEN_W, game.SCREEN_H), flags) # Create the game.screen

update_mode()

# These must be done after window creation


# Import ascii_pygame_game_fuctions with globals
import ascii_pygame_drawing_functions
game = dict(**game,**ascii_pygame_drawing_functions.__dict__)



@autoclass
class WorldTile:
    def __init__(self, char = ' ', x = 0, z = 0, worldseed = random.random() * 10 ** 6, passable = False, draw_index = 1, flatness = 0.4, town = False):
        pass
    def gen(self):
        # Generate the local map
        map_gened = generate.terrain.main(
            self.worldseed, 
            game.mapw, 
            game.maph, 
            self.x, 
            self.z, 
            flatness = self.flatness)


        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]

        game.entities = []
        for i in range(0,game.mapw):
            for j in range(0,game.maph):
                # i // 8 is to make the world a slope (a smooth one)
                game.entities.append(Grass(i,int(map_gened[i][j] * 10 + 10),j))
        game.entities = Map(game.entities)
        if self.town:
            game.entities.add(*[Entity(i) for i in generate.town.main(game.entities)])
        new_entities = Map(game.entities.d.values())
        # Generate slopes in the terrain "cliffs"
        for i in filter(lambda x: 'terrain' in x.attrs, game.entities.d.values()):
            # Search for adjacent tiles in the higher layer
            for e in (game.entities[i.x + 1, i.y + 1, i.z],game.entities[i.x + 1, i.y + 1, i.z + 1],game.entities[i.x - 1, i.y + 1, i.z],game.entities[i.x, i.y + 1, i.z - 1]):
                if e != None: # there is nothing on the tile
                    if 'terrain' in e.attrs: # make sure the tile is not the game.player or smth


                        game.entities[i.x, i.y, i.z].char = "G: 1F" # Up arrow
                        game.entities[i.x, i.y, i.z].slope = 1

                        if game.entities[e.x, i.y + 1, e.z]:
                            if 'terrain' in game.entities[e.x, i.y + 1, e.z].attrs:
                                continue
                            game.entities[e.x, i.y + 1, e.z].slope = -1
                            game.entities[e.x, i.y + 1, e.z].char = "G: 1E"
            # do the same but for lower layers
            for e in (game.entities[i.x + 1, i.y - 1, i.z],game.entities[i.x + 1, i.y - 1, i.z + 1],game.entities[i.x - 1, i.y - 1, i.z],game.entities[i.x, i.y - 1, i.z - 1]):
                if e != None: 
                    if 'terrain' in e.attrs:

                        game.entities[i.x, i.y, i.z].char = "G: 1E" # Up arrow
                        game.entities[i.x, i.y, i.z].slope = -1
                        if game.entities[e.x, i.y - 1, e.z]:
                            if 'terrain' in game.entities[e.x, i.y - 1, e.z].attrs:
                                continue
                            game.entities[e.x, i.y - 1, e.z].slope = 1
                            game.entities[e.x, i.y - 1, e.z].char = "G: 1F"
                        else:
                            pass
        game.entities = new_entities
        return new_entities
    def print(self):
        if game.CHAR_H <= self.z - game.cameraz:
            return
        elif game.CHAR_W <= self.x - game.camerax:
            return
        if self.draw_index < game.zindex_buf[self.x][self.z]:
            return
        game.zindex_buf[self.x][self.z] = self.draw_index 
        if self.town:
            self.char = '+' 
        game.char_notation_blit(game,self.char, self.x, self.z)      



class World(Map):
    def __init__(self, entity_list, seed = 3):
        self.d = {}
        for i in entity_list:
            self.d[i.x,i.z] = i
        self.seed = seed
    def add(self, *items):
        for i in items:
            i.worldseed = self.seed
            self.d[i.x,i.z] = i
    def __contains__(self,*items):
        for i in items:
            if type(i) == tuple:
                if len(i) == 2:
                    return self.d.has_key(i.x,i.z)
            else:
                return self.d[i.x,i.z] == i
    has = __contains__
    def __getitem__(self,item):
        if type(item) == tuple:
            if len(item) == 2:
                return self.d.get((item[0],item[1]))

    def remove(self,*items):
        for i in items:
            del self.d[i.x,i.z]

# Create world tile and game.entities
world = World([],seed = 1)
for i in range(0,game.worldw):
    for j in range(0,game.worldh):
        world.add(WorldTile('G:n',i,j))
world[2,2].town = True
game.player = Entity('@',0,0,0)
def regenerate_world_tile(playerx = 4, playerz = 4):
    worldtile = world[game.playerworldx,game.playerworldy]
    game.entities = worldtile.gen()
    game.player.y = game.entities.yproject(game.player.x, game.player.z)
    game.entities.add(game.player)
regenerate_world_tile()


def focus_camera(e):
    game.camerax = game.CHAR_W / 2 - e.x
    game.cameraz = game.CHAR_H / 2 - e.z
# Variables for the loop
pygame.display.flip()
clock = pygame.time.Clock()

# Player state variables
curr_view = 'play' # if the player is in a menu, etc.

tick = True

# These two are to avoid having to redraw the screen every tick the game.screen is being resized
videoResizeWasHappening = False
timeSinceVideoResize = 0

# Holding F11 behaviour
screenResizedUsingF11 = False

# Direction in a keypad 
# 7 8 9
# 4 5 6 # 5 means the game.player is standing still
# 1 2 3
direction = 5
last_player_pos = game.player.pos
dt = 0
tt = 0
tickc = 0

console_kb = nonblockingchinput.KBHit()

timeSinceKeyWasLastPressed = {}
pygame.key.set_repeat(0)

# Minified list of key names 
KEY_NAMES = { K_UNKNOWN: "UNKNOWN", "UNKNOWN": K_UNKNOWN, K_FIRST: "FIRST", "FIRST": K_FIRST, K_BACKSPACE: "BACKSPACE", "BACKSPACE": K_BACKSPACE, K_TAB: "TAB", "TAB": K_TAB, K_CLEAR: "CLEAR", "CLEAR": K_CLEAR, K_RETURN: "RETURN", "RETURN": K_RETURN, K_PAUSE: "PAUSE", "PAUSE": K_PAUSE, K_ESCAPE: "ESCAPE", "ESCAPE": K_ESCAPE, K_SPACE: "SPACE", "SPACE": K_SPACE, K_EXCLAIM: "EXCLAIM", "EXCLAIM": K_EXCLAIM, K_QUOTEDBL: "QUOTEDBL", "QUOTEDBL": K_QUOTEDBL, K_HASH: "HASH", "HASH": K_HASH, K_DOLLAR: "DOLLAR", "DOLLAR": K_DOLLAR, K_AMPERSAND: "AMPERSAND", "AMPERSAND": K_AMPERSAND, K_QUOTE: "QUOTE", "QUOTE": K_QUOTE, K_LEFTPAREN: "LEFTPAREN", "LEFTPAREN": K_LEFTPAREN, K_RIGHTPAREN: "RIGHTPAREN", "RIGHTPAREN": K_RIGHTPAREN, K_ASTERISK: "ASTERISK", "ASTERISK": K_ASTERISK, K_PLUS: "PLUS", "PLUS": K_PLUS, K_COMMA: "COMMA", "COMMA": K_COMMA, K_MINUS: "MINUS", "MINUS": K_MINUS, K_PERIOD: "PERIOD", "PERIOD": K_PERIOD, K_SLASH: "SLASH", "SLASH": K_SLASH, K_0: "0", "0": K_0, K_1: "1", "1": K_1, K_2: "2", "2": K_2, K_3: "3", "3": K_3, K_4: "4", "4": K_4, K_5: "5", "5": K_5, K_6: "6", "6": K_6, K_7: "7", "7": K_7, K_8: "8", "8": K_8, K_9: "9", "9": K_9, K_COLON: "COLON", "COLON": K_COLON, K_SEMICOLON: "SEMICOLON", "SEMICOLON": K_SEMICOLON, K_LESS: "LESS", "LESS": K_LESS, K_EQUALS: "EQUALS", "EQUALS": K_EQUALS, K_GREATER: "GREATER", "GREATER": K_GREATER, K_QUESTION: "QUESTION", "QUESTION": K_QUESTION, K_AT: "AT", "AT": K_AT, K_LEFTBRACKET: "LEFTBRACKET", "LEFTBRACKET": K_LEFTBRACKET, K_BACKSLASH: "BACKSLASH", "BACKSLASH": K_BACKSLASH, K_RIGHTBRACKET: "RIGHTBRACKET", "RIGHTBRACKET": K_RIGHTBRACKET, K_CARET: "CARET", "CARET": K_CARET, K_UNDERSCORE: "UNDERSCORE", "UNDERSCORE": K_UNDERSCORE, K_BACKQUOTE: "BACKQUOTE", "BACKQUOTE": K_BACKQUOTE, K_a: "a", "a": K_a, K_b: "b", "b": K_b, K_c: "c", "c": K_c, K_d: "d", "d": K_d, K_e: "e", "e": K_e, K_f: "f", "f": K_f, K_g: "g", "g": K_g, K_h: "h", "h": K_h, K_i: "i", "i": K_i, K_j: "j", "j": K_j, K_k: "k", "k": K_k, K_l: "l", "l": K_l, K_m: "m", "m": K_m, K_n: "n", "n": K_n, K_o: "o", "o": K_o, K_p: "p", "p": K_p, K_q: "q", "q": K_q, K_r: "r", "r": K_r, K_s: "s", "s": K_s, K_t: "t", "t": K_t, K_u: "u", "u": K_u, K_v: "v", "v": K_v, K_w: "w", "w": K_w, K_x: "x", "x": K_x, K_y: "y", "y": K_y, K_z: "z", "z": K_z, K_DELETE: "DELETE", "DELETE": K_DELETE, K_KP0: "KP0", "KP0": K_KP0, K_KP1: "KP1", "KP1": K_KP1, K_KP2: "KP2", "KP2": K_KP2, K_KP3: "KP3", "KP3": K_KP3, K_KP4: "KP4", "KP4": K_KP4, K_KP5: "KP5", "KP5": K_KP5, K_KP6: "KP6", "KP6": K_KP6, K_KP7: "KP7", "KP7": K_KP7, K_KP8: "KP8", "KP8": K_KP8, K_KP9: "KP9", "KP9": K_KP9, K_KP_PERIOD: "KP_PERIOD", "KP_PERIOD": K_KP_PERIOD, K_KP_DIVIDE: "KP_DIVIDE", "KP_DIVIDE": K_KP_DIVIDE, K_KP_MULTIPLY: "KP_MULTIPLY", "KP_MULTIPLY": K_KP_MULTIPLY, K_KP_MINUS: "KP_MINUS", "KP_MINUS": K_KP_MINUS, K_KP_PLUS: "KP_PLUS", "KP_PLUS": K_KP_PLUS, K_KP_ENTER: "KP_ENTER", "KP_ENTER": K_KP_ENTER, K_KP_EQUALS: "KP_EQUALS", "KP_EQUALS": K_KP_EQUALS, K_UP: "UP", "UP": K_UP, K_DOWN: "DOWN", "DOWN": K_DOWN, K_RIGHT: "RIGHT", "RIGHT": K_RIGHT, K_LEFT: "LEFT", "LEFT": K_LEFT, K_INSERT: "INSERT", "INSERT": K_INSERT, K_HOME: "HOME", "HOME": K_HOME, K_END: "END", "END": K_END, K_PAGEUP: "PAGEUP", "PAGEUP": K_PAGEUP, K_PAGEDOWN: "PAGEDOWN", "PAGEDOWN": K_PAGEDOWN, K_F1: "F1", "F1": K_F1, K_F2: "F2", "F2": K_F2, K_F3: "F3", "F3": K_F3, K_F4: "F4", "F4": K_F4, K_F5: "F5", "F5": K_F5, K_F6: "F6", "F6": K_F6, K_F7: "F7", "F7": K_F7, K_F8: "F8", "F8": K_F8, K_F9: "F9", "F9": K_F9, K_F10: "F10", "F10": K_F10, K_F11: "F11", "F11": K_F11, K_F12: "F12", "F12": K_F12, K_F13: "F13", "F13": K_F13, K_F14: "F14", "F14": K_F14, K_F15: "F15", "F15": K_F15, K_NUMLOCK: "NUMLOCK", "NUMLOCK": K_NUMLOCK, K_CAPSLOCK: "CAPSLOCK", "CAPSLOCK": K_CAPSLOCK, K_SCROLLOCK: "SCROLLOCK", "SCROLLOCK": K_SCROLLOCK, K_RSHIFT: "RSHIFT", "RSHIFT": K_RSHIFT, K_LSHIFT: "LSHIFT", "LSHIFT": K_LSHIFT, K_RCTRL: "RCTRL", "RCTRL": K_RCTRL, K_LCTRL: "LCTRL", "LCTRL": K_LCTRL, K_RALT: "RALT", "RALT": K_RALT, K_LALT: "LALT", "LALT": K_LALT, K_RMETA: "RMETA", "RMETA": K_RMETA, K_LMETA: "LMETA", "LMETA": K_LMETA, K_LSUPER: "LSUPER", "LSUPER": K_LSUPER, K_RSUPER: "RSUPER", "RSUPER": K_RSUPER, K_MODE: "MODE", "MODE": K_MODE, K_HELP: "HELP", "HELP": K_HELP, K_PRINT: "PRINT", "PRINT": K_PRINT, K_SYSREQ: "SYSREQ", "SYSREQ": K_SYSREQ, K_BREAK: "BREAK", "BREAK": K_BREAK, K_MENU: "MENU", "MENU": K_MENU, K_POWER: "POWER", "POWER": K_POWER, K_EURO: "EURO", "EURO": K_EURO, K_LAST: "LAST", "LAST": K_LAST}
##### BINDING HANDLING FUNCTIONS ######
game.view = 'play'

game.bindings = {
    'play': {

    }
}
game.dBindings = {
    'play': {

    }
}

game.heldBindings = {
    'play': {
    
    }
}
game.pressed = {}

def bind(view, combination, function, *args, **kwargs):
    if game.bindings.get(view):
        game.bindings[view][combination.upper()] = lambda: function(*args, **kwargs)
    else:
        game.bindings[view] = {}
        game.bindings[view][combination.upper()] = lambda: function(*args, **kwargs)

def hbind(view, combination, function, *args, **kwargs):
    if game.heldBindings.get(view):
        game.heldBindings[view][combination.upper()] = lambda: function(*args, **kwargs)
    else:
        game.heldBindings[view] = {}
        game.heldBindings[view][combination.upper()] = lambda: function(*args, **kwargs)

def dbind(view, combination, function, *args, **kwargs):
    if game.dBindings.get(view):
        game.dBindings[view][combination.upper()] = lambda: function(*args, **kwargs)
    else:
        game.dBindings[view] = {}
        game.dBindings[view][combination.upper()] = lambda: function(*args, **kwargs)


def handleBindingUp(event):
    name = KEY_NAMES[event.key]
    viewBindings = game.bindings[game.view]
    for i in filter(lambda i: name in i.split('-'),viewBindings.keys()):
        i = i.upper()
        comb = i
        comb_keys = i.split('-')
        all_keys_pressed = True
        for i in filter(lambda i: i in comb_keys, KEY_NAMES.keys()):
            if not game.pressed.get(KEY_NAMES[i]):
                all_keys_pressed = False
                break
        if all_keys_pressed:
            viewBindings[comb]()   
    if game.pressed.get(event.key):
        del game.pressed[event.key]
def handleBindingDown(event):
    game.pressed[event.key] = True
    name = KEY_NAMES[event.key]
    viewBindings = game.dBindings[game.view]

    for i in filter(lambda i: name in i.split('-'),viewBindings.keys()):
        i = i.upper()
        comb = i
        comb_keys = i.split('-')
        all_keys_pressed = True
        for i in filter(lambda i: i in comb_keys, KEY_NAMES.keys()):
            if not game.pressed.get(KEY_NAMES[i]):
                all_keys_pressed = False
                break
        if all_keys_pressed:
            viewBindings[comb]()    

def listHeldBindings(): # Return a list of functions that need to be run now
    functions = []
    viewBindings = game.heldBindings[game.view]
    for key in game.pressed.keys():
        if type(key) == int:
            key = KEY_NAMES[key]
        for i in filter(lambda i: key in i.split('-'),viewBindings.keys()):
            i = i.upper()
            comb = i
            comb_keys = i.split('-')
            all_keys_pressed = True
            for i in filter(lambda i: (i.upper() if type(i) == str else i) in comb_keys, KEY_NAMES.keys()):
                if not game.pressed.get(KEY_NAMES[i]):
                    all_keys_pressed = False
                    break
            if all_keys_pressed:
                functions.append(viewBindings[comb.upper()])
    return functions

def addScreen(direction):
    global game
    if game.get('resize_amount') != None:
        game.resize_amount += 1
    else:
        game.resize_amount = 0

def resizeScreen(direction):
    resize_amount = game.resize_amount
    game.resize_amount = 0
    if direction == 8:
        game.CHAR_H -= resize_amount
    elif direction == 2:
        game.CHAR_H += resize_amount
    elif direction == 4:
        game.CHAR_W -= resize_amount
    elif direction == 6:
        game.CHAR_W += resize_amount
    game.SCREEN_H = game.TILE_H * game.CHAR_H
    game.SCREEN_W = game.TILE_W * game.CHAR_W
    direction = 0
    update_mode()

bind('play', 'rshift-up', resizeScreen, 8)
bind('play', 'rshift-down', resizeScreen, 2)
bind('play', 'rshift-right',resizeScreen, 6)
bind('play', 'rshift-left', resizeScreen, 4)
hbind('play', 'rshift-up', addScreen, 8)
hbind('play', 'rshift-down', addScreen, 2)
hbind('play', 'rshift-right',addScreen, 6)
hbind('play', 'rshift-left', addScreen, 4)
################ MAIN LOOP ####################################
while True:
    stime = perf_counter()
    #if console_kb.kbhit():
    #   print(console_kb.getch())
    for i in listHeldBindings():
        i()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            game.SCREEN_H = event.h
            game.SCREEN_W = event.w
            game.CHAR_H = int(game.SCREEN_H / game.TILE_H)
            game.CHAR_W = int(game.SCREEN_W / game.TILE_W)
            videoResizeWasHappening = True
            timeSinceVideoResize = 0
            game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
            update_mode()
            for i in game.entities:
                if game.player.y == i.y:
                    i.print() 
        elif event.type == KEYDOWN:
            handleBindingDown(event)
            mods = pygame.key.get_mods()
            timeSinceKeyWasLastPressed[event.key, mods] = tickc
            if curr_view == 'play':
                tick = True
                if event.key == K_UP:
                    direction = 8
                elif event.key == K_DOWN:
                    direction = 2
                elif event.key == K_LEFT:
                    direction = 4
                elif event.key == K_RIGHT:
                    direction = 6

        elif event.type == KEYUP:
            handleBindingUp(event)
            mods = pygame.key.get_mods()
            try:
                del timeSinceKeyWasLastPressed[event.key, mods]
            except KeyError:
                pass
            if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                direction = 5
            elif mods & KMOD_SHIFT:
                if event.key == K_m:
                    # Map or travel
                    if curr_view != 'play':
                        curr_view = 'play'
                    else:
                        curr_view = 'map'
                    tick = True
                if event.key == K_q:
                    print(game.player)

            elif event.key == K_F11:
                if not screenResizedUsingF11:
                    #game.IS_FULLSCREEN = not game.IS_FULLSCREEN
                    update_mode()
                screenResizedUsingF11 = False
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    timeSinceVideoResize += 1
    if direction != 5 and game.MOVE_WHEN_HELD:
        tick = True
        if timeSinceKeyWasLastPressed == {}:
            direction = 5
    if timeSinceVideoResize > 10 and videoResizeWasHappening:
        tick = True
        videoResizeWasHappening = False
    tickc += 1
    if curr_view == 'play': # Local view
        if tick:
            tile_at_player = game.entities[game.player.pos]
            def move_player_according_to_direction(tile_at_player, last_player_pos):
                if direction == 2:
                    game.player.z += 1
                if direction == 4:
                    game.player.x -= 1
                    
                if direction == 6:
                    game.player.x += 1
                    
                if direction == 8:
                    game.player.z -= 1


                if not tile_at_player:
                    game.player.x, game.player.y, game.player.z = last_player_pos
                    tile_at_player = game.entities[last_player_pos] 
                    return tile_at_player, 'a'


                if direction != 5:
                    game.player.y += tile_at_player.slope
                if game.entities[game.player.x, game.player.y, game.player.z]:
                    if game.entities[game.player.x, game.player.y, game.player.z].passable == False:
                        game.player.x, game.player.y, game.player.z = tile_at_player.x, tile_at_player.y, tile_at_player.z                    


                # Did the player walk out of the map?
                if game.player.x < 0:
                    game.playerworldx -= 1
                    game.player.x = game.mapw - 1
                    regenerate_world_tile(game.player.x, game.player.z)
                if game.player.z < 0:
                    game.playerworldy -= 1
                    game.player.z = game.maph - 1
                    regenerate_world_tile(game.player.x, game.player.z)
                if game.player.x >= game.mapw:
                    game.playerworldx += 1
                    game.player.x = 0
                    regenerate_world_tile(game.player.x, game.player.z)
                if game.player.z >= game.maph:
                    game.playerworldy += 1
                    game.player.z = 0
                    regenerate_world_tile(game.player.x, game.player.z)

                # Trick to undo game.player Y movement if game.player stepped from a slope in the reverse direction
                if game.entities[game.player.x, game.player.y, game.player.z] == None:
                    if tile_at_player.slope != 0:
                        game.player.y -= tile_at_player.slope
                    return
                        
                # Trick to undo game.player Y movement if the game.player is walking parallel to the slope
                if game.entities[game.player.x, game.player.y, game.player.z].slope == tile_at_player.slope:
                    if direction != 5:
                        game.player.y -= tile_at_player.slope
                return tile_at_player

            tile_at_player = move_player_according_to_direction(tile_at_player, last_player_pos)
            if tile_at_player == None:
                # skip graphics tick
                continue

            if type(tile_at_player) == tuple:
                if tile_at_player[1] == 'a':
                    # The player has encountered a cliff
                    tile_at_player = tile_at_player[0]
                    focus_camera(game.player)

        if tick: # Graphics tick, redraw and stuff. Split it from the main tick when the game gets too large
            # Move camera
            focus_camera(game.player)
            game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
            game.screen.fill((0,0,0)) # TODO only redraw everything if the game.camera has moved
            for i in game.entities:
                
                if game.player.y == i.y:
                    i.print() 
                
            game.char_notation_blit(game, 'FPS - ' + str(dt)[:5],0, 0)
            game.char_notation_blit(game, 'Time taken - ' + str(tt)[:5],0, 1)
            pygame.display.update()

        if tick:
            last_player_pos = tile_at_player.x, tile_at_player.y, tile_at_player.z
    elif curr_view == 'map':
        if tick:
            for i in world:
                i.print()
            game.char_notation_blit(game,'@', game.playerworldx, game.playerworldy)
            pygame.display.update()
    etime = perf_counter()
    pygame.display.update()
    dt = (-1 / (((etime - stime))))
    tt = (etime - stime)
    tick = False
    if dt < 30:
        dt = 30
    pygame.event.pump()
    clock.tick(30)