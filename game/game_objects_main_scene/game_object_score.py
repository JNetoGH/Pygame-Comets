import pygame

from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class Score(GameObject):

    def __init__(self, scene):
        super().__init__("score", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))

        self.remove_default_rect_image()
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, 20))

        self._score_points = 0
        self._score_points_text_render = TextRenderComponent(f"score {self._score_points}", 20, pygame.Color("white"), 0, 0, self)

    def add_to_score(self, num: int):
        self._score_points += num
        self._score_points_text_render.set_text(f"score {self._score_points}")

    def reset_score(self):
        self._score_points = 0

    def game_object_update(self) -> None:
        pass