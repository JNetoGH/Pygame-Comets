import math

import pygame
from engine_JNeto_Productions.components.component_base_class.component_base_class import Component


class CircleTriggerComponent(Component):
    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, radius, game_object_owner):
        super().__init__(game_object_owner)

        self.game_object_owner.has_circle_trigger = True

        # initiating fields
        self.radius = radius
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y

    @property
    def world_position_read_only(self):
        world_pos = pygame.Vector2()
        world_pos.x = self.game_object_owner.transform.world_position_read_only.x + self.offset_from_game_object_x
        world_pos.y = self.game_object_owner.transform.world_position_read_only.y + self.offset_from_game_object_y
        return world_pos.copy()

    def is_there_a_point_inside(self, point: pygame.Vector2):
        circle_pos = self.world_position_read_only
        squared_dist = (circle_pos.x - point.x) ** 2 + (circle_pos.y - point.y) ** 2
        return squared_dist <= self.radius ** 2

    def component_update(self):
       pass

    def get_inspector_debugging_status(self) -> str:
        return "Component(Circle Trigger)"
