from game_classes import BaseMapTile, Map, BaseEntity
from autoclass import autoclass
import random
import generate
from itertools import product
import math
import numpy as np
import copy

# Makes a grass entity
def Grass(game, x,y,z):
    ch = random.choice([',','\'','"'])
    ch = 'G:0:' + ch
    e = MapTile(game, ch, x, y, z, True, -10)
    e.attrs.add('terrain')
    return e


def convert_to_graphics_classes(game, self: Map):
    # Converts all BaseMapTiles -> MapTiles
    # And BaseEntities -> Entities

    for k, m in self.mapTiles.items():
        if not isinstance(m, BaseMapTile):
            # Something horrible happened
            del self.mapTiles[k]
            continue
        for idx, j in enumerate(m.entities):
            if type(j) == BaseEntity:
                m.entities[idx] = Entity(game, j)
        if type(m) == BaseMapTile:
            m = MapTile(game, m)
        self.mapTiles[k] = m
    pass
class MapTile(BaseMapTile):
    def __init__(self, game, *args, **kwargs):
        self.game = game
        if len(args) == 1 and kwargs == {}:
            if type(args[0]) == BaseMapTile:
                e = args[0]
                self.char , self.x , self.y , self.z , self.passable , self.draw_index , self.slope , self.attrs, self.entities =  e.char , e.x , e.y , e.z , e.passable , e.draw_index , e.slope , e.attrs, e.entities
                return
                
        BaseMapTile.__init__(self, *args, **kwargs)

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

class Entity(BaseEntity):
    def __init__(self, game, *args, **kwargs):    
        self.game = game
        if len(args) == 1 and kwargs == {}:
            if type(args[0]) == BaseEntity:
                e = args[0]
                self.char , self.x , self.y , self.z , self.draw_index , self.volume, self.desc, self.attrs, =  e.char , e.x , e.y , e.z , e.draw_index , e.volume, e.desc, e.attrs 
                return
        BaseEntity.__init__(self, *args, **kwargs)
    def print(self):
        if self.game.CHAR_H <= self.z + self.game.cameraz:
            return
        elif self.game.CHAR_W <= self.x + self.game.camerax:
            return
        if self.draw_index + 100 < self.game.zindex_buf[self.x][self.z]: # + 100 because entities will always be drawn after map tiles
            return
        self.game.zindex_buf[self.x][self.z] = self.draw_index + 100
        self.game.char_notation_blit(self.char, self.x + self.game.camerax, self.z + self.game.cameraz)

@autoclass
class WorldTile:

    def __init__(self, game, char = ' ', x = 0, z = 0, worldseed = random.random() * 10 ** 6, passable = False, draw_index = 1, flatness = 0.4, site = None):
        self.game = game

    def gen(self):
        # Generate the local map
        map_gened = generate.terrain.main(
            self.worldseed, 
            self.game.mapw, 
            self.game.maph, 
            self.x, 
            self.z)
        self.game.zindex_buf = [[-100 for _ in range(self.game.maph)] for _ in range(self.game.mapw)]

        # Convert map_gened to a Map class
        new_entities = []
        for i in range(self.game.mapw):
            for j in range(self.game.maph):
                new_entities.append(Grass(self.game, i, int(map_gened[i][j] * 5 + 80),j)) 
        
        new_entities = Map(new_entities)

        # Add the town contents
        if self.site:
            t_gened = self.site.gen(new_entities)
            convert_to_graphics_classes(self.game, t_gened) 
            new_entities += t_gened

        # Generate slopes in the terrain "cliffs"
        for i in filter(lambda x: {'terrain', 'road'} & x.attrs, new_entities.d.values()):
            # Search for adjacent tiles in the higher layer
            for e in (new_entities[i.x + 1, i.y + 1, i.z], 
                      new_entities[i.x + 1, i.y + 1, i.z + 1],
                      new_entities[i.x - 1, i.y + 1, i.z],
                      new_entities[i.x, i.y + 1, i.z - 1]):
                if e != None: # there is nothing on the tile
                    if {'terrain', 'road'} & e.attrs: # make sure the tile is not the new_player or smth


                        new_entities[i.x, i.y, i.z].char = "G: 1F" # Up arrow
                        new_entities[i.x, i.y, i.z].slope = 1

                        if new_entities[e.x, i.y + 1, e.z]:
                            if {'terrain', 'road'} & new_entities[e.x, i.y + 1, e.z].attrs:
                                continue
                            new_entities[e.x, i.y + 1, e.z].slope = -1
                            new_entities[e.x, i.y + 1, e.z].char = "G: 1E"
            # do the same but for lower layers
            for e in (new_entities[i.x + 1, i.y - 1, i.z],new_entities[i.x + 1, i.y - 1, i.z + 1],new_entities[i.x - 1, i.y - 1, i.z],new_entities[i.x, i.y - 1, i.z - 1]):
                if e != None: 
                    if {'terrain', 'road'} & e.attrs:

                        new_entities[i.x, i.y, i.z].char = "G: 1E" # Up arrow
                        new_entities[i.x, i.y, i.z].slope = -1
                        if new_entities[e.x, i.y - 1, e.z]:
                            if {'terrain', 'road'} & new_entities[e.x, i.y - 1, e.z].attrs:
                                continue
                            new_entities[e.x, i.y - 1, e.z].slope = 1
                            new_entities[e.x, i.y - 1, e.z].char = "G: 1F"
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


class World():
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
