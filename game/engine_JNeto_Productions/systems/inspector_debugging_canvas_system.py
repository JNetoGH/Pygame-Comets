import pygame

from engine_JNeto_Productions.systems.input_manager_system import InputManager
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from engine_JNeto_Productions.systems.game_time_system import GameTime
from engine_JNeto_Productions.systems.special_text import TextRenderOverlaySystem

from engine_JNeto_Productions.scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, game_loop, scene: Scene, font_size=10):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.game_loop = game_loop
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('engine_JNeto_Productions/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,

        # black transparent rect
        s = pygame.Surface(
            (GameScreen.DummyScreenWidth // 3, GameScreen.DummyScreenHeight - 20))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        GameScreen.GameScreenDummySurface.blit(s, (10, 10))  # (0,0) are the top-left coordinates

        # the msgs
        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n\n" \
               f"ENGINE INNER DETAILS\n" \
               f"fps: {self.game_loop.clock.get_fps():.1f}\n" \
               f"elapsed updates: {self.game_loop.elapsed_updates}\n" \
               f"delta-time: {str(GameTime.DeltaTime)}\n\n" \
               f"{GameScreen.get_inspector_debugging_status()}\n" + \
               f"{InputManager.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.camera.get_inspector_debugging_status()}"

        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth // 3,
                                          msgs, (30, 30), font, color=pygame.Color("white"))

    def render_game_object_inspector_debugging_status(self, index_of_game_obj, color: str):
        font = pygame.font.Font('engine_JNeto_Productions/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,
        msgs = f"{self.current_scene.game_object_list[index_of_game_obj].get_inspector_debugging_status()}\n"
        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth * 2,
                                          msgs, (GameScreen.DummyScreenWidth // 3 * 2, 20), font,
                                          color=pygame.Color(color))
