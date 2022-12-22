import math
import pygame.transform

from engine_JNeto_Productions.components.key_tracker_component import KeyTrackerComponent
from engine_JNeto_Productions.components.rect_collider_component import ColliderComponent
from engine_JNeto_Productions.components.single_sprite_component import SingleSpriteComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.game_time_system import GameTime
from engine_JNeto_Productions.systems.input_manager_system import InputManager
from game_objects_main_scene.game_object_bullet import Bullet


class Player(GameObject):

    def __init__(self, scene):
        super().__init__("player", scene, scene.camera.get_rendering_layer_by_name("player_layer"))

        # SPRITE
        self.single_sprite = SingleSpriteComponent("game_res/ship.png", self)
        self.single_sprite.scale_itself(1.5)

        # COLLIDER
        self.player_collider = ColliderComponent(0, 0, 40, 40, self)

        # MAKES CAMERA FOLLOW PLAYER
        self.scene.camera.follow_game_object(self)
        self.key_p = KeyTrackerComponent(pygame.K_p, self)
        self.is_followed = True

        # BULLET
        self.instantiation_cooldown_in_sec = 1
        self.bullet_instantiation_timer = TimerComponent(self.instantiation_cooldown_in_sec*1000, self)

        # MOVEMENT
        self.BASE_MAX_MOVE_SPEED = 250
        self.ACCELERATION = 300
        self.DECELERATION = 200
        self.current_speed = 1
        self.dir_from_angle = pygame.Vector2(0,0)

        # ROTATION
        self.angle = 0
        self.angular_velocity = 200
        # pygame não faz a rotação direito, a cada rotação a imagem perde um pouco de detalhe, então é preciso
        # armazenar a original, para sempre fazer a rotação com base nela, pois os detalhes não foram perdidos.
        self.buffered_original_image = self.image.copy()

    def game_object_update(self) -> None:

        # CAMERA CONTROL
        if self.key_p.has_key_been_fired_at_this_frame_read_only:
            if self.is_followed:
                self.scene.camera.stop_following_current_set_game_object()
                self.is_followed = False
            else:
                self.scene.camera.follow_game_object(self)
                self.is_followed = True

        # MOVE DIRECTION
        self._generate_direction_from_ship_angle()

        # SHOOTING
        # shoos a bullet and then waits til the counter has finished counting to instantiate the nex bullet
        if InputManager.is_key_pressed(pygame.K_SPACE) and not self.bullet_instantiation_timer.is_timer_active_read_only:
            self.bullet_instantiation_timer.activate()
            self._instantiate_bullet()

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

    def _instantiate_bullet(self):
        Bullet(self.transform.world_position_read_only, self.dir_from_angle, self.angle, self.scene)

    def _generate_direction_from_ship_angle(self):
        # I need to add/sub more 180 because my default orientation for 0 is ↑ sited of 0º aiming ↓ by default
        angle_in_rad = math.radians(self.angle-180)
        # makes the direction, normalizing can't throw a division by 0 exception, because a (0,0) direction is impossible
        self.dir_from_angle = pygame.Vector2(math.sin(angle_in_rad), math.cos(angle_in_rad)).normalize()

    def _move_player_forward(self):
        # new position with acceleration or deceleration til its stop or on max speed
        new_position = self.transform.world_position_read_only + self.dir_from_angle * self.current_speed * GameTime.DeltaTime
        self.transform.move_world_position_with_collisions_calculations(new_position)
        # self.transform.move_world_position(new_position)

    def _accelerate(self):
        self.current_speed = self.current_speed + (self.ACCELERATION * GameTime.DeltaTime)
        if self.current_speed > self.BASE_MAX_MOVE_SPEED:
            self.current_speed = self.BASE_MAX_MOVE_SPEED

    def _decelerate(self):
        # new position with acceleration
        self.current_speed = self.current_speed - (self.DECELERATION * GameTime.DeltaTime)
        if self.current_speed < 0:
            self.current_speed = 0

    def _rotate_player(self):

        # increments(A)/decrements(D) the angle according to angular speed
        self.angle = self.angle + self.angular_velocity * GameTime.DeltaTime if InputManager.Horizontal_Axis == -1 else self.angle
        self.angle = self.angle - self.angular_velocity * GameTime.DeltaTime if InputManager.Horizontal_Axis == 1 else self.angle

        # it's not really necessary, it works with a 7232º, but I prefer keeping it in the ]0º, 360º] for visualization
        self.angle = self.angle = 0 + (self.angle - 360) if self.angle > 360 else self.angle  # 0   + oq passou de 360
        self.angle = self.angle = 360 - (self.angle * -1) if self.angle < 0 else self.angle   # 360 - oq passou de 0

        # rotates keeping the buffered image as it its
        self.image = pygame.transform.rotate(self.buffered_original_image, self.angle)