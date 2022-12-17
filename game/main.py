from JNetoProductions_pygame_game_engine.camera import Camera
from JNetoProductions_pygame_game_engine.game_loop import GameLoop
from JNetoProductions_pygame_game_engine.rendering_layer import RenderingLayer
from JNetoProductions_pygame_game_engine.scene import Scene
from meteor import Meteor
from map_gmobj import Map
from player_gmobj import Player

game_loop = GameLoop()
map_rendering_layer = RenderingLayer("map_layer")
player_rendering_layer = RenderingLayer("player_layer")
over_player_layer = RenderingLayer("over_player_layer")

main_camera = Camera(map_rendering_layer, player_rendering_layer, over_player_layer)
main_scene = Scene(main_camera)

map = Map(main_scene)
player = Player(main_scene)
meteor = Meteor(main_scene)

# GAME LOOP
game_loop.set_current_scene(main_scene)
game_loop.run_game_loop()

