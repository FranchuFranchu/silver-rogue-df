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
import graphics
import bind_utils

# Makes a grass entity
def Grass(game, x,y,z):
    ch = random.choice([',','\'','"'])
    ch = 'G:0:' + ch
    e = Entity(game, ch, x, y, z, True, -1)
    e.attrs.add('terrain')
    return e
class GameObjectFeature:
    def regenerate_world_tile(game, playerx = 4, playerz = 4):
        game.worldtile = game.world[game.playerworldx,game.playerworldy]
        game.entities = game.worldtile.gen()
        print(game.entities)
        game.player.y = game.entities.yproject(game.player.x, game.player.z)
        game.entities.add(game.player)
class Entity(BaseEntity):
    def __init__(self, game, *args, **kwargs):
        if len(args) == 2 and kwargs == {}:
            if type(args[1]) == BaseEntity:
                e = args[1]
                self.char , self.x , self.y , self.z , self.passable , self.draw_index , self.slope , self.attrs =  e.char , e.x , e.y , e.z , e.passable , e.draw_index , e.slope , e.attrs 
                return
        self.game = game
        BaseEntity.__init__(self, *args, **kwargs)
    def print(self):
        #log(self.x,self.y,self.z)
        if self.game.CHAR_H <= self.z + self.game.cameraz:
            return
        elif self.game.CHAR_W <= self.x + self.game.camerax:
            return
        if self.draw_index < self.game.zindex_buf[self.x][self.z]:
            return
        self.game.zindex_buf[self.x][self.z] = self.draw_index
        self.game.char_notation_blit(self.char, self.x + self.game.camerax, self.z + self.game.cameraz)

@autoclass
class WorldTile:
    def __init__(self, game, char = ' ', x = 0, z = 0, worldseed = random.random() * 10 ** 6, passable = False, draw_index = 1, flatness = 0.4, town = False):
        pass
    def gen(self):
        # Generate the local map
        map_gened = generate.terrain.main(
            self.worldseed, 
            self.game.mapw, 
            self.game.maph, 
            self.x, 
            self.z, 
            flatness = self.flatness)


        self.game.zindex_buf = [[-100 for _ in range(self.game.maph)] for _ in range(self.game.mapw)]

        self.game.entities = []
        for i in range(self.game.mapw):
            for j in range(self.game.maph):
                # i // 8 is to make the world a slope (a smooth one)
                self.game.entities.append(Grass(self.game, i,int(map_gened[i][j] * 10 + 10),j))
        self.game.entities = Map(self.game.entities)
        self.town = False
        if self.town:
            self.game.entities.add(*[Entity(self.game, i) for i in generate.town.main(self.game.entities)])
        new_entities = Map(self.game.entities.d.values())
        # Generate slopes in the terrain "cliffs"
        for i in filter(lambda x: 'terrain' in x.attrs, self.game.entities.d.values()):
            # Search for adjacent tiles in the higher layer
            for e in (self.game.entities[i.x + 1, i.y + 1, i.z],self.game.entities[i.x + 1, i.y + 1, i.z + 1],self.game.entities[i.x - 1, i.y + 1, i.z],self.game.entities[i.x, i.y + 1, i.z - 1]):
                if e != None: # there is nothing on the tile
                    if 'terrain' in e.attrs: # make sure the tile is not the self.game.player or smth


                        self.game.entities[i.x, i.y, i.z].char = "G: 1F" # Up arrow
                        self.game.entities[i.x, i.y, i.z].slope = 1

                        if self.game.entities[e.x, i.y + 1, e.z]:
                            if 'terrain' in self.game.entities[e.x, i.y + 1, e.z].attrs:
                                continue
                            self.game.entities[e.x, i.y + 1, e.z].slope = -1
                            self.game.entities[e.x, i.y + 1, e.z].char = "G: 1E"
            # do the same but for lower layers
            for e in (self.game.entities[i.x + 1, i.y - 1, i.z],self.game.entities[i.x + 1, i.y - 1, i.z + 1],self.game.entities[i.x - 1, i.y - 1, i.z],self.game.entities[i.x, i.y - 1, i.z - 1]):
                if e != None: 
                    if 'terrain' in e.attrs:

                        self.game.entities[i.x, i.y, i.z].char = "G: 1E" # Up arrow
                        self.game.entities[i.x, i.y, i.z].slope = -1
                        if self.game.entities[e.x, i.y - 1, e.z]:
                            if 'terrain' in self.game.entities[e.x, i.y - 1, e.z].attrs:
                                continue
                            self.game.entities[e.x, i.y - 1, e.z].slope = 1
                            self.game.entities[e.x, i.y - 1, e.z].char = "G: 1F"
                        else:
                            pass
        self.game.entities = new_entities
        return new_entities
    def print(self):
        if self.game.CHAR_H <= self.z - self.game.cameraz:
            return
        elif self.game.CHAR_W <= self.x - self.game.camerax:
            return
        if self.draw_index < self.game.zindex_buf[self.x][self.z]:
            return
        self.game.zindex_buf[self.x][self.z] = self.draw_index 
        if self.town:
            self.char = '+' 
        self.game.char_notation_blit(self.char, self.x, self.z)      






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



class ScreenResizingFeature:
    def addScreen(game, direction):
        if game.get('resize_amount') != None:
            game.resize_amount += 1
        else:
            game.resize_amount = 0

    def resizeScreen(game, direction):
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

class MainGame(
    variable_declarations.VariableDeclarations,
                 graphics.GraphicsFeature,
               bind_utils.BindingFeature,
                          GameObjectFeature,
                          ScreenResizingFeature,

    ):
    def init(self):
        pygame.display.init()
        self.init_vars()
        self.update_mode()
        self.graphics_init()
        # Create world tile and game.entities

        wtiles = []
        for i in range(self.worldw):
            for j in range(self.worldh):
                wtiles.append(WorldTile(self, 'G:n',i,j))

        self.world = World(wtiles,seed = 1)
        self.world[2,2].town = True
        self.player = Entity(self, '@', 0, 0, 0)
        
        self.regenerate_world_tile()
        """
        self.bind('play', 'rshift-up', resizeScreen, 8)
        self.bind('play', 'rshift-down', resizeScreen, 2)
        self.bind('play', 'rshift-right',resizeScreen, 6)
        self.bind('play', 'rshift-left', resizeScreen, 4)
        self.hbind('play', 'rshift-up', addScreen, 8)
        self.hbind('play', 'rshift-down', addScreen, 2)
        self.hbind('play', 'rshift-right',addScreen, 6)
        self.hbind('play', 'rshift-left', addScreen, 4)
        """
    def run(game):
        # Variables for the loop
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
        ################ MAIN LOOP ####################################
        while True:
            stime = perf_counter()
            #if console_kb.kbhit():
            #   print(console_kb.getch())
            for i in game.listHeldBindings():
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
                    game.update_mode()
                    for i in game.entities:
                        if game.player.y == i.y:
                            i.print() 
                elif event.type == KEYDOWN:
                    game.handleBindingDown(event)
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
                    game.handleBindingUp(event)
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
                            game.update_mode()
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
                            game.regenerate_world_tile(game.player.x, game.player.z)
                        if game.player.z < 0:
                            game.playerworldy -= 1
                            game.player.z = game.maph - 1
                            game.regenerate_world_tile(game.player.x, game.player.z)
                        if game.player.x >= game.mapw:
                            game.playerworldx += 1
                            game.player.x = 0
                            game.regenerate_world_tile(game.player.x, game.player.z)
                        if game.player.z >= game.maph:
                            game.playerworldy += 1
                            game.player.z = 0
                            game.regenerate_world_tile(game.player.x, game.player.z)

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
                            game.focus_camera(game.player)

                if tick: # Graphics tick, redraw and stuff. Split it from the main tick when the game gets too large
                    # Move camera
                    game.focus_camera(game.player)
                    game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
                    game.screen.fill((0,0,0)) # TODO only redraw everything if the game.camera has moved
                    for i in game.entities:
                        
                        if game.player.y == i.y:
                            i.print() 
                        
                    game.char_notation_blit('FPS - ' + str(dt)[:5],0, 0)
                    game.char_notation_blit('Time taken - ' + str(tt)[:5],0, 1)
                    pygame.display.update()

                if tick:
                    last_player_pos = tile_at_player.x, tile_at_player.y, tile_at_player.z
            elif curr_view == 'map':
                if tick:
                    for i in world:
                        i.print()
                    game.char_notation_blit('@', game.playerworldx, game.playerworldy)
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


if __name__ == '__main__':
    theMainGame = MainGame()
    theMainGame.init()
    theMainGame.run()