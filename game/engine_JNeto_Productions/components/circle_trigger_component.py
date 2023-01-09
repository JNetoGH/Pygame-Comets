import pygame
from engine_JNeto_Productions.components.component_base_class._component_base_class import Component


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

    def is_there_overlap_with_point(self, point: pygame.Vector2):
        circle_pos = self.world_position_read_only
        squared_dist = (circle_pos.x - point.x) ** 2 + (circle_pos.y - point.y) ** 2
        return squared_dist <= self.radius ** 2

    def is_there_overlap_with_rect(self, rect: pygame.Rect):

        """                  (X2, Y2)
                    |-------|
                    |       |
                    |-------|
            (X1, Y1)
        """

        X1 = rect.x
        X2 = rect.x + rect.width
        Y1 = rect.y
        Y2 = rect.y + rect.height

        def smaller(a, b):
            if a < b:
                return a
            return b

        def bigger(a, b):
            if a > b:
                return a
            return b

        # - Finds the nearest point on the rectangle to the center of the circle
        Xn = bigger(X1, smaller(self.world_position_read_only.x, X2))
        Yn = bigger(Y1, smaller(self.world_position_read_only.y, Y2))

        # - Finds the distance between the nearest point and the center of the circle
        # - Distance between 2 points, (x1, y1) & (x2, y2) in 2D Euclidean space is ((x1-x2)**2 + (y1-y2)**2)**0.5
        Dx = Xn - self.world_position_read_only.x
        Dy = Yn - self.world_position_read_only.y
        return (Dx ** 2 + Dy ** 2) <= self.radius ** 2

    def get_inspector_debugging_status(self) -> str:
        return "Component(Circle Trigger)"
