from autoclass import autoclass
import copy
@autoclass
class BaseMapTile:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, passable = True, draw_index = 0, slope = 0, attrs = None, entities = None):
        if isinstance(char, BaseMapTile):
            e = char
            self.char , self.x , self.y , self.z , self.passable , self.mapTilesraw_index , self.slope , self.attrs =  e.char , e.x , e.y , e.z , e.passable , e.draw_index , e.slope , e.attrs 
        if attrs == None:  
            self.attrs = set()
        if entities == None:  
            self.entities = list()
    @property
    def pos(self):
        return self.x, self.y, self.z

    @property
    def xz(self):
        return self.x, self.z

    def copy(self, alloc):
        return self.__class__(alloc)
# Class for the map, works like a set/dict and iterator

class Map:
    def __init__(self, entities = None):
        entities = entities or list()
        self.mapTiles = {}

        if isinstance(entities, dict):
            self.mapTiles = entities.copy()

        elif hasattr(entities, '__iter__'):
            for e in entities:
                #alloc = BaseMapTile()
                self.mapTiles[e.x, e.y, e.z] = e# = e.copy(alloc)
    @property
    def d(self): # For backwards compatibility
        return self.mapTiles
    
    def add(self, *entities):
        for e in entities:
            if isinstance(e, BaseEntity):
                self.mapTiles[e.x, e.y, e.z].entities.append(e)
            elif isinstance(e, BaseMapTile):
                self.mapTiles[e.x, e.y, e.z] = e

    def remove(self, *entities):
        for e in entities:
            del self.mapTiles[e.x, e.y, e.z]

    def yproject(self, x, z): # Finds a safe place to place a game.player, house, etc.
        for i in sorted(list(filter(lambda e: e.x == x and e.z == z, self)),key = lambda a: -a.y) :
            return i.y
    def __contains__(self, *items):
        for i in items:
            if isinstance(i, tuple):
                if len(i) == 3:
                    return (i.x, i.y, i.z) in self.mapTiles
            else:
                return self.mapTiles.get((i.x,i.y,i.z)) == i

    has = __contains__
    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) == 3:
                return self.mapTiles.get((item[0], item[1], item[2]))

    def __iter__(self):
        self.i = iter(self.mapTiles.values())
        return self.i

    def __next__(self):
        return self.i.__next__()

    def __add__(self, other):
        new_self_map_tiles = self.mapTiles.copy()
        f = {**new_self_map_tiles, **other.mapTiles}
        return Map(f)

class HistoricalEntity:
    # Saves entities when they aren't loaded
    name = ''

class Site:
    pass

class Item:
    def __init__(self, game, item_name):
        self.game = game
        self.name = item_name

    @property
    def volume(self):
        return self._volume

    @property
    def translate(self):
        return self.game._(self.item_name)
    
    

class Inventory:
    def __init__(self, max_volume):
        self.max_volume = max_volume
        self.items = []

    @property
    def used_volume(self):
        v = 0
        for i in self.items:
            v += i.volume

        return v
    
    def add(self, item: Item):
        if item.volume + self.used_volume > max_volume:
            return False

        self.items.append(item)
        return True

    def remove(self, item: Item):
        self.items.remove(item)

@autoclass
class BaseEntity:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, volume = 75, draw_index = 0, attrs = None, desc = ''):
        self.char , self.x , self.y , self.z , self.draw_index , self.volume, self.desc, self.attrs =  char , x , y , z , draw_index , volume, desc, attrs 
    @property
    def pos(self):
        return self.x, self.y, self.z
    
