
class PlayViewTickFeature:
    def playv_tick(game):
        if game.tile_at_player == None:
            # skip graphics game.tick
           return

        if type(game.tile_at_player) == tuple:
            if game.tile_at_player[1] == 'a':
                # The player has encountered a cliff
                game.tile_at_player = game.tile_at_player[0]
                game.focus_camera(game.player)

        # Move camera
        game.focus_camera(game.player)
        
        game.zindex_buf = [[-100 for _ in range(game.maph)] for _ in range(game.mapw)]
        game.screen.fill((0,0,0)) # TODO only redraw everything if the game.camera has moved

        game.drawMap()
        game.char_notation_blit('@', game.camerax + game.player.x , game.player.z + game.cameraz)
            
        game.last_player_pos = game.tile_at_player.x, game.tile_at_player.y, game.tile_at_player.z
