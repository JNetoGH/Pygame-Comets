import pygame
from engine_JNeto_Productions.components.single_sprite_component import SingleSpriteComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.game_time_system import GameTime


class Bullet(GameObject):

    def __init__(self, initial_pos: pygame.Vector2, direction: pygame.Vector2, rotation_angle, scene):
        super().__init__("bullet", scene, scene.camera.get_rendering_layer_by_name("player_layer"))

        # initial pos
        self.transform.move_world_position(initial_pos)

        # destruction time
        self.time_to_destruction_in_seconds = 4
        self.timer_to_destruction = TimerComponent(self.time_to_destruction_in_seconds * 1000, self, self._set_bullet_to_garbage_collection)
        self.timer_to_destruction.activate()

        # sprite
        self.single_sprite = SingleSpriteComponent("game_res/bullet.png", self)
        self.single_sprite.scale_itself(1.5)

        # movement
        self.direction = direction
        self.BULLET_SPEED = 400

        # rotation
        self.image = pygame.transform.rotate(self.image, rotation_angle).convert_alpha()

    def game_object_update(self) -> None:
        self._move_bullet_forward()

    def _move_bullet_forward(self):
        new_pos = self.transform.world_position_read_only + self.direction * self.BULLET_SPEED * GameTime.DeltaTime
        self.transform.move_world_position(new_pos)

    def _set_bullet_to_garbage_collection(self):
        self.scene.remove_game_object(self)