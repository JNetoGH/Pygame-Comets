import random
import pygame
from engine_JNeto_Productions.components.rect_trigger_component import RectTriggerComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from game_objects_main_scene.game_object_meteor import Meteor


class MeteorManager(GameObject):

    def __init__(self, scene, rendering_layer):
        super().__init__("MeteorManager", scene, rendering_layer)

        self.remove_default_rect_image()
        self.stop_rendering_this_game_object()

        self._instantiation_rect_top = RectTriggerComponent(0, -470, 1000, 100, self)
        self._instantiation_rect_bottom = RectTriggerComponent(0, 470, 1000, 100, self)
        self._instantiation_rect_left = RectTriggerComponent(-550, 0, 100, 800, self)
        self._instantiation_rect_right = RectTriggerComponent(550, 0, 100, 800, self)
        self._instantiation_rect_list = [self._instantiation_rect_top, self._instantiation_rect_bottom,
                                         self._instantiation_rect_right, self._instantiation_rect_bottom]

        self._inst_frequency_in_seg = 0.75
        self._instantiation_timer = TimerComponent(self._inst_frequency_in_seg * 1000, self, self._instantiate_meteor)

    def game_object_update(self) -> None:
        if not self._instantiation_timer.is_timer_active_read_only:
            self._instantiation_timer.activate()

    def _instantiate_meteor(self):

        initial_pos = pygame.Vector2(0, 0)
        direction = pygame.Vector2(0, 0)

        # picked randomly
        instantiation_rect = self._instantiation_rect_list[random.randint(0, len(self._instantiation_rect_list) - 1)]

        # sets a random point inside the instantiation rect
        start_range_point_x = instantiation_rect.world_position_read_only.x - instantiation_rect.width / 2
        end_range_point_x = instantiation_rect.world_position_read_only.x + instantiation_rect.width / 2
        start_range_point_y = instantiation_rect.world_position_read_only.y - instantiation_rect.height / 2
        end_range_point_y = instantiation_rect.world_position_read_only.y + instantiation_rect.height / 2
        initial_pos.x = random.randint(round(start_range_point_x), round(end_range_point_x))
        initial_pos.y = random.randint(round(start_range_point_y), round(end_range_point_y))

        # direction
        if instantiation_rect == self._instantiation_rect_top or instantiation_rect == self._instantiation_rect_bottom:
            direction.y = 1 if instantiation_rect == self._instantiation_rect_top else direction.y
            direction.y = -1 if instantiation_rect == self._instantiation_rect_bottom else direction.y
            #                            x = 0.1 <=> 1                 sign + || -
            direction.x = (random.randint(1, 10) / 10) * random.choice([1, -1])  # output is like x = 0.7 or -0.7
        else:
            direction.x = 1 if instantiation_rect == self._instantiation_rect_left else direction.x
            direction.x = -1 if instantiation_rect == self._instantiation_rect_right else direction.x
            #                          y = 0.1 <=> 1                 sign + || -
            direction.y = (random.randint(1, 10) / 10) * random.choice([1, -1])  # output is like y = 0.4 or -0.4

        # rank
        # 50% small, 30% mid, 20% big
        rank = None
        rank_picker = random.randint(1, 10)
        if 1 <= rank_picker <= 5:
            rank = Meteor.MeteorRank.Small
        elif 6 <= rank_picker <= 8:
            rank = Meteor.MeteorRank.Mid
        elif rank_picker <= 10:
            rank = Meteor.MeteorRank.Big

        # ==============================================================================================================

        direction = direction.normalize()
        # print(f"meteor init: {initial_pos}, dir: {direction}, rank: {rank}")
        Meteor(self.scene, rank, initial_pos, direction)
