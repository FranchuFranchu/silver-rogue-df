# Module containing selection lists and similar stuff

class Widget:
    def __init__(self, game):
        # Set bindings and draw it
        self.game = game

class SelectionList(Widget):
    def __init__(self, game, name, x = 0, y = 0, w = 0, h = 0, items = [], onselect = lambda i: i, color_scheme = 'W'):
        super().__init__(game)
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_scheme = color_scheme
        self.onselect = onselect
        self.items = items
        self.currselected = 0
        self.pre_screen = game.screen.copy() # Lower layer of the screen
        game.bind('W_%s' % name, 'PLUS', self.moveSelectionFoward)
        game.bind('W_%s' % name, 'MINUS', self.moveSelectionBackward)
        game.bind('W_%s' % name, 'RETURN', self.enterKey)
        print(game.bindings)

    def display(self):
        self.b_view = self.game.curr_view
        self.game.curr_view = 'W_%s' % self.name

        self.update()


    def update(self):
        self.pre_screen.blit(self.game.screen, (0, 0))

        for y, i in enumerate(self.items):
            col = 'W:' + i if y == self.currselected else '8:' + i # Highligth the item if it's selected
            self.game.char_notation_blit(col, self.x, self.y + y)
        self.game.g_update()
    def moveSelectionFoward(self):
        self.currselected += 1
        self.update()

    def moveSelectionBackward(self):
        self.currselected -= 1
        self.update()
    
    def enterKey(self):
        self.game.setView(self.b_view)
        self.onselect(self.currselected)

    # For pickling and deep-copying
    def __getstate__(self):
        d = self.__dict__
        del d['pre_screen']
        return d

class WidgetFeature:
    pass