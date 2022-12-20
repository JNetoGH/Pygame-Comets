import math
import pygame.transform

from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.timer_component import TimerComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager
from game_object_bullet import Bullet


class Player(GameObject):

    def __init__(self, scene):
        super().__init__("player", scene, scene.get_rendering_layer_by_name("player_layer"))

        # SPRITE
        self.single_sprite = SingleSpriteComponent("res/ship.png", self)
        self.single_sprite.scale_itself(1.5)

        # COLLIDER
        self.player_collider = ColliderComponent(0, 0, 40, 40, self)

        # MAKES CAMERA FOLLOW PLAYER
        self.scene.main_camera.follow_game_object(self)

        # BULLET
        self.instantiation_cooldown_in_sec = 1
        self.bullet_instantiation_timer = TimerComponent(self.instantiation_cooldown_in_sec*1000, self)

        # MOVEMENT
        self.BASE_MAX_MOVE_SPEED = 250
        self.ACCELERATION = 300
        self.DECELERATION = 300
        self.current_speed = 1
        self.dir_from_angle = pygame.Vector2(0,0)

        # ROTATION
        self.angle = 0
        self.angular_velocity = 200
        # pygame não faz a rotação direito, a cada rotação a imagem perde um pouco de detalhe, então é preciso
        # armazenar a original, para sempre fazer a rotação com base nela, pois os detalhes não foram perdidos.
        self.buffered_original_image = self.image.copy()

    def game_object_update(self) -> None:

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