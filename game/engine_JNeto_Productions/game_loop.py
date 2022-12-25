import pygame
from engine_JNeto_Productions.constants.pre_definied_screen_resolutions import *
from engine_JNeto_Productions.systems.gizmos_system import GizmosSystem
from engine_JNeto_Productions.systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from engine_JNeto_Productions.systems.input_manager_system import InputManager
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from engine_JNeto_Productions.systems.game_time_system import GameTime
from engine_JNeto_Productions.scene import Scene


class GameLoop:

    def __init__(self):

        pygame.init()

        GameScreen.init_screens(RES_ASTEROIDS, RES_ASTEROIDS, RES_ASTEROIDS)

        # important stuff are made with this, like fps count, fps lock
        self.clock = pygame.time.Clock()

        # it is not used for much, just holds the total amount of update elapsed
        self.elapsed_updates = 0

        # running scene
        self._current_scene = None

        # should be the one of the last things to be instantiated
        self.inspector_debugging_canvas = None
        self.gizmos_system = GizmosSystem()
        self.show_inspector_debugging_canvas = False
        self.show_debugging_gizmos = False

    def set_current_scene(self, scene: Scene):
        self._current_scene = scene
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self, self._current_scene, font_size=15)
        self.gizmos_system.set_current_scene(self._current_scene)
        self._current_scene.scene_start()

    def run_game_loop(self):
        while True:

            # updates the systems and stuff
            pygame.display.set_caption(f"JNETO PRODUCTIONS PYGAME GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()  # can't close the app window without it

            # in case the is no scene set makes a screen saying that there is no scene, and skip the rest of the loop
            if self._current_scene is None:
                GameLoop.__run_with_no_scene_set()
                continue

            # ==========================================================================================================

            # current scene update and render
            self._current_scene.scene_update()
            self._current_scene.scene_render()

            # ==========================================================================================================

            # debugging inspector system and gizmos, it needs to be on top of gizmos
            if InputManager.is_key_pressed(pygame.K_z):
                self.show_inspector_debugging_canvas = True
            elif InputManager.is_key_pressed(pygame.K_x):
                self.show_inspector_debugging_canvas = False
            if self.show_inspector_debugging_canvas:
                self.inspector_debugging_canvas.render_inspector_debugging_text()
                #self.inspector_debugging_canvas.render_game_object_inspector_debugging_status(1, "white")  # GmObj info

            # ==========================================================================================================

            if InputManager.is_key_pressed(pygame.K_c):
                self.show_debugging_gizmos = True
            elif InputManager.is_key_pressed(pygame.K_v):
                self.show_debugging_gizmos = False
            if self.show_debugging_gizmos:
                self.gizmos_system.render_scene_game_objects_gizmos()

            # ==========================================================================================================

            # renders the final produced frame
            GameScreen.render_final_scaled_result()

    @staticmethod
    def __run_with_no_scene_set():
        # clears the screen
        GameScreen.GameScreenDummySurface.fill("darkgreen")

        # font and font surface
        font = pygame.font.Font('engine_JNeto_Productions/_engine_resources/fonts/JetBrainsMono-Medium.ttf', 50)
        text_surface = font.render("no scene set", True, pygame.Color(255, 255, 255))

        # makes a centralized position at screen
        text_position = pygame.Vector2(0, 0)
        text_position.x = GameScreen.HalfDummyScreenWidth - (text_surface.get_width() / 2)
        text_position.y = GameScreen.HalfDummyScreenHeight - (text_surface.get_height() / 2)

        # blits and render final scaled result
        GameScreen.GameScreenDummySurface.blit(text_surface, text_position)
        GameScreen.render_final_scaled_result()
