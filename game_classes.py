from autoclass import autoclass
import copy
@autoclass
class BaseEntity:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, passable = True, draw_index = 0, slope = 0, attrs = None):
        if isinstance(char, BaseEntity):
            e = char
            self.char , self.x , self.y , self.z , self.passable , self.draw_index , self.slope , self.attrs =  e.char , e.x , e.y , e.z , e.passable , e.draw_index , e.slope , e.attrs 
        if attrs == None:  
            self.attrs = set()
    @property
    def pos(self):
        return self.x, self.y, self.z

    def copy(self, alloc):
        return self.__class__(alloc)
# Class for the map, works like a set/dict and iterator
# It's more like a "Specialized Entity array"
class Map:
    def __init__(self, entities = None):
        entities = entities or list()
        self.d = {}

        if isinstance(entities, dict):
            self.d = entities.copy()

        elif hasattr(entities, '__iter__'):
            for e in entities:
                #alloc = BaseEntity()
                self.d[e.x, e.y, e.z] = e# = e.copy(alloc)

    def add(self, *entities):
        for e in entities:
            self.d[e.x, e.y, e.z] = e
    def dirty_copy(self):
        # I hope this works
        self.d['Some key'] = 1
        k = {}.update(self.d)
        print(k)
        return k
    def remove(self, *entities):
        for e in entities:
            del self.d[e.x, e.y, e.z]

    def yproject(self, x, z): # Finds a safe place to place a game.player, house, etc.
        for i in sorted(list(filter(lambda e: e.x == x and e.z == z, self)),key = lambda a: -a.y) :
            return i.y

    def __contains__(self, *items):
        for i in items:
            if isinstance(i, tuple):
                if len(i) == 3:
                    return (i.x, i.y, i.z) in self.d
            else:
                return self.d.get((i.x,i.y,i.z)) == i

    has = __contains__
    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) == 3:
                return self.d.get((item[0], item[1], item[2]))

    def __iter__(self):
        self.i = iter(self.d.values())
        return self.i

    def __next__(self):
        return self.i.__next__()

    def __add__(self, other):
        return Map({**self.d, **other.d})

