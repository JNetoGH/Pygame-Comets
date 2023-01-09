import pygame
from engine_JNeto_Productions.components.component_base_class._component_base_class import Component


class RectTriggerComponent(Component):
    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, width, height, game_object_owner):
        super().__init__(game_object_owner)

        self.game_object_owner.has_rect_trigger = True

        # initiating fields
        self.width = width
        self.height = height
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y

        self.__trigger_inner_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        # - Sets trigger_inner_rectangle default shape and position
        # - Pygame is stupid, it only uses ints to represent rectangle what truncates the float from 1.9 to 1 for example
        #   making pretty bad collision, so I am rounding what makes 1.9 => 2 and 1.2 => 1, what is a bit better,
        #   but still not perfect, just because it's an approximation.
        self.__trigger_inner_rect.width = self.width
        self.__trigger_inner_rect.height = self.height
        self.__realign_with_game_object_owner()

    @property
    def world_position_read_only(self):
        world_pos = pygame.Vector2()
        world_pos.x = self.game_object_owner.transform.world_position_read_only.x + self.offset_from_game_object_x
        world_pos.y = self.game_object_owner.transform.world_position_read_only.y + self.offset_from_game_object_y
        return world_pos.copy()

    @property
    def inner_rect_read_only(self):
        return self.__trigger_inner_rect.copy()

    def is_there_overlap_with_point(self, point: pygame.Vector2):
        return self.__trigger_inner_rect.collidepoint(point.x, point.y)

    # every frame it realigns it-self with its owner, so it moves along with the owner
    def component_update(self):
        self.__realign_with_game_object_owner()

    # every frame it realigns it-self with its owner, so it moves along with the owner
    def __realign_with_game_object_owner(self):

        # updates just in case they get changed in the middle of the game
        self.__trigger_inner_rect.width = self.width
        self.__trigger_inner_rect.height = self.height

        # I have to round it, because pygame is stupid and only treats rects with in variables
        # so, a 50.9 position, would be truncate to 50, removing the decimal part completely,
        # by rounding it I make 4.8 = 5, 3.2 => 3, still not perfect, you can see little gaps
        # but is way better than if I haven't done anything
        self.__trigger_inner_rect.centerx = round(self.game_object_owner.transform.world_position_read_only.x + self.offset_from_game_object_x)
        self.__trigger_inner_rect.centery = round(self.game_object_owner.transform.world_position_read_only.y + self.offset_from_game_object_y)

    def get_inspector_debugging_status(self) -> str:
        return "Component(Rect Trigger)"
