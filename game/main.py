import sys
import pygame

# ENGINE IMPORTS
from engine_JNeto_Productions.game_loop import GameLoop
from engine_JNeto_Productions.rendering_layer import RenderingLayer
from engine_JNeto_Productions.camera import Camera
from engine_JNeto_Productions.scene import Scene
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen

# GAME OBJECTS IMPORTS
from game_objects_main_scene.game_object_cockpit import Cockpit
from game_objects_main_scene.game_object_map_limits import MapLimits
from game_objects_main_scene.game_object_map import Map
from game_objects_main_scene.game_object_meteor_manager import MeteorManager
from game_objects_main_scene.game_object_player import Player
from game_objects_main_scene.game_object_score import Score
from game_objects_main_scene.main_scene_reseter_game_object import MainSceneReseter
from game_objects_menu_scene.banner_game_object import MenuBanner
from game_objects_menu_scene.menu_background_game_object import MenuBackground
from button_game_object import Button

# GAME LOOP
game_loop = GameLoop()

# MENU SCENE
menu_layer1 = RenderingLayer("menu_layer1")
menu_layer2 = RenderingLayer("menu_layer2")
camera_menu = Camera(RenderingLayer("map_layer"), menu_layer1, menu_layer2)
menu_scene = Scene(camera_menu)
map0 = Map(menu_scene)
menu_background = MenuBackground(menu_scene, menu_layer1)
menu_banner = MenuBanner(menu_scene, menu_layer1)


# MAIN SCENE
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
# SCENE loaders/transitions/buttons
main_scene_reseter = MainSceneReseter(main_scene)

def func_setinha_button():
    main_scene_reseter.reset_phase()
    game_loop.set_current_scene(menu_scene)
setinha_button = Button("game_res/setinha.png", "game_res/setinha_active.png",
                           pygame.Vector2(40, 40), 1.5, func_setinha_button, main_scene, cockpit_layer)

def func_start_button():
    main_scene_reseter.reset_phase()
    game_loop.set_current_scene(main_scene)
    print("menu => main scene")
menu_start_button = Button("game_res/menu/menu_start.png", "game_res/menu/menu_start_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight-40), 2,
                           func_start_button, menu_scene, menu_layer2)

def func_score_button():
    print("menu => scores")
menu_scores_button = Button("game_res/menu/menu_score_button.png", "game_res/menu/menu_score_button_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight+50), 2,
                           func_score_button, menu_scene, menu_layer2)

def func_exit_button():
    pygame.quit()
    sys.exit()
menu_exit_button = Button("game_res/menu/menu_exit.png", "game_res/menu/menu_exit_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight+140), 2,
                           func_exit_button, menu_scene, menu_layer2)


# GAME LOOP
game_loop.set_current_scene(menu_scene)
game_loop.run_game_loop()

