class VariableDeclarations:
    def init_vars(self):
        self.IS_FULLSCREEN = False
        
        self.TILE_W = 12 # Tile size, in pixels
        self.TILE_H = 12
        self.CHAR_W = 18 # Screen size, in tiles
        self.CHAR_H = 18    

        # Screen size, in pixels
        self.SCREEN_W = self.TILE_W * self.CHAR_W
        self.SCREEN_H = self.TILE_H * self.CHAR_H

        # If the player should move when an arrow key is held
        self.MOVE_WHEN_HELD = True

        # Default map width and height for a local map
        self.mapw = 64
        self.maph = 64

        # Player position in local map
        self.playerx = self.mapw // 2
        self.playery = 0
        self.playerz = self.maph // 2

        # Player position in the world
        self.playerworldx = 2
        self.playerworldy = 2

        # Camera position
        self.camerax = self.CHAR_W // 2
        self.cameraz = self.CHAR_H // 2

        # Size in local maps of the whole world
        # (the world is supposed to be round, not yet implemented)
        self.worldw = 48
        self.worldh = 48

        # this is a 2-dimensional array for the z-index of things:
        # i.e., the player has to be drawn above grass
        self.zindex_buf = [[-100 for _ in range(self.maph)] for _ in range(self.mapw)]
        # I made a way to add foreground and background colors to entitities easily
        # i'll call it "Color notation" here
        # It works as follows:
        #   - A colored tile is represented by a string
        #   - The string has the format [foreground[:background]:]character
        #   - If the character starts with whitespace, then interpret the rest of string as an hexadecimal representation of the character
        #   - Examples:
        #       - R:@ = Red "@"
        #       - B:G:w = Blue "w" with a green background
        #       - Y: 2741 = a yellow Unicode 0x2741: Flower emoji

        self.COLOR_MAP = {
            "0": (0,0,0),
            "R": (255,0,0),
            "G": (0,255,0),
            "Y": (255,255,0),
            "B": (0,0,255),
            "M": (255,0,255),
            "C": (0,255,255),
            "W": (255,255,255)
        }


        self.player = None

        self.bindings = {
            'play': {

            }, 
            '*': {}
        }
        self.dBindings = {
            'play': {

            }, 
            '*': {}
        }

        self.heldBindings = {
            'play': {
            
            }, 
            '*': {}
        }