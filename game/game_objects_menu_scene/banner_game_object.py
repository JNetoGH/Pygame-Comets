import pygame

from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class MenuBanner(GameObject):

    def __init__(self, scene, rendering_layer):
        super().__init__("menu_banner", scene, rendering_layer)
        self.remove_default_rect_image()
        self.transform.move_world_position(pygame.Vector2(GameScreen.HalfDummyScreenWidth, 80))

        self.single_sprite = SpriteComponent("game_res/menu/menu_nome_jogo.png", self)
        self.single_sprite.scale_sprite(2.5)

    def game_object_update(self) -> None:
        pass

