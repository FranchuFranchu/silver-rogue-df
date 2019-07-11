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


################ MAIN LOOP ####################################
while True:
    stime = perf_counter()
    #if console_kb.kbhit():
    #   print(console_kb.getch())
    if 1:
        keys = pygame.key.get_pressed()
        if keys[K_RSHIFT]:
            if keys[K_UP]:
                game.CHAR_H -= 1
            elif keys[K_DOWN]:
                game.CHAR_H += 1
            elif keys[K_LEFT]:
                game.CHAR_W -= 1
            elif keys[K_RIGHT]:
                game.CHAR_W += 1
            game.SCREEN_H = game.TILE_H * game.CHAR_H
            game.SCREEN_W = game.TILE_W * game.CHAR_W
            direction = 0
            update_mode()
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