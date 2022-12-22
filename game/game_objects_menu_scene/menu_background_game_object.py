import pygame

from engine_JNeto_Productions.components.single_sprite_component import SingleSpriteComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class MenuBackground(GameObject):

    def __init__(self, scene, rendering_layer):
        super().__init__("menu_back_ground", scene, rendering_layer)
        self.remove_default_rect_image()
        self.transform.move_world_position(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfRealScreenHeight+50))

        self.single_sprite = SingleSpriteComponent("game_res/menu/menu_background.png", self)
        self.single_sprite.scale_itself(1.5)

    def game_object_update(self) -> None:
        pass

