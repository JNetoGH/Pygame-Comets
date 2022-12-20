import math
import pygame.transform
from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager


class Player(GameObject):

    def __init__(self, scene):
        super().__init__("player", scene, scene.get_rendering_layer_by_name("player_layer"))

        # SPRITE
        self.single_sprite = SingleSpriteComponent("res/ship.png", self)
        self.single_sprite.scale_itself(1.5)

        # MAKES CAMERA FOLLOW PLAYER
        self.scene.main_camera.follow_game_object(self)

        # MOVEMENT
        self.BASE_MAX_MOVE_SPEED = 350
        self.ACCELERATION = 300
        self.DECELERATION = 300
        self.current_speed = 1
        self.speed_text_render = TextRenderComponent("speed: 0 units/s", 15, pygame.Color(255, 255, 255), 0, -90, self)
        self.speed_status_text_render = TextRenderComponent("status: stop", 15, pygame.Color(255, 255, 255), 0, -70, self)

        # ROTATION
        self.angle_text_render = TextRenderComponent("angle: 0º", 15, pygame.Color(255, 255, 255), 0, -50, self)
        self.angle = 0
        self.angular_velocity = 300
        # pygame não faz a rotação direito, a cada rotação a imagem perde um pouco de detalhe, então é preciso
        # armazenar a original, para sempre fazer a rotação com base nela, pois os detalhes não foram perdidos.
        self.buffered_original_image = self.image.copy()

    def game_object_update(self) -> None:

        if InputManager.is_key_pressed(pygame.K_SPACE):
            self._shoot()

        # moves forward when W or UP arrow is pressed
        if InputManager.Vertical_Axis == -1:
            self._accelerate()
            self._move_player_forward()
        elif self.current_speed > 0:
            self._decelerate()
            self._move_player_forward()

        self._update_speed_related_texts()

        # rotates player according to A, D, < adn >keys
        if InputManager.Horizontal_Axis != 0:
            self._rotate_player()


    def _shoot(self):
        print("shoot")

    def _move_player_forward(self):
        # I need to add/sub more 180 because my default orientation for 0 is ↑ sited of 0º aiming ↓ by default
        angle_in_rad = math.radians(self.angle-180)

        # makes the direction, normalizing can't throw a division by 0 exception, because a (0,0) direction is impossible
        dir_from_angle = pygame.Vector2(math.sin(angle_in_rad), math.cos(angle_in_rad)).normalize()

        # new position with acceleration or deceleration til its stop or on max speed
        new_position = self.transform.world_position_read_only + dir_from_angle * self.current_speed * GameTime.DeltaTime
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

        # updates the text
        self.angle_text_render.change_text(f"angle: {self.angle:.2f}º")

    def _update_speed_related_texts(self):

        # speed text itself
        self.speed_text_render.change_text(f"speed: {self.current_speed:.0f} units/s")

        # speed status
        if InputManager.Vertical_Axis == -1:
            if self.current_speed >= self.BASE_MAX_MOVE_SPEED:
                self.speed_status_text_render.change_text("status: MAX SPEED")
                self.speed_status_text_render.change_color(pygame.Color(255, 255, 150))
                return
            self.speed_status_text_render.change_text("status: accelerating")
            self.speed_status_text_render.change_color(pygame.Color(120, 225, 120))
        elif self.current_speed > 0:
            self.speed_status_text_render.change_text("status: decelerating")
            self.speed_status_text_render.change_color(pygame.Color(255, 120, 120))
        elif self.current_speed == 0:
            self.speed_status_text_render.change_text("status: stop")
            self.speed_status_text_render.change_color(pygame.Color(255, 255, 255))