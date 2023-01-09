import pygame
from engine_JNeto_Productions.components.component_base_class._component_base_class import Component


class SpriteComponent(Component):

    def __init__(self, img_path: str, game_object_owner):
        super().__init__(game_object_owner)

        # simply stores the path to the img file
        self.__img_path: str = img_path

        # - Pygame does not __rotate_sprite correctly, with each rotation the image loses a little detail, so it is
        #   necessary to store the original, in order to always __rotate_sprite based on it, as details are not lost.
        # - For scaling is the same
        self.original_image = pygame.image.load(self.__img_path).convert_alpha()
        self.game_object_owner.image = self.original_image.copy()
        self.image_copy_for_scaling = self.original_image.copy()
        self.image_copy_for_rotation = self.original_image.copy()

        # used for performance assurance, only rotates when the angle changes
        self._last_angle = 0

    # ------------------------------------------------------------------------------------------------------------------

    # syncs the rotation with the transform rotation angle
    def component_update(self):
        # used for performance assurance, only rotates when the angle changes
        current_angle = self.game_object_owner.transform.rotation_angle_read_only
        if self._last_angle == current_angle:
            return
        self._last_angle = current_angle
        self.__rotate_sprite(self._last_angle)

    # ------------------------------------------------------------------------------------------------------------------

    def get_img_path(self) -> str:
        return self.__img_path

    def change_image(self, new_img_path) -> None:
        self.__img_path = new_img_path
        self.original_image = pygame.image.load(self.__img_path).convert_alpha()
        self.game_object_owner.image = self.original_image
        self.image_copy_for_scaling = self.original_image.copy()
        self.image_copy_for_rotation = self.original_image.copy()

    # scaled like 0.8 = 80%
    def scale_sprite(self, scale) -> None:
        self.image_copy_for_scaling = SpriteComponent.return_scaled_image_surface(self.original_image, scale)
        self.game_object_owner.image = self.image_copy_for_scaling

    # ------------------------------------------------------------------------------------------------------------------

    # USED ONLY INTERNALLY:
    # - It's done whenever the transform rotation changes
    # - The rotation occurs based on the image_copy_for_scaling, in order to keep proportions while rotation,
    #   otherwise, it would shrink back to the originals proportions
    def __rotate_sprite(self, angle) -> None:
        self.image_copy_for_rotation = SpriteComponent.return_rotated_image_surface(self.image_copy_for_scaling, angle)
        self.game_object_owner.image = self.image_copy_for_rotation

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def return_scaled_image_surface(surface_img, scale) -> pygame.Surface:  # scaled like 0.8 = 80%
        return pygame.transform.scale(surface_img, (surface_img.get_width() * scale, surface_img.get_height() * scale)).convert_alpha()

    @staticmethod
    def return_rotated_image_surface(surface_img, angle) -> pygame.Surface:
        return pygame.transform.rotate(surface_img, angle).convert_alpha()

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(SpriteComponent)\n" \
               f"path: {self.__img_path}\n"
