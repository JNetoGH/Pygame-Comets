import pygame

from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime


class Meteor(GameObject):

    def __init__(self, scene):
        super().__init__("meteor", scene, scene.get_rendering_layer_by_name("over_player_layer"))
        self.sigle_sprite = SingleSpriteComponent("res/meteor.png", self)
        self.sigle_sprite.scale_itself(0.1)
        self.transform.move_world_position(pygame.Vector2(300, 300))

        self.move_speed = 100
        self.direction_to_player = pygame.Vector2(0, 0)
        self.direction_text_renderer = TextRenderComponent(
            f"dir to player{self.direction_to_player}", 20, pygame.Color("cyan"), 0, -50, self)

        self.player = self.scene.get_game_object_by_name("player")

    def game_object_update(self) -> None:
        self.move_to_player_direction()

    def move_to_player_direction(self):

        self.direction_to_player = self.player.transform.world_position_read_only - self.transform.world_position_read_only

        # avoids division by zero exception for normalizing a (0,0) vector
        if self.direction_to_player.magnitude() == 0:
            return
        self.direction_to_player = self.direction_to_player.normalize()

        self.direction_text_renderer.change_text(f"dir to player{self.direction_to_player}")
        new_position = self.transform.world_position_read_only + self.direction_to_player * self.move_speed * GameTime.DeltaTime
        self.transform.move_world_position(new_position)
