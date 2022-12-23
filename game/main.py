import sys
import pygame

# ENGINE IMPORTS
from engine_JNeto_Productions.game_loop import GameLoop
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.rendering_layer import RenderingLayer
from engine_JNeto_Productions.camera import Camera
from engine_JNeto_Productions.scene import Scene
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_object_score_scene.black_filter_game_object import BlackFilter
from game_object_score_scene.score_registration_floating_menu import ScoreRegistrationFloatingMenu
from game_object_score_scene.text_holder_game_object import TextHolder
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent

# GAME OBJECTS IMPORTS
from game_objects_main_scene.game_object_cockpit import Cockpit
from game_objects_main_scene.game_object_difficulty_ui import DifficultyUi
from game_objects_main_scene.game_object_right_shoot_ui import RightShootUi
from game_objects_main_scene.game_object_map_limits import MapLimits
from game_objects_main_scene.game_object_map import Map
from game_objects_main_scene.game_object_meteor import Meteor
from game_objects_main_scene.game_object_meteor_manager import MeteorManager
from game_objects_main_scene.game_object_player import Player
from game_objects_main_scene.game_object_score import ScoreUi
from game_objects_main_scene.game_object_main_scene_reseter import MainSceneReseter
from game_objects_menu_scene.banner_game_object import MenuBanner
from game_objects_menu_scene.menu_background_game_object import MenuBackground
from engine_JNeto_Productions.prefabs.game_object_button import Button

# ======================================================================================================================
# ======================================================================================================================

# GAME LOOP
game_loop = GameLoop()

# ======================================================================================================================
# ======================================================================================================================

# MENU SCENE
menu_layer1 = RenderingLayer("menu_layer1")
menu_layer2 = RenderingLayer("menu_layer2")
camera_menu = Camera(RenderingLayer("map_layer"), menu_layer1, menu_layer2)
menu_scene = Scene(camera_menu)
map0 = Map(menu_scene)
menu_background = MenuBackground(menu_scene, menu_layer1)
menu_banner = MenuBanner(menu_scene, menu_layer1)

# ======================================================================================================================
# ======================================================================================================================

# SCORE SCENE
score_layer1 = RenderingLayer("score_layer1")
score_layer2 = RenderingLayer("score_layer2")
score_layer3 = RenderingLayer("score_layer3")
score_layer4 = RenderingLayer("score_layer4")
score_sence_camara = Camera(RenderingLayer("map_layer"), score_layer1, score_layer2, score_layer3, score_layer4)
score_scene = Scene(score_sence_camara)
map1 = Map(score_scene)
black_filter = BlackFilter(score_scene, score_layer1)
text_holder = TextHolder(score_scene, score_layer1)
score_registration_menu = ScoreRegistrationFloatingMenu(score_scene, score_layer4)

# ======================================================================================================================
# ======================================================================================================================

# GAME OVER SCENE
game_over_layer = RenderingLayer("game_over_layer")
game_over_camera = Camera(game_over_layer)
game_over_scene = Scene(game_over_camera)


class GameOverManager(GameObject):

    Count: bool = False
    Score = 0

    def __init__(self, scene, rendering_layer):
        super().__init__("game_over", scene, rendering_layer)

        self.game_over_sound = pygame.mixer.Sound("game_res/audio/annauncer/Game over 1.wav")

        self.remove_default_rect_image()
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight))
        self.header = TextRenderComponent("GAME OVER", 70, pygame.Color("white"), 0, 0, self)
        self.score_text = TextRenderComponent("SCORE: 0", 40, pygame.Color("white"), 0, 100, self)

        self.duration_in_seg = 4
        self.timer_comp = TimerComponent(self.duration_in_seg * 1000, self, self.change_scene)

    def game_object_update(self) -> None:

        # print(f"timer elapsed time: {self.timer_comp.elapsed_time_read_only} ms")
        # print(f"timer is activate: {self.timer_comp.is_timer_active_read_only}\n")

        if GameOverManager.Count:
            GameOverManager.Count = False
            self.game_over_sound.play()
            self.score_text.set_text(f"SCORE: {GameOverManager.Score}")
            self.timer_comp.activate()

    def change_scene(self):
        game_loop.set_current_scene(score_scene)


    @staticmethod
    def set_up(score):
        GameOverManager.Count = True
        GameOverManager.Score = score


game_over_manager_obj = GameOverManager(game_over_scene, game_over_layer)


# ======================================================================================================================
# ======================================================================================================================


# MAIN SCENE
# CAMERA AND RENDERING LAYERS
map_rendering_layer = RenderingLayer("map_layer")
player_rendering_layer = RenderingLayer("player_layer")
map_limits_layer = RenderingLayer("map_limits_layer")
over_player_layer = RenderingLayer("over_player_layer")
bars_layer = RenderingLayer("bars_layer")
cockpit_layer = RenderingLayer("cockpit_layer")
main_camera = Camera(map_rendering_layer, player_rendering_layer, over_player_layer, map_limits_layer, bars_layer,cockpit_layer)

# MAIN SCENE
main_scene = Scene(main_camera)

# GAME OBJECTS
map = Map(main_scene)
map_limits = MapLimits(main_scene)
player = Player(main_scene)
cockpit = Cockpit(main_scene, cockpit_layer)
right_shoot_ui = RightShootUi(main_scene)
score_ui = ScoreUi(main_scene)
difficulty_ui = DifficultyUi(main_scene, cockpit_layer)

Meteor.Game_loop = game_loop
Meteor.Game_Over_manager = game_over_manager_obj
meteor_manager = MeteorManager(main_scene, map_rendering_layer)


# ======================================================================================================================
# ======================================================================================================================


# SCENE loaders/transitions/buttons
main_scene_reseter = MainSceneReseter(main_scene)

def func_setinha_back_to_menu():
    main_scene_reseter.reset_phase()
    game_loop.set_current_scene(menu_scene)
    print("main scene => menu")
setinha_main_game_button = Button("game_res/setinha.png", "game_res/setinha_active.png",
                                   pygame.Vector2(40, 40), 1.5, func_setinha_back_to_menu, main_scene, cockpit_layer)

setinha_score_button = Button("game_res/setinha.png", "game_res/setinha_active.png",
                                   pygame.Vector2(40, 40), 1.5, func_setinha_back_to_menu, score_scene, score_layer4)

def func_start_button():
    main_scene_reseter.reset_phase()
    game_loop.set_current_scene(main_scene)
    print("menu => main scene")
menu_start_button = Button("game_res/menu/menu_start.png", "game_res/menu/menu_start_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight-40), 2,
                           func_start_button, menu_scene, menu_layer2)

def func_score_button():
    print("menu => scores")
    game_loop.set_current_scene(score_scene)
menu_scores_button = Button("game_res/menu/menu_score_button.png", "game_res/menu/menu_score_button_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight+50), 2,
                           func_score_button, menu_scene, menu_layer2)

def func_exit_button():
    pygame.quit()
    sys.exit()
menu_exit_button = Button("game_res/menu/menu_exit.png", "game_res/menu/menu_exit_active.png",
                           pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight+140), 2,
                           func_exit_button, menu_scene, menu_layer2)

# ======================================================================================================================
# ======================================================================================================================

# GAME LOOP
pygame.mixer.Sound("game_res/audio/annauncer/Welcome back 2.wav").play()
pygame.mixer.music.load("game_res/music/Sci Fi Ambiences - Heaven.wav")
pygame.mixer.music.play(-1)
game_loop.set_current_scene(menu_scene)
game_loop.run_game_loop()

