import pygame
from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.game_time_system import GameTime


class Bullet(GameObject):

    In_Scene_Bullets = []

    def __init__(self, initial_pos: pygame.Vector2, direction: pygame.Vector2, rotation_angle, scene):
        super().__init__("bullet", scene, scene.camera.get_rendering_layer_by_name("player_layer"))

        # initial pos
        self.transform.move_world_position(initial_pos)

        # destruction time
        self.time_to_destruction_in_seconds = 4
        self.timer_to_destruction = TimerComponent(self.time_to_destruction_in_seconds * 1000, self, self.set_bullet_to_garbage_collection)
        self.timer_to_destruction.activate()

        # sprite
        self.single_sprite = SpriteComponent("game_res/bullet.png", self)
        self.single_sprite.scale_sprite(1.5)

        # movement
        self.direction = direction
        self.BULLET_SPEED = 400

        # rotation
        self.transform.set_rotation(rotation_angle)

        Bullet.In_Scene_Bullets.append(self)

    def game_object_update(self) -> None:
        self._move_bullet_forward()

    def _move_bullet_forward(self):
        new_pos = self.transform.world_position_read_only + self.direction * self.BULLET_SPEED * GameTime.DeltaTime
        self.transform.move_world_position(new_pos)

    def set_bullet_to_garbage_collection(self):
        self.scene.remove_game_object(self)
        if self in Bullet.In_Scene_Bullets:
            Bullet.In_Scene_Bullets.remove(self)
