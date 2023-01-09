import math
import pygame
from engine_JNeto_Productions.components.rect_collider_component import ColliderComponent
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from engine_JNeto_Productions.components.component_base_class._component_base_class import Component


class TransformComponent(Component):

    def __init__(self, game_object_owner):
        super().__init__(game_object_owner)
        self.__world_position: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__screen_position: pygame.Vector2 = pygame.Vector2()
        self.__is_center_point_appearing_on_screen = False
        self.__rotation_angle = 0

    # ------------------------------------------------------------------------------------------------------------------

    def component_update(self):
        # updates the screen position  a.k.a. image_rect position
        self.__screen_position = pygame.Vector2(self.game_object_owner.image_rect.centerx,
                                                self.game_object_owner.image_rect.centery)

        # updates __is_center_point_appearing_on_screen
        is_in_x = GameScreen.DummyScreenWidth > self.__screen_position.x > 0
        is_in_y = GameScreen.DummyScreenHeight > self.__screen_position.y > 0
        self.__is_center_point_appearing_on_screen = is_in_x and is_in_y

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def forward_direction(self):

        # I need to add 90º because my default orientation for 0 is ->, it's subtracted so 0º aims ↓ by default
        angle_in_rad = math.radians(self.__rotation_angle+90)

        # In pygame 1 in y goes ↓ instead of ↑, dir_y needs to be inverted
        dir_x = math.cos(angle_in_rad)
        dir_y = - math.sin(angle_in_rad)
        dir_from_angle = pygame.Vector2(dir_x, dir_y)

        # normalizes avoiding division by 0 exception
        dir_from_angle = dir_from_angle if dir_from_angle.magnitude() == 0 else dir_from_angle.normalize()

        def debug_info():
            print(f"angle (deg): {self.__rotation_angle}º")
            print(f"angle (rad): {angle_in_rad}")
            print(f"direction:   {dir_from_angle}\n")
        #debug_info()

        return dir_from_angle

    @property
    def rotation_angle_read_only(self):
        return self.__rotation_angle

    @property
    def screen_position_read_only(self):
        return self.__screen_position.copy()

    @property
    def world_position_read_only(self):
        return self.__world_position.copy()

    @property
    def is_center_point_appearing_on_screen_read_only(self):
        return self.__is_center_point_appearing_on_screen

    # ------------------------------------------------------------------------------------------------------------------

    def set_rotation(self, new_angle):
        self.__rotation_angle = new_angle
        self.__keep_rotation_angle_inside_0_to_360()

    def __keep_rotation_angle_inside_0_to_360(self):
        # it's not really necessary, it works with a 7232º, but I prefer keeping it in the ]0º, 360º] for visualization
        if self.__rotation_angle > 360:
            self.__rotation_angle = self.__rotation_angle = 0 + (self.__rotation_angle - 360)   # 0 + what passed from 360
        elif self.__rotation_angle < 0:
            self.__rotation_angle = self.__rotation_angle = 360 - (self.__rotation_angle * -1)  # 360 - what passed from 0

    # ------------------------------------------------------------------------------------------------------------------

    def translate_world_position(self, direction: pygame.Vector2):
        new_pos = pygame.Vector2(self.__world_position.x + direction.x, self.__world_position.y + direction.y)
        self.move_world_position(new_pos)

    def move_world_position(self, new_position):
        self.__world_position = new_position

    def move_world_position_with_collisions_calculations(self, new_position):

        # doesn't make the calculation if the new position is the same of the current position,
        # A.K.A. GameObject didn't move
        if new_position.x == self.__world_position.x and new_position.y == self.__world_position.y:
            return

        # if the object meant to be4 moved has no colliders, then it is simply moved with no calculations
        if not self.game_object_owner.has_collider:
            self.__world_position = new_position
            return

        # moves it if the new position is diff from the current position
        is_next_position_colliding = False
        other_game_object_colliders_list = []
        this_game_object_colliders_list = []

        # inits this game object colliders list
        for component in self.game_object_owner.components_list:
            if isinstance(component, ColliderComponent):
                this_game_object_colliders_list.append(component)

        for other_gm_obj in self.game_object_owner.scene.game_object_list:

            # if another game object have a collider it will remake the other game object colliders list
            if other_gm_obj != self.game_object_owner and other_gm_obj.has_collider:

                # fills the other game object colliders list
                for component in other_gm_obj.components_list:
                    if isinstance(component, ColliderComponent):
                        other_game_object_colliders_list.append(component)

                # checks for collision
                for i in range(len(this_game_object_colliders_list)):

                    this_game_object_collider = this_game_object_colliders_list[i]
                    projection_of_current_collider_rect_to_new_position = this_game_object_collider.inner_rect_read_only.copy()
                    # I have to round it, because pygame is stupid and only treats rects with in variables
                    # so, a 50.9 position, would be truncate to 50, removing the decimal part completely,
                    # by rounding it I make 4.8 = 5, 3.2 => 3, still not perfect, you can see little gaps
                    # but is way better than if I haven't done anything
                    projection_of_current_collider_rect_to_new_position.centerx = round(new_position.x + this_game_object_collider.offset_from_game_object_x)
                    projection_of_current_collider_rect_to_new_position.centery = round(new_position.y + this_game_object_collider.offset_from_game_object_y)

                    for other_game_obj_collider in other_game_object_colliders_list:
                        if projection_of_current_collider_rect_to_new_position.colliderect(other_game_obj_collider.inner_rect_read_only):
                            is_next_position_colliding = True

        if not is_next_position_colliding:
            self.__world_position = new_position

    # ------------------------------------------------------------------------------------------------------------------

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(TransformComponent)\n" \
               f"world position:  {self.__world_position}\n" \
               f"screen position: {self.__screen_position}\n" \
               f"rotation angle:  {self.__rotation_angle}ª"
