# ENGINE IMPORTS
from engine_JNeto_Productions.game_loop import GameLoop
from engine_JNeto_Productions.rendering_layer import RenderingLayer
from engine_JNeto_Productions.camera import Camera
from engine_JNeto_Productions.scene import Scene

# GAME OBJECTS IMPORTS
from game_objects.game_object_cockpit import Cockpit
from game_objects.game_object_map_limits import MapLimits
from game_objects.game_object_map import Map
from game_objects.game_object_meteor_manager import MeteorManager
from game_objects.game_object_player import Player
from game_objects.game_object_score import Score

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
meteor_manager = MeteorManager(main_scene, map_rendering_layer)
score = Score(main_scene)

# GAME LOOP
game_loop.set_current_scene(main_scene)
game_loop.run_game_loop()

