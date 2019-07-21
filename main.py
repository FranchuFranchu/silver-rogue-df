import random
import math
from time import perf_counter
from itertools import product
from functools import partial

import pygame, sys
from pygame.locals import *
from autoclass import autoclass

import spritesheets
import generate
import nonblockingchinput
# Import classes
from game_classes import BaseEntity, Map
from drawable_game_classes import Entity, World, WorldTile
# Import features
from variable_declarations import VariableDeclarations
from graphics import GraphicsFeature
from bind_utils import BindingFeature
from screen_resizing import ScreenResizingFeature
from copy import deepcopy

class GameObjectFeature:
    def regenerate_world_tile(game, playerx = 4, playerz = 4):
        game.worldtile = game.world[game.playerworldx,game.playerworldy]
        game.entities = game.worldtile.gen()
        game.player.y = game.entities.yproject(game.player.x, game.player.z)
        game.entities.add(game.player)

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
        for i in game.entities:
            
            if game.player.y == i.y:
                i.print() 
        game.char_notation_blit('@', game.camerax + game.player.x , game.player.z + game.cameraz)
            
        game.last_player_pos = game.tile_at_player.x, game.tile_at_player.y, game.tile_at_player.z

class LookingFeature:
    def lookv_tick(game):
        if not hasattr(game, 'cursor_e'):
            game.cursor_e = Entity(game, 'X', game.player.x, game.player.y, game.player.z)

        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
        game.screen.fill((0,0,0))
        for i in game.entities:
            
            if game.cursor_e.y == i.y:
                i.print() 

        game.cursor_e.print()
        
    def move_cursor(game, direction):
        game.direction = direction
        game.tick = True
        game.focus_camera(game.cursor_e)

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
        for i in game.entities:
            if game.player.y == i.y:
                i.print() 

class ViewSwitchFunctionsFeature:
    # Functions to switch between Views using lambdas
    def setView(game, view):
        game.curr_view = view
        print('!', game.curr_view)

class MainGame(
    VariableDeclarations,
    GraphicsFeature,
    BindingFeature,
    GameObjectFeature,
    ScreenResizingFeature,
    ViewSwitchFunctionsFeature,
    PlayViewTickFeature,
    LookingFeature
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
        self.hbind('look', 'up',   self.move_cursor, 8)
        self.hbind('look', 'down', self.move_cursor, 2)
        self.hbind('look', 'right',self.move_cursor, 6)
        self.hbind('look', 'left', self.move_cursor, 4)
        self.hbind('look', 'less',self.move_cursor, 10)
        self.hbind('look', 'greater', self.move_cursor, 11)
        self.tile_at_player = self.entities[0, self.entities.yproject(0,0), 0]

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

        # Player state variables
        game.curr_view = 'play' # if the player is in a menu, etc.

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

        game.curr_view = 'play'
        game.pressed = {}
        ################ MAIN LOOP ####################################
        while True:
            stime = perf_counter()

            if console_kb.kbhit():
                ch = console_kb.getch()
                print(ch, end = '')
                sys.stdout.flush()
                if ch == '\n':
                    if game.currcmd == 'exit':
                        pygame.quit()
                        sys.exit()
                    game.currcmd = ''
                else:
                    game.currcmd += ch

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
            etime = perf_counter()
            if game.tick:

                game.char_notation_blit('FPS - ' + str(dt)[:5],0, 0)
                game.char_notation_blit('Time taken - ' + str(tt)[:5],0, 1)
                pygame.display.update()
            dt = (-1 / (((etime - stime))))
            tt = (etime - stime)
            game.tick = False
            if dt < 30:
                dt = 30
            pygame.event.pump()
            clock.tick(30)


if __name__ == '__main__':
    theMainGame = MainGame()
    theMainGame.init()
    theMainGame.run()