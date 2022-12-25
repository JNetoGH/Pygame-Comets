import pygame
from os import walk   # allow us to walk through folders
from engine_JNeto_Productions.components.sprite_component import SpriteComponent


# it's basically a list of images
class AnimationClip:

    def __init__(self, name: str, animation_speed, folder_path: str):
        self.name = name
        self.images = []
        self.animation_speed = animation_speed
        self.__import_images_from_folder(folder_path)

    # imports every image inside a folder
    def __import_images_from_folder(self, folder_path) -> None:
        surface_list = []
        print("importing ", end="")
        for folder_name, sub_folder, img_files_list in walk(folder_path):
            print(f"{folder_name} => {img_files_list}:")
            for img_name in img_files_list:
                img_path = folder_path + "/" + img_name
                print(f"{img_path}")
                img_surface = pygame.image.load(img_path).convert_alpha()
                surface_list.append(img_surface)
            print()
        for surface_img in surface_list:
            self.images.append(surface_img)

    def add_frame(self, image_path) -> None:
        image_surface = pygame.image.load(image_path).convert_alpha()
        self.images.append(image_surface)

    def scale_all_frames_of_this_animation(self, scale):
        for i in range(0, len(self.images)):
            self.images[i] = SpriteComponent.return_scaled_image_surface(self.images[i], scale)
