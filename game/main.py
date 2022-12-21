# ENGINE IMPORTS
from JNeto_Productions_Engine.game_loop import GameLoop
from JNeto_Productions_Engine.rendering_layer import RenderingLayer
from JNeto_Productions_Engine.camera import Camera
from JNeto_Productions_Engine.scene import Scene

# GAME OBJECTS IMPORTS
from game_object_cockpit import Cockpit
from game_object_map_limits import MapLimits
from game_object_meteor import Meteor
from game_object_map import Map
from game_object_player import Player

# GAME LOOP
game_loop = GameLoop()

# CAMERA AND RENDERING LAYERS
map_rendering_layer = RenderingLayer("map_layer")
player_rendering_layer = RenderingLayer("player_layer")
map_limits_layer = RenderingLayer("map_limits_layer")
over_player_layer = RenderingLayer("over_player_layer")
cockpit_layer = RenderingLayer("cockpit_layer")
main_camera = Camera(map_rendering_layer, player_rendering_layer, over_player_layer, map_limits_layer, cockpit_layer)

# MAIN SCENE
main_scene = Scene(main_camera)

# GAME OBJECTS
map = Map(main_scene)
map_limits = MapLimits(main_scene)
player = Player(main_scene)
cockpit = Cockpit(main_scene, cockpit_layer)
meteor = Meteor(main_scene)

# GAME LOOP
game_loop.set_current_scene(main_scene)
game_loop.run_game_loop()

