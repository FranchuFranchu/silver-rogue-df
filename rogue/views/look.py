import random

import yaml

from graphics import SelectionList
from drawable_game_classes import MapTile

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
        

    def talkedWithPerson(game, what, metadata):
        if metadata.get('messages_self'):

            game.announcements.append("You: " + 
                game._(random.choice(metadata.get('messages_self'))).
                format(
                    listener = game.entities[game.cursor_e.pos].entities[0].desc,
                    speaker = game.player.desc
                ))
        if metadata.get('messages_other'):

            game.announcements.append(game.entities[game.cursor_e.pos].entities[0].desc + ": " + 
                game._(random.choice(metadata.get('messages_other'))).
                format(
                    speaker = game.entities[game.cursor_e.pos].entities[0].desc,
                    listener = game.player.desc
                ))
        if metadata.get('self'):
            # Move to another menu
            game.talking_menu = metadata['self']
            game.curr_view = 'play'
            if game.talking_menu != 'exit':
                game.talking_list[game.talking_menu].display()
                return


        #game.announcements.append(game.entities[game.cursor_e.pos].entities[0].desc + ': Hi')
        game.setView('play')
        game.drawMap()

    def talkWithPerson(game):
        game.talking_menu = 'greet'
        e = game.entities[game.cursor_e.pos]
        game.drawMap()
        if len(e.entities) == 0:
            game.announcements.append("There is no one to talk with here")
        else:
            game.talking_list[game.talking_menu].display()

    def load_talking_behaviour(game):
        with open('../data/conversation/behaviour.yml') as f:
            game.talking_behaviour = yaml.load(f)
        game.talking_list = {}
        for k, v in game.talking_behaviour.items():
            sl_items = []
            sl_metadata = []
            for l, w in v.items():
                sl_items.append(w["option"])
                sl_metadata.append(w)
            game.talking_list[k] = SelectionList(game, "talking_list_" + k, items = 
                game.multiple_translations(
                    *sl_items
                    ),
                    metadata = sl_metadata,
                    onselect = game.talkedWithPerson)