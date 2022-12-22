import random
import pygame
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_objects.game_object_meteor import Meteor


class MeteorManager(GameObject):

    def __init__(self, scene, rendering_layer):
        super().__init__("MeteorManager", scene, rendering_layer)

        self.remove_default_rect_image()
        self.stop_rendering_this_game_object()
        self._inst_frequency_in_seg = 0.5
        self._instantiation_timer = TimerComponent(self._inst_frequency_in_seg * 1000, self, self._instantiate_meteor)

    def game_object_update(self) -> None:
        if not self._instantiation_timer.is_timer_active_read_only:
            self._instantiation_timer.activate()

    def _instantiate_meteor(self):
        camera_pos = self.scene.camera.world_position_read_only
        camera_width = GameScreen.DummyScreenWidth
        camera_height = GameScreen.DummyScreenHeight
        """
        BASICALLY OUT OF THE FOV
              corner *  up_side_pos                     
                      |----------|
        left_side_pos |  camera  | () meteor instantiation point
                      |----------|
                                () meteor instantiation point
        """
        camera_square_left_side_position = round(camera_pos.x - camera_width//2)
        camera_square_up_side_position = round(camera_pos.y - camera_height//2)
        camera_corner_pos = pygame.Vector2(camera_square_left_side_position, camera_square_up_side_position)
        print(camera_corner_pos)

        # needs to be the bigger than the size of the meteor
        # will be added/sub of the x and y of the instantiation points
        safe_dist = 700

        initial_pos = pygame.Vector2(0, 0)
        initial_pos.x = random.choice([random.randrange(int(camera_corner_pos.x), camera_width-safe_dist), random.choice([-1 * safe_dist - 5, camera_height + 5])])
        initial_pos.y = random.choice([random.choice([-1 * safe_dist - 5, camera_width + 5]), random.randrange(int(camera_corner_pos.y), camera_height + safe_dist)])

        """
        # ORINAL BUGGY WAY
        # random.choice(
        # [(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])),
        # (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        instantiation_point = random.choice([
            (random.randrange(camera_square_left_side_position, camera_width-safe_dist), random.choice([-1 * safe_dist - 5, camera_height + 5])),
            (random.choice([-1 * safe_dist - 5, camera_width + 5]), random.randrange(camera_square_up_side_position, camera_height - safe_dist))])
       """


        # ==============================================================================================================

        direction = pygame.Vector2(0, 0)

        # left half
        if initial_pos.x < camera_width//2:
            direction.x = 1
        # right half
        else:
            direction.x = -1
        # upper half
        if initial_pos.y < camera_height//2:
            direction.y = 1
        # bottom half
        else:
            direction.y = -1

        # ==============================================================================================================

        print(f"meteor instantiated at {initial_pos}")
        Meteor(self.scene, Meteor.MeteorRank.Big, initial_pos, direction)
