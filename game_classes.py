from autoclass import autoclass

@autoclass
class BaseEntity:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, passable = True, draw_index = 0, slope = 0, attrs = None):
        if attrs == None:
            self.attrs = set()
    @property
    def pos(self):
        return self.x, self.y, self.z
        

# Class for the map, works like a set/dict and iterator
# It's more like a "Specialized Entity array"
class Map:
    def __init__(self, entity_list = []):
        self.d = {}
        if type(entity_list) == dict:
            self.d = entity_list
        elif hasattr(entity_list, '__iter__'):
            for i in entity_list:
                self.d[i.x,i.y,i.z] = i
    def add(self, *items):
        for i in items:
            if self.d.get((i.x,i.y,i.z)):
                del self.d[i.x,i.y,i.z]
            self.d[i.x,i.y,i.z] = i

    def yproject(self, x, z): # Finds a safe place to place a game.player, house, etc.
        for i in sorted(list(filter(lambda e: e.x == x and e.z == z, self)),key = lambda a: -a.y) :
            return i.y

    def __contains__(self,*items):
        for i in items:
            if type(i) == tuple:
                if len(i) == 3:
                    return self.d.has_key(i.x,i.y,i.z)
            else:
                return self.d[i.x,i.y,i.z] == i
    has = __contains__
    def __getitem__(self,item):
        if type(item) == tuple:
            if len(item) == 3:
                return self.d.get((item[0],item[1],item[2]))

    def remove(self,*items):
        for i in items:
            del self.d[i.x,i.y,i.z]

    def __iter__(self):
        self.i = iter(self.d.values())
        return self.i
    def __next__(self):
        return self.i.__next__()

    def __add__(self, other):
        return Map({**self.d, **other.d})