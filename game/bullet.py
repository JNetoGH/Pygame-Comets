import pygame

from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class Bullet(GameObject):

    def __init__(self, name: str, scene):
        super().__init__(name, scene, scene.get_rendering_layer_by_name("player_layer"))

        # sprite
        self.single_sprite = SingleSpriteComponent("bullet.py", self)
        self.buffered_original_sprite = self.image.copy()

        # movement and rotation
        self.direction = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(0, 0)
        self.rotation = 0

    def game_object_update(self) -> None:
        pass

    def _move_bullet_forward(self):
        pass

    def _set_bullet_to_garbage_collection(self):
        self.scene.remove_game_object(self)
