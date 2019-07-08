 
@autoclass
class Entity:
    def __init__(self, char = ' ', x = 0, y = 0, z = 0, passable = False, draw_index = 0, slope = 0, attrs = set()):
        pass
    def print(self):
        #log(self.x,self.y,self.z)
        global zindex_buf
        if CHAR_H <= self.z + cameraz:
            return
        elif CHAR_W <= self.x + camerax:
            return
        if self.draw_index < zindex_buf[self.x][self.z]:
            return
        zindex_buf[self.x][self.z] = self.draw_index
        drawing.char_notation_blit(self.char, self.x + camerax, self.z + cameraz)
 
 
# Makes a grass entity
def Grass(x,y,z):
    ch = random.choice([',','\'','"'])
    ch = 'G:0:' + ch
    e = Entity(ch, x, y, z, True, -1)
    e.attrs.add('terrain')
    return e

