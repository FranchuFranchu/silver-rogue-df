# Minified list of key names 
KEY_NAMES = {0: 'FIRST', 'UNKNOWN': 0, 'FIRST': 0, 8: 'BACKSPACE', 'BACKSPACE': 8, 9: 'TAB', 'TAB': 9, 12: 'CLEAR', 'CLEAR': 12, 13: 'RETURN', 'RETURN': 13, 19: 'PAUSE', 'PAUSE': 19, 27: 'ESCAPE', 'ESCAPE': 27, 32: 'SPACE', 'SPACE': 32, 33: 'EXCLAIM', 'EXCLAIM': 33, 34: 'QUOTEDBL', 'QUOTEDBL': 34, 35: 'HASH', 'HASH': 35, 36: 'DOLLAR', 'DOLLAR': 36, 38: 'AMPERSAND', 'AMPERSAND': 38, 39: 'QUOTE', 'QUOTE': 39, 40: 'LEFTPAREN', 'LEFTPAREN': 40, 41: 'RIGHTPAREN', 'RIGHTPAREN': 41, 42: 'ASTERISK', 'ASTERISK': 42, 43: 'PLUS', 'PLUS': 43, 44: 'COMMA', 'COMMA': 44, 45: 'MINUS', 'MINUS': 45, 46: 'PERIOD', 'PERIOD': 46, 47: 'SLASH', 'SLASH': 47, 48: '0', '0': 48, 49: '1', '1': 49, 50: '2', '2': 50, 51: '3', '3': 51, 52: '4', '4': 52, 53: '5', '5': 53, 54: '6', '6': 54, 55: '7', '7': 55, 56: '8', '8': 56, 57: '9', '9': 57, 58: 'COLON', 'COLON': 58, 59: 'SEMICOLON', 'SEMICOLON': 59, 60: 'LESS', 'LESS': 60, 61: 'EQUALS', 'EQUALS': 61, 62: 'GREATER', 'GREATER': 62, 63: 'QUESTION', 'QUESTION': 63, 64: 'AT', 'AT': 64, 91: 'LEFTBRACKET', 'LEFTBRACKET': 91, 92: 'BACKSLASH', 'BACKSLASH': 92, 93: 'RIGHTBRACKET', 'RIGHTBRACKET': 93, 94: 'CARET', 'CARET': 94, 95: 'UNDERSCORE', 'UNDERSCORE': 95, 96: 'BACKQUOTE', 'BACKQUOTE': 96, 97: 'a', 'a': 97, 98: 'b', 'b': 98, 99: 'c', 'c': 99, 100: 'd', 'd': 100, 101: 'e', 'e': 101, 102: 'f', 'f': 102, 103: 'g', 'g': 103, 104: 'h', 'h': 104, 105: 'i', 'i': 105, 106: 'j', 'j': 106, 107: 'k', 'k': 107, 108: 'l', 'l': 108, 109: 'm', 'm': 109, 110: 'n', 'n': 110, 111: 'o', 'o': 111, 112: 'p', 'p': 112, 113: 'q', 'q': 113, 114: 'r', 'r': 114, 115: 's', 's': 115, 116: 't', 't': 116, 117: 'u', 'u': 117, 118: 'v', 'v': 118, 119: 'w', 'w': 119, 120: 'x', 'x': 120, 121: 'y', 'y': 121, 122: 'z', 'z': 122, 127: 'DELETE', 'DELETE': 127, 256: 'KP0', 'KP0': 256, 257: 'KP1', 'KP1': 257, 258: 'KP2', 'KP2': 258, 259: 'KP3', 'KP3': 259, 260: 'KP4', 'KP4': 260, 261: 'KP5', 'KP5': 261, 262: 'KP6', 'KP6': 262, 263: 'KP7', 'KP7': 263, 264: 'KP8', 'KP8': 264, 265: 'KP9', 'KP9': 265, 266: 'KP_PERIOD', 'KP_PERIOD': 266, 267: 'KP_DIVIDE', 'KP_DIVIDE': 267, 268: 'KP_MULTIPLY', 'KP_MULTIPLY': 268, 269: 'KP_MINUS', 'KP_MINUS': 269, 270: 'KP_PLUS', 'KP_PLUS': 270, 271: 'KP_ENTER', 'KP_ENTER': 271, 272: 'KP_EQUALS', 'KP_EQUALS': 272, 273: 'UP', 'UP': 273, 274: 'DOWN', 'DOWN': 274, 275: 'RIGHT', 'RIGHT': 275, 276: 'LEFT', 'LEFT': 276, 277: 'INSERT', 'INSERT': 277, 278: 'HOME', 'HOME': 278, 279: 'END', 'END': 279, 280: 'PAGEUP', 'PAGEUP': 280, 281: 'PAGEDOWN', 'PAGEDOWN': 281, 282: 'F1', 'F1': 282, 283: 'F2', 'F2': 283, 284: 'F3', 'F3': 284, 285: 'F4', 'F4': 285, 286: 'F5', 'F5': 286, 287: 'F6', 'F6': 287, 288: 'F7', 'F7': 288, 289: 'F8', 'F8': 289, 290: 'F9', 'F9': 290, 291: 'F10', 'F10': 291, 292: 'F11', 'F11': 292, 293: 'F12', 'F12': 293, 294: 'F13', 'F13': 294, 295: 'F14', 'F14': 295, 296: 'F15', 'F15': 296, 300: 'NUMLOCK', 'NUMLOCK': 300, 301: 'CAPSLOCK', 'CAPSLOCK': 301, 302: 'SCROLLOCK', 'SCROLLOCK': 302, 303: 'RSHIFT', 'RSHIFT': 303, 304: 'LSHIFT', 'LSHIFT': 304, 305: 'RCTRL', 'RCTRL': 305, 306: 'LCTRL', 'LCTRL': 306, 307: 'RALT', 'RALT': 307, 308: 'LALT', 'LALT': 308, 309: 'RMETA', 'RMETA': 309, 310: 'LMETA', 'LMETA': 310, 311: 'LSUPER', 'LSUPER': 311, 312: 'RSUPER', 'RSUPER': 312, 313: 'MODE', 'MODE': 313, 315: 'HELP', 'HELP': 315, 316: 'PRINT', 'PRINT': 316, 317: 'SYSREQ', 'SYSREQ': 317, 318: 'BREAK', 'BREAK': 318, 319: 'MENU', 'MENU': 319, 320: 'POWER', 'POWER': 320, 321: 'EURO', 'EURO': 321, 323: 'LAST', 'LAST': 323}


class BindingFeature:

    def bind(game, view, combination, function, *args, **kwargs):
        if game.bindings.get(view):
            game.bindings[view][combination.upper()] = lambda: function(*args, **kwargs)
        else:
            game.bindings[view] = {}
            game.bindings[view][combination.upper()] = lambda: function(*args, **kwargs)

    def hbind(game, view, combination, function, *args, **kwargs):
        if game.heldBindings.get(view):
            game.heldBindings[view][combination.upper()] = lambda: function(*args, **kwargs)
        else:
            game.heldBindings[view] = {}
            game.heldBindings[view][combination.upper()] = lambda: function(*args, **kwargs)

    def dbind(game, view, combination, function, *args, **kwargs):
        if game.dBindings.get(view):
            game.dBindings[view][combination.upper()] = lambda: function(*args, **kwargs)
        else:
            game.dBindings[view] = {}
            game.dBindings[view][combination.upper()] = lambda: function(*args, **kwargs)

    def handleBindingUp(game, event):
        try:
            name = KEY_NAMES[event.key]
        except KeyError:
            name = str(event.key).upper()
        viewBindings = {**game.bindings.get(game.curr_view, {}), **game.bindings['*']}
        name = name.upper()
        for i in filter(lambda i: name in i.split('-'),viewBindings.keys()):
            i = i.upper()
            comb = i
            comb_keys = i.split('-')
            all_keys_pressed = True
            for i in filter(lambda i: i in comb_keys, KEY_NAMES.keys()):
                if not game.pressed.get(KEY_NAMES[i]):
                    all_keys_pressed = False
                    break
            if all_keys_pressed:
                viewBindings[comb]()   
        if game.pressed.get(event.key):
            del game.pressed[event.key]

    def handleBindingDown(game, event):
        game.pressed[event.key] = True
        try:
            name = KEY_NAMES[event.key]
            
        except KeyError:
            name = str(event.key)
        game.timeSinceHeldBindingWasPressed[name.upper()] = 0
        viewBindings = {**game.dBindings.get(game.curr_view, {}), **game.dBindings['*']}
        for i in filter(lambda i: name in i.split('-'),viewBindings.keys()):
            i = i.upper()
            comb = i
            comb_keys = i.split('-')
            all_keys_pressed = True
            for i in filter(lambda i: i in comb_keys, KEY_NAMES.keys()):
                if not game.pressed.get(KEY_NAMES[i]):
                    all_keys_pressed = False
                    break
            if all_keys_pressed:
                viewBindings[comb]()    

    def listHeldBindings(game): # Return a list of functions that need to be run now
        functions = []

        viewBindings = {**game.heldBindings.get(game.curr_view, {}), **game.heldBindings['*']}
        for key in game.pressed.keys():
            if type(key) == int:
                try:
                    key = KEY_NAMES[key]
                except KeyError:
                    key = str(key)
            for i in filter(lambda i: key in i.split('-'),viewBindings.keys()):
                i = i.upper()
                comb = i
                comb_keys = i.split('-')
                all_keys_pressed = True
                for i in filter(lambda i: (i.upper() if type(i) == str else i) in comb_keys, KEY_NAMES.keys()):
                    if not game.pressed.get(KEY_NAMES[i]):
                        all_keys_pressed = False
                        break
                if all_keys_pressed:
                    game.timeSinceHeldBindingWasPressed[comb.upper()] += 1
                    
                    if game.timeSinceHeldBindingWasPressed[comb.upper()] == 1:


                        functions.append(viewBindings[comb.upper()])
                    elif game.timeSinceHeldBindingWasPressed[comb.upper()] > game.TAP_HOLD_THRESHOLD:
                        functions.append(viewBindings[comb.upper()])

                else:
                    game.timeSinceHeldBindingWasPressed[comb.upper()] = 0
        return functions
