import pygame
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.component_base_class.component_base_class import Component


class TransformComponent(Component):
    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self.world_position: pygame.Vector2 = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight)
        self._screen_position: pygame.Vector2 = pygame.Vector2()
        self._is_center_point_appearing_on_screen = False

    @property
    def screen_position_read_only(self):
        return self._screen_position

    @property
    def is_center_point_appearing_on_screen_read_only(self):
        return self._is_center_point_appearing_on_screen

    def translate_world_position(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(self.world_position.x + direction.x, self.world_position.y + direction.y)
        self.move_world_position(new_pos)

    def move_world_position(self, new_position):
        self.world_position = new_position

    def move_world_position_with_collisions_calculations(self, new_position):

        # doesn't make the calculation if the new position is the same of the current position,
        # A.K.A GameObject didn't move
        if new_position.x == self.world_position.x and new_position.y == self.world_position.y:
            return

        # if the object meant to be4 moved has no colliders, then it is simply moved with no calculations
        if not self.game_object_owner.has_collider:
            self.world_position = new_position
            return

        # moves it if the new position is diff from the current position
        is_next_position_colliding = False
        other_game_object_colliders_list = []
        this_game_object_colliders_list = []

        # inits this game_loop object colliders list
        for component in self.game_object_owner.components_list:
            if isinstance(component, ColliderComponent):
                this_game_object_colliders_list.append(component)

        for other_gm_obj in self.game_object_owner.scene.all_game_obj:

            # if another game_loop object have a collider it will remake the other game_loop object colliders list
            if other_gm_obj != self.game_object_owner and other_gm_obj.has_collider:

                # fills the other game_loop object colliders list
                for component in other_gm_obj.components_list:
                    if isinstance(component, ColliderComponent):
                        other_game_object_colliders_list.append(component)

                # checks for collision
                for i in range(len(this_game_object_colliders_list)):

                    this_game_object_collider = this_game_object_colliders_list[i]
                    projection_of_current_collider_rect_to_new_position = this_game_object_collider.collider_rect.copy()
                    # I have to round it, because pygame is stupid and only treats rects with in variables
                    # so, a 50.9 position, would be truncate to 50, removing the decimal part completely,
                    # by rounding it I make 4.8 = 5, 3.2 => 3, still not perfect, you can see little gaps
                    # but is way better than if I haven't done anything
                    projection_of_current_collider_rect_to_new_position.centerx = round(new_position.x + this_game_object_collider.offset_from_game_object_x)
                    projection_of_current_collider_rect_to_new_position.centery = round(new_position.y + this_game_object_collider.offset_from_game_object_y)

                    for other_game_obj_collider in other_game_object_colliders_list:

                        if projection_of_current_collider_rect_to_new_position.colliderect(other_game_obj_collider.collider_rect):
                            is_next_position_colliding = True

        if not is_next_position_colliding:
            self.world_position = new_position




    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(TransformComponent)\n" \
               f"world position:  {self.world_position}\n" \
               f"screen position: {self._screen_position}\n"

    def component_update(self):
        # updates the screen position  a.k.a. image_rect position
        self._screen_position = pygame.Vector2(self.game_object_owner.image_rect.centerx, self.game_object_owner.image_rect.centery)
        # updates _is_center_point_appearing_on_screen
        is_in_x = ScalableGameScreen.DummyScreenWidth > self._screen_position.x > 0
        is_in_y = ScalableGameScreen.DummyScreenHeight > self._screen_position.y > 0
        self._is_center_point_appearing_on_screen = is_in_x and is_in_y
