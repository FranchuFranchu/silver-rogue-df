import random
import math
from time import perf_counter
from itertools import product
from functools import partial
from copy import deepcopy
from pprint import pformat

import pygame, sys
from pygame.locals import *
from autoclass import autoclass

import spritesheets
import generate
import nonblockingchinput

# Import classes
from game_classes import BaseMapTile, Map, BaseEntity
from drawable_game_classes import MapTile, World, WorldTile, Entity

# Import features
from variable_declarations import VariableDeclarations
from pygame_g import GraphicsFeature
from bind_utils import BindingFeature
from screen_resizing import ScreenResizingFeature
from graphics import SelectionList

class DrawMapFeature:
    def drawMap(game):
        for i in game.entities:
            if game.player.y == i.y:
                i.print() 
                for e in i.entities:
                    e.print()

class GameObjectFeature:
    def regenerate_world_tile(game, playerx = 4, playerz = 4):
        game.worldtile = game.world[game.playerworldx,game.playerworldy]
        game.entities = game.worldtile.gen()
        game.player.y = game.entities.yproject(game.player.x, game.player.z)
        game.entities.add(game.player)

class AnnouncementFeature:
    def blit_announcements(game):

        # Find out how much announcements fit in the box
        free_lines = game.ANNOUNCEMENT_H
        fitting_announcements = 0
        for i in game.announcements[::-1]:
            if free_lines < 1:
                break
            free_lines -= math.ceil(len(i) / game.ANNOUNCEMENT_W)
            fitting_announcements += 1
        # print them
        for y, i in enumerate(game.announcements[-fitting_announcements:][::-1]):
            game.blit_str_at(i, 0, game.CHAR_H - 1 - y)


class PlayViewTickFeature:
    def playv_tick(game):
        if game.tile_at_player == None:
            # skip graphics game.tick
           return

        if type(game.tile_at_player) == tuple:
            if game.tile_at_player[1] == 'a':
                # The player has encountered a cliff
                game.tile_at_player = game.tile_at_player[0]
                game.focus_camera(game.player)

        # Move camera
        game.focus_camera(game.player)
        
        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
        game.screen.fill((0,0,0)) # TODO only redraw everything if the game.camera has moved

        game.drawMap()
        game.char_notation_blit('@', game.camerax + game.player.x , game.player.z + game.cameraz)
            
        game.last_player_pos = game.tile_at_player.x, game.tile_at_player.y, game.tile_at_player.z

class LookingFeature:
    def lookv_tick(game):
        if not hasattr(game, 'cursor_e'):
            game.cursor_e = MapTile(game, 'X', game.player.x, game.player.y, game.player.z, draw_index = 1000)

        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
        game.screen.fill((0,0,0))
        game.drawMap()

        game.cursor_e.print()
        game.blit_str_at(', '.join([str(i) for i in game.cursor_e.pos]), 0, 0)
    def move_cursor(game, direction):
        game.direction = direction
        game.tick = True

        if game.direction == 2:
            game.cursor_e.z += 1
        if game.direction == 4:
            game.cursor_e.x -= 1
            
        if game.direction == 6:
            game.cursor_e.x += 1
            
        if game.direction == 8:
            game.cursor_e.z -= 1

        if game.direction == 10:
            game.cursor_e.y -= 1

        elif game.direction == 11:
            game.cursor_e.y += 1
        game.focus_camera(game.cursor_e)
        

    def talkedWithPerson(game, what):
        game.announcements.append("You: " + game.talking_list.items[what])
        game.announcements.append(game.entities[game.cursor_e.pos].entities[0].desc + ': Hi')
        game.setView('play')
        game.drawMap()
    def talkWithPerson(game):
        e = game.entities[game.cursor_e.pos]
        game.drawMap()
        if len(e.entities) == 0:
            game.announcements.append("There is no one to talk with here")
        else:
            game.talking_list.display()

class GameToStringFeature:
    def game_to_string(game, where = '', depth = 1, tab = 1):
        d = game.__dict__.copy()
        if where != '':

            d = d[where]
        s = ''

        if isinstance(d, list):
            ditems = enumerate(d)
        elif isinstance(d, dict):
            ditems = d.items()
        for k, v in ditems:
            s += '\t' * tab + str(k) + ': '
            if isinstance(v, dict) or isinstance(v, list):
                if depth <= 1:
                    s += ' <...>'
                else:
                    s += game.game_to_string(k, depth - 1, tab + 1)
            else:
                s += str(v) 
            s += ',\n'
        return s
class VideoResizeHandlerFeature:
    def handle_video_resize(game, event):
        game.SCREEN_H = event.h
        game.SCREEN_W = event.w
        game.CHAR_H = int(game.SCREEN_H / game.TILE_H)
        game.CHAR_W = int(game.SCREEN_W / game.TILE_W)
        videoResizeWasHappening = True
        timeSinceVideoResize = 0
        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
        game.update_mode()
        game.drawMap()

class ViewSwitchFunctionsFeature:
    # Functions to switch between Views using lambdas
    def setView(game, view):
        game.curr_view = view
        game.tick_according_to_current_view()

class MainGame(
    VariableDeclarations,
    GraphicsFeature,
    BindingFeature,
    GameObjectFeature,
    ScreenResizingFeature,
    ViewSwitchFunctionsFeature,
    PlayViewTickFeature,
    LookingFeature,
    GameToStringFeature,
    AnnouncementFeature,
    DrawMapFeature
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
        self.bind('*',  'rshift-up',   self.resizeScreen, 8)
        self.bind('*',  'rshift-down', self.resizeScreen, 2)
        self.bind('*',  'rshift-right',self.resizeScreen, 6)
        self.bind('*',  'rshift-left', self.resizeScreen, 4)
        self.hbind('*', 'rshift-up',   self.addScreen, 8)
        self.hbind('*', 'rshift-down', self.addScreen, 2)
        self.hbind('*', 'rshift-right',self.addScreen, 6)
        self.hbind('*', 'rshift-left', self.addScreen, 4)
        self.hbind('play', 'up',   self.movePlayerAccordingToDirection, 8)
        self.hbind('play', 'down', self.movePlayerAccordingToDirection, 2)
        self.hbind('play', 'right',self.movePlayerAccordingToDirection, 6)
        self.hbind('play', 'left', self.movePlayerAccordingToDirection, 4)
        self.bind('play', 'p',    lambda g: print(g.player, g.tile_at_player), self)
        self.bind('play', 'l', partial(self.setView, 'look'))
        self.bind('look', 'l', partial(self.setView, 'play'))
        self.hbind('look', 'up',   self.move_cursor, 8)
        self.hbind('look', 'down', self.move_cursor, 2)
        self.hbind('look', 'right',self.move_cursor, 6)
        self.hbind('look', 'left', self.move_cursor, 4)
        self.hbind('look', 'less',self.move_cursor, 10)
        self.hbind('look', 'greater', self.move_cursor, 11)
        self.bind('look', 'k', self.talkWithPerson)
        self.tile_at_player = self.entities[0, self.entities.yproject(0,0), 0]
        # Player state variables
        self.curr_view = 'play' # if the player is in a menu, etc.
        
        self.talking_list = SelectionList(self, "talking_list", items = ["Ask about someone", "Ask for directions", "Ask the listener to join you", "Say goodbye"], onselect = self.talkedWithPerson)

    def tick_according_to_current_view(game):
        if game.curr_view == 'play':
            game.playv_tick()
        elif game.curr_view == 'look':
            game.lookv_tick()
    def movePlayerAccordingToDirection(game, direction):
        game.direction = direction
        game.tile_at_player = game.entities[game.player.pos]
        if game.direction == 2:
            game.player.z += 1
        if game.direction == 4:
            game.player.x -= 1
            
        if game.direction == 6:
            game.player.x += 1
            
        if game.direction == 8:
            game.player.z -= 1


        if not game.tile_at_player:
            game.player.x, game.player.y, game.player.z = game.last_player_pos
            game.tile_at_player = game.entities[game.last_player_pos] 
            return game.tile_at_player, 'a'


        if game.direction != 5:
            game.player.y += game.tile_at_player.slope
        if game.entities[game.player.x, game.player.y, game.player.z]:
            if game.entities[game.player.x, game.player.y, game.player.z].passable == False:
                game.player.x, game.player.y, game.player.z = game.tile_at_player.x, game.tile_at_player.y, game.tile_at_player.z                    


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

        # Trick to undo game.player Y movement if game.player stepped from a slope in the reverse game.direction
        if game.entities[game.player.x, game.player.y, game.player.z] == None:
            if game.tile_at_player.slope != 0:
                game.player.y -= game.tile_at_player.slope
            return
        game.tick = True
                
        # Trick to undo game.player Y movement if the game.player is walking parallel to the slope
        if game.entities[game.player.x, game.player.y, game.player.z].slope == game.tile_at_player.slope:
            return game.tile_at_player
            if game.direction != 5:
                game.player.y -= game.tile_at_player.slope
        return game.tile_at_player

    def run(game):
        # Variables for the loop
        clock = pygame.time.Clock()


        game.tick = True
        # These two are to avoid having to redraw the screen every game.tick the game.screen is being resized
        videoResizeWasHappening = False
        timeSinceVideoResize = 0

        # Holding F11 behaviour
        screenResizedUsingF11 = False

        # Direction in a keypad 
        # 7 8 9
        # 4 5 6 # 5 means the game.player is standing still
        # 1 2 3
        # 10 is down
        # 11 is up
        game.direction = 5
        game.last_player_pos = game.player.pos
        dt = 0
        tt = 0
        game.tickc = 0

        console_kb = nonblockingchinput.KBHit()

        timeSinceKeyWasLastPressed = {}
        pygame.key.set_repeat(0)

        game.pressed = {}
        ################ MAIN LOOP ####################################
        while True:
            stime = perf_counter()

            if console_kb.kbhit():
                ch = console_kb.getch()
                print(ch, end = '')
                if ch == '\n':
                    if game.currcmd == 'exit':
                        pygame.quit()
                        sys.exit()
                    gargs = game.currcmd.split(' ')
                    if gargs[0] == 'p':
                        print(game.game_to_string())
                    elif game.currcmd == 'mkhuman':
                        game.entities.add(Entity(game, 'U', *game.player.pos, desc = 'A human'))
                    game.currcmd = ''
                elif ord(ch) == 0x7F: # Backspace
                    print('\b \b', end = '')
                    game.currcmd = game.currcmd[:-1]
                else:
                    game.currcmd += ch
                sys.stdout.flush()

            for i in game.listHeldBindings():
                i()

            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.handle_video_resize()
                elif event.type == KEYDOWN:
                    game.handleBindingDown(event)
                elif event.type == KEYUP:
                    game.handleBindingUp(event)
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            timeSinceVideoResize += 1

            if game.direction != 5 and game.MOVE_WHEN_HELD:
                game.tick = True
                if timeSinceKeyWasLastPressed == {}:
                    game.direction = 5

            if timeSinceVideoResize > 10 and videoResizeWasHappening:
                game.tick = True
                videoResizeWasHappening = False
            game.tickc += 1
            if game.tick:
                if game.curr_view == 'play': # Local view
                    game.playv_tick()
                elif game.curr_view == 'look':
                    game.lookv_tick()
                elif game.curr_view == 'map':
                    if game.tick:
                        for i in world:
                            i.print()
                        game.char_notation_blit('@', game.playerworldx, game.playerworldy)
                        pygame.display.update()
            if game.tick:   
                #game.char_notation_blit('FPS - ' + str(dt)[:5],0, 0)
                #game.char_notation_blit('Time taken - ' + str(tt)[:5],0, 1)
                game.blit_announcements()
                pygame.display.update()
            pygame.event.pump()
            etime = perf_counter()
            dt = (1 / (1 / 20 - ((etime - stime)))) 
            tt = (etime - stime)
            game.tick = False
            clock.tick(dt)

    # For pickling and deep-copying
    def __getstate__(self):
        # Pickle everything, except the screen and sheet
        d = self.__dict__
        del d['screen']
        del d['sheet']
        return d

    def __setstate__(self, state):
        pygame.display.init()
        self.__dict__ = state
        self.update_mode()
        self.graphics_init()
        return self.__dict__
if __name__ == '__main__':
    theMainGame = MainGame()
    theMainGame.init()
    theMainGame.run()