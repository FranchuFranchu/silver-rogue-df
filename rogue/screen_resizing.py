
class ScreenResizingFeature:
    def addScreen(game, direction):
        if hasattr(game, 'resize_amount'):
            game.resize_amount += 1
        else:
            game.resize_amount = 0

    def resizeScreen(game, direction):
        resize_amount = game.resize_amount
        game.resize_amount = 0
        if direction == 8:
            game.CHAR_H -= resize_amount
        elif direction == 2:
            game.CHAR_H += resize_amount
        elif direction == 4:
            game.CHAR_W -= resize_amount
        elif direction == 6:
            game.CHAR_W += resize_amount
        game.SCREEN_H = game.TILE_W * game.CHAR_H
        game.SCREEN_W = game.TILE_H * game.CHAR_W
        direction = 0
        game.update_mode()
