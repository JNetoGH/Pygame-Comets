import pygame
from JNeto_Productions_Engine.constants.pre_definied_screen_resolutions import *
from JNeto_Productions_Engine.systems._gizmos_and_debugging_text_rendering_system import TextRenderOverlaySystem
from JNeto_Productions_Engine.systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from JNeto_Productions_Engine.systems.input_manager_system import InputManager
from JNeto_Productions_Engine.systems.scalable_game_screen_system import GameScreen
from JNeto_Productions_Engine.systems.game_time_system import GameTime
from JNeto_Productions_Engine.scene import Scene


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

        # show both the inspector lateral info and the gizmos
        self.show_inspector_debugging_canvas = False
        self.show_debugging_gizmos = False

    def set_current_scene(self, scene: Scene):
        self._current_scene = scene
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self, self._current_scene, font_size=15)

    def run_game_loop(self):

        while True:

            pygame.display.set_caption(f"JNETO PRODUCTIONS PYGAME GAME ENGINE |  FPS {self.clock.get_fps():.1f}")

            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()

            # in case the is no scene set makes a scene saying that there is no scene
            if self._current_scene is None:
                # clears the screen
                GameScreen.GameScreenDummySurface.fill("darkgreen")
                font = pygame.font.Font('JNeto_Productions_Engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf', 50)  # create a text surface object,
                TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth, "no scene set", (600, 400), font, color="white")
                GameScreen.render_final_scaled_result()
                continue

            self._current_scene.scene_update()
            self._current_scene.scene_render()

            # debugging inspector system and gizmos
            if InputManager.is_key_pressed(pygame.K_z):
                self.show_inspector_debugging_canvas = True
            elif InputManager.is_key_pressed(pygame.K_x):
                self.show_inspector_debugging_canvas = False
            if InputManager.is_key_pressed(pygame.K_c):
                self.show_debugging_gizmos = True
            elif InputManager.is_key_pressed(pygame.K_v):
                self.show_debugging_gizmos = False

            if self.show_debugging_gizmos:
                self.inspector_debugging_canvas.render_scene_game_objects_gizmos()

            # needs to be on top of gizmos
            if self.show_inspector_debugging_canvas:
                self.inspector_debugging_canvas.render_inspector_debugging_text()
                self.inspector_debugging_canvas.render_game_object_inspector_debugging_status(1, "white")  # GmObj info

            # render the final produced frame
            GameScreen.render_final_scaled_result()
