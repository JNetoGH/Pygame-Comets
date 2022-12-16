import pygame

from JNetoProductions_pygame_game_engine.systems._text_rendering_system import TextRenderOverlaySystem
from JNetoProductions_pygame_game_engine.systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.scene import Scene


class GameLoop:

    def __init__(self):

        pygame.init()

        # 21:9
        RES_WFHD= [2560, 1080]

        # 16:9
        RES_NHD = [640, 360]
        RES_FWVGA = [854, 480]
        RES_HD = [1280, 720]
        RES_HD_PLUS = [1600, 900]
        RES_FULL_HD = [1920, 1080]
        RES_2K_QHD = [2560, 1440]
        RES_4K = [3840, 2160]

        ScalableGameScreen.init_screens(RES_HD, RES_HD, RES_HD)

        # important stuff
        self.clock = pygame.time.Clock()

        # it is not used for much, just holds the total amount of update elapsed
        self.elapsed_updates = 0

        # running scene
        self._running_scene = None

        # should be the one of the last things to be instantiated
        self.inspector_debugging_canvas = None

        # show both the inspector lateral info and the gizmos
        self.show_inspector_debugging_canvas = False
        self.show_debugging_gizmos = False

    def run_game_loop(self):

        while True:

            pygame.display.set_caption(f"JNETO PRODUCTIONS PYGAME GAME ENGINE |  FPS {self.clock.get_fps():.1f}")

            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()

            # in case the is no scene set
            if self._running_scene is None:
                # clears the screen
                ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")
                font = pygame.font.Font('JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf', 50)  # create a text surface object,
                TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, "no scene set", (600, 400), font, color="white")
                ScalableGameScreen.render_final_scaled_result()
                continue

            self._running_scene.scene_update()
            self._running_scene.scene_render()

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
            ScalableGameScreen.render_final_scaled_result()

    def set_current_scene(self, scene: Scene):
        self._running_scene = scene
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self, self._running_scene, font_size=15)
