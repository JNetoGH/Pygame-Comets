import math
import pygame.transform

from engine_JNeto_Productions.components.key_tracker_component import KeyTrackerComponent
from engine_JNeto_Productions.components.rect_collider_component import ColliderComponent
from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.game_time_system import GameTime
from engine_JNeto_Productions.systems.input_manager_system import InputManager
from game_objects_main_scene.game_object_bullet import Bullet
from game_objects_main_scene.game_object_right_shoot_ui import RightShootUi


class Player(GameObject):

    def __init__(self, scene):
        super().__init__("player", scene, scene.camera.get_rendering_layer_by_name("player_layer"))

        self.is_alive = True

        # SPRITE
        self.single_sprite = SpriteComponent("game_res/ship.png", self)
        self.single_sprite.scale_sprite(1.5)

        # COLLIDER
        self.player_collider = ColliderComponent(0, 0, 40, 40, self)

        # MAKES CAMERA FOLLOW PLAYER
        self.scene.camera.follow_game_object(self)
        self.key_p = KeyTrackerComponent(pygame.K_p, self)

        # BULLET
        self.instantiation_cooldown_in_sec = 1
        self.bullet_instantiation_timer = TimerComponent(self.instantiation_cooldown_in_sec*1000, self)
        self.bullet_sound_effect = pygame.mixer.Sound("game_res/audio/shot.wav")

        # MOVEMENT
        self.BASE_MAX_MOVE_SPEED = 250
        self.ACCELERATION = 300
        self.DECELERATION = 200
        self.current_speed = 1
        self.dir_from_angle = pygame.Vector2(0,0)

        # ROTATION
        self.angular_velocity = 200
        # pygame não faz a rotação direito, a cada rotação a imagem perde um pouco de detalhe, então é preciso
        # armazenar a original, para sempre fazer a rotação com base nela, pois os detalhes não foram perdidos.
        self.buffered_original_image = self.image.copy()

    # ------------------------------------------------------------------------------------------------------------------

    def game_object_update(self) -> None:

        # CAMERA FOCUS
        if self.key_p.has_key_been_fired_at_this_frame_read_only:
            self.scene.camera.follow_game_object(self if self.scene.camera.get_followed_game_object() != self else None)

        # SHOOTING
        # shoots a bullet and then waits til the counter has finished counting to instantiate the nex bullet
        if InputManager.is_key_pressed(pygame.K_SPACE) and not self.bullet_instantiation_timer.is_timer_active_read_only:
            self._shoot()
        # lateral shoot bar sync
        RightShootUi.ElapsedTime = self.bullet_instantiation_timer.elapsed_time_read_only

        # MOVEMENT
        # moves forward when W or UP arrow is pressed
        if InputManager.Vertical_Axis == -1:
            self._accelerate()
            self._move_player_forward()
        elif self.current_speed > 0:
            self._decelerate()
            self._move_player_forward()

        # ROTATION
        # rotates player according to A, D, < adn >keys
        if InputManager.Horizontal_Axis != 0:
            self._rotate_player()

    # ------------------------------------------------------------------------------------------------------------------

    # SHOOTING
    def _shoot(self):
        self.bullet_instantiation_timer.activate()
        self._instantiate_bullet()
        pygame.mixer.Sound.play(self.bullet_sound_effect)
        # lateral shoot bar sync
        RightShootUi.TotWaitTime = self.bullet_instantiation_timer.duration_in_ms_read_only

    def _instantiate_bullet(self):
        Bullet(self.transform.world_position_read_only, self.transform.forward_direction,
               self.transform.rotation_angle_read_only, self.scene)

    # ------------------------------------------------------------------------------------------------------------------

    # MOVEMENT
    def _move_player_forward(self):
        # new position with acceleration or deceleration til its stop or on max speed
        new_pos = self.transform.world_position_read_only + self.transform.forward_direction * self.current_speed * GameTime.DeltaTime
        self.transform.move_world_position_with_collisions_calculations(new_pos)
        #self.transform.move_world_position(new_pos)

    def _accelerate(self):
        self.current_speed = self.current_speed + (self.ACCELERATION * GameTime.DeltaTime)
        if self.current_speed > self.BASE_MAX_MOVE_SPEED:
            self.current_speed = self.BASE_MAX_MOVE_SPEED

    def _decelerate(self):
        self.current_speed = self.current_speed - (self.DECELERATION * GameTime.DeltaTime)
        if self.current_speed < 0:
            self.current_speed = 0

    # ------------------------------------------------------------------------------------------------------------------

    # ROTATION
    def _rotate_player(self):
        # increments(A)/decrements(D) the angle according to angular speed
        new_rotation = self.transform.rotation_angle_read_only
        if InputManager.Horizontal_Axis == -1:
            new_rotation = self.transform.rotation_angle_read_only + self.angular_velocity * GameTime.DeltaTime
        if InputManager.Horizontal_Axis == 1:
            new_rotation = self.transform.rotation_angle_read_only - self.angular_velocity * GameTime.DeltaTime
        self.transform.set_rotation(new_rotation)
