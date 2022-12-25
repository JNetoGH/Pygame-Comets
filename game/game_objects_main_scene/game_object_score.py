import pygame

from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class ScoreUi(GameObject):

    def __init__(self, scene):
        super().__init__("score", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))

        self.remove_default_rect_image()
        self.single_sprite = SpriteComponent("game_res/main_game_score.png", self)
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, 24))
        self.single_sprite.scale_sprite(1.5)

        self._score_points = 0
        self._score_points_text_render = TextRenderComponent(f"{self._score_points}", 20, pygame.Color("white"), 40, 0, self)

    @property
    def score_points_read_only(self):
        return self._score_points

    def add_to_score(self, num: int):
        self._score_points += num
        self._score_points_text_render.set_text(f"{self._score_points}")

    def reset_score(self):
        self._score_points = 0
        self._score_points_text_render.set_text(f"{self._score_points}")

    def game_object_update(self) -> None:
        pass