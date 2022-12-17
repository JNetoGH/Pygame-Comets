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
        self.single_sprite = SingleSpriteComponent("res/test_player_sprite.png", self)
        self.single_sprite.scale_itself(2)

        # MAKES CAMERA FOLLOW PLAYER
        self.scene.main_camera.follow_game_object(self)

        # MOVEMENT
        self.move_speed = 200

        # ROTATION
        self.angle_text_render = TextRenderComponent("angle: 0", 20, pygame.Color(255, 255, 255), 0, -50, self)
        self.angle = 0
        self.angular_velocity = 300
        # pygame não faz a rotação direito, a cada rotação a imagem perde um pouco de detalhe, então é preciso
        # armazenar a original, para sempre fazer a rotação com base nela, pois os detalhes não foram perdidos.
        self.buffered_original_image = self.image.copy()

    def game_object_update(self) -> None:

        # rotates player according to A and D keys
        if InputManager.Horizontal_Axis != 0:
            self.rotate_player()

        # moves forward when W is pressed
        if InputManager.is_key_pressed(pygame.K_w):
            self.move_player_forward()

    def move_player_forward(self):

        # I need to add/sub more 180 because my default orientation for 0 is ↑ sited of 0º aiming ↓ by default
        angle_in_rad = math.radians(self.angle-180)

        # makes the direction, normalizing can't throw a division by 0 exception, because a (0,0) direction is impossible
        dir_from_angle = pygame.Vector2(math.sin(angle_in_rad), math.cos(angle_in_rad)).normalize()
        new_position = self.transform.world_position_read_only + dir_from_angle * self.move_speed * GameTime.DeltaTime
        self.transform.move_world_position_with_collisions_calculations(new_position)

    def rotate_player(self):

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
