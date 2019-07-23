from pygame.locals import *

# Minified list of key names 
KEY_NAMES = {K_UNKNOWN: "UNKNOWN", "UNKNOWN": K_UNKNOWN, K_FIRST: "FIRST", "FIRST": K_FIRST, K_BACKSPACE: "BACKSPACE", "BACKSPACE": K_BACKSPACE, K_TAB: "TAB", "TAB": K_TAB, K_CLEAR: "CLEAR", "CLEAR": K_CLEAR, K_RETURN: "RETURN", "RETURN": K_RETURN, K_PAUSE: "PAUSE", "PAUSE": K_PAUSE, K_ESCAPE: "ESCAPE", "ESCAPE": K_ESCAPE, K_SPACE: "SPACE", "SPACE": K_SPACE, K_EXCLAIM: "EXCLAIM", "EXCLAIM": K_EXCLAIM, K_QUOTEDBL: "QUOTEDBL", "QUOTEDBL": K_QUOTEDBL, K_HASH: "HASH", "HASH": K_HASH, K_DOLLAR: "DOLLAR", "DOLLAR": K_DOLLAR, K_AMPERSAND: "AMPERSAND", "AMPERSAND": K_AMPERSAND, K_QUOTE: "QUOTE", "QUOTE": K_QUOTE, K_LEFTPAREN: "LEFTPAREN", "LEFTPAREN": K_LEFTPAREN, K_RIGHTPAREN: "RIGHTPAREN", "RIGHTPAREN": K_RIGHTPAREN, K_ASTERISK: "ASTERISK", "ASTERISK": K_ASTERISK, K_PLUS: "PLUS", "PLUS": K_PLUS, K_COMMA: "COMMA", "COMMA": K_COMMA, K_MINUS: "MINUS", "MINUS": K_MINUS, K_PERIOD: "PERIOD", "PERIOD": K_PERIOD, K_SLASH: "SLASH", "SLASH": K_SLASH, K_0: "0", "0": K_0, K_1: "1", "1": K_1, K_2: "2", "2": K_2, K_3: "3", "3": K_3, K_4: "4", "4": K_4, K_5: "5", "5": K_5, K_6: "6", "6": K_6, K_7: "7", "7": K_7, K_8: "8", "8": K_8, K_9: "9", "9": K_9, K_COLON: "COLON", "COLON": K_COLON, K_SEMICOLON: "SEMICOLON", "SEMICOLON": K_SEMICOLON, K_LESS: "LESS", "LESS": K_LESS, K_EQUALS: "EQUALS", "EQUALS": K_EQUALS, K_GREATER: "GREATER", "GREATER": K_GREATER, K_QUESTION: "QUESTION", "QUESTION": K_QUESTION, K_AT: "AT", "AT": K_AT, K_LEFTBRACKET: "LEFTBRACKET", "LEFTBRACKET": K_LEFTBRACKET, K_BACKSLASH: "BACKSLASH", "BACKSLASH": K_BACKSLASH, K_RIGHTBRACKET: "RIGHTBRACKET", "RIGHTBRACKET": K_RIGHTBRACKET, K_CARET: "CARET", "CARET": K_CARET, K_UNDERSCORE: "UNDERSCORE", "UNDERSCORE": K_UNDERSCORE, K_BACKQUOTE: "BACKQUOTE", "BACKQUOTE": K_BACKQUOTE, K_a: "a", "a": K_a, K_b: "b", "b": K_b, K_c: "c", "c": K_c, K_d: "d", "d": K_d, K_e: "e", "e": K_e, K_f: "f", "f": K_f, K_g: "g", "g": K_g, K_h: "h", "h": K_h, K_i: "i", "i": K_i, K_j: "j", "j": K_j, K_k: "k", "k": K_k, K_l: "l", "l": K_l, K_m: "m", "m": K_m, K_n: "n", "n": K_n, K_o: "o", "o": K_o, K_p: "p", "p": K_p, K_q: "q", "q": K_q, K_r: "r", "r": K_r, K_s: "s", "s": K_s, K_t: "t", "t": K_t, K_u: "u", "u": K_u, K_v: "v", "v": K_v, K_w: "w", "w": K_w, K_x: "x", "x": K_x, K_y: "y", "y": K_y, K_z: "z", "z": K_z, K_DELETE: "DELETE", "DELETE": K_DELETE, K_KP0: "KP0", "KP0": K_KP0, K_KP1: "KP1", "KP1": K_KP1, K_KP2: "KP2", "KP2": K_KP2, K_KP3: "KP3", "KP3": K_KP3, K_KP4: "KP4", "KP4": K_KP4, K_KP5: "KP5", "KP5": K_KP5, K_KP6: "KP6", "KP6": K_KP6, K_KP7: "KP7", "KP7": K_KP7, K_KP8: "KP8", "KP8": K_KP8, K_KP9: "KP9", "KP9": K_KP9, K_KP_PERIOD: "KP_PERIOD", "KP_PERIOD": K_KP_PERIOD, K_KP_DIVIDE: "KP_DIVIDE", "KP_DIVIDE": K_KP_DIVIDE, K_KP_MULTIPLY: "KP_MULTIPLY", "KP_MULTIPLY": K_KP_MULTIPLY, K_KP_MINUS: "KP_MINUS", "KP_MINUS": K_KP_MINUS, K_KP_PLUS: "KP_PLUS", "KP_PLUS": K_KP_PLUS, K_KP_ENTER: "KP_ENTER", "KP_ENTER": K_KP_ENTER, K_KP_EQUALS: "KP_EQUALS", "KP_EQUALS": K_KP_EQUALS, K_UP: "UP", "UP": K_UP, K_DOWN: "DOWN", "DOWN": K_DOWN, K_RIGHT: "RIGHT", "RIGHT": K_RIGHT, K_LEFT: "LEFT", "LEFT": K_LEFT, K_INSERT: "INSERT", "INSERT": K_INSERT, K_HOME: "HOME", "HOME": K_HOME, K_END: "END", "END": K_END, K_PAGEUP: "PAGEUP", "PAGEUP": K_PAGEUP, K_PAGEDOWN: "PAGEDOWN", "PAGEDOWN": K_PAGEDOWN, K_F1: "F1", "F1": K_F1, K_F2: "F2", "F2": K_F2, K_F3: "F3", "F3": K_F3, K_F4: "F4", "F4": K_F4, K_F5: "F5", "F5": K_F5, K_F6: "F6", "F6": K_F6, K_F7: "F7", "F7": K_F7, K_F8: "F8", "F8": K_F8, K_F9: "F9", "F9": K_F9, K_F10: "F10", "F10": K_F10, K_F11: "F11", "F11": K_F11, K_F12: "F12", "F12": K_F12, K_F13: "F13", "F13": K_F13, K_F14: "F14", "F14": K_F14, K_F15: "F15", "F15": K_F15, K_NUMLOCK: "NUMLOCK", "NUMLOCK": K_NUMLOCK, K_CAPSLOCK: "CAPSLOCK", "CAPSLOCK": K_CAPSLOCK, K_SCROLLOCK: "SCROLLOCK", "SCROLLOCK": K_SCROLLOCK, K_RSHIFT: "RSHIFT", "RSHIFT": K_RSHIFT, K_LSHIFT: "LSHIFT", "LSHIFT": K_LSHIFT, K_RCTRL: "RCTRL", "RCTRL": K_RCTRL, K_LCTRL: "LCTRL", "LCTRL": K_LCTRL, K_RALT: "RALT", "RALT": K_RALT, K_LALT: "LALT", "LALT": K_LALT, K_RMETA: "RMETA", "RMETA": K_RMETA, K_LMETA: "LMETA", "LMETA": K_LMETA, K_LSUPER: "LSUPER", "LSUPER": K_LSUPER, K_RSUPER: "RSUPER", "RSUPER": K_RSUPER, K_MODE: "MODE", "MODE": K_MODE, K_HELP: "HELP", "HELP": K_HELP, K_PRINT: "PRINT", "PRINT": K_PRINT, K_SYSREQ: "SYSREQ", "SYSREQ": K_SYSREQ, K_BREAK: "BREAK", "BREAK": K_BREAK, K_MENU: "MENU", "MENU": K_MENU, K_POWER: "POWER", "POWER": K_POWER, K_EURO: "EURO", "EURO": K_EURO, K_LAST: "LAST", "LAST": K_LAST}

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
