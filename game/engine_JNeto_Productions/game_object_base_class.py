import pygame
from engine_JNeto_Productions.components.transform_component import TransformComponent
from abc import abstractmethod


class GameObject(pygame.sprite.Sprite):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__()

        # yes, because why not? It's useful in many situations
        self.name = name

        # in case False the SceneCamera won't render this GameObject
        self.should_be_rendered: bool = True

        # when a component is instantiated, it is automatically stored here
        self.components_list = []

        # holds the scene that the game object is part of, and adds itself in it
        self.scene = scene
        scene.game_object_list.append(self)

        # sets the transform
        # every game object in JNeto Production GameLoop Engine must have a TransformComponent
        self.transform = TransformComponent(self)

        # sets the rendering layer, and adds itself to it
        self.rendering_layer = rendering_layer
        self.rendering_layer.add_game_object(self)

        # makes a default img to the object, it's a white rect
        # sprites or animation override it
        self.image = pygame.Surface((100, 100))
        self.image.fill("white")
        # - The rectangle that holds the game object's image
        # - The center pos of the image_rect (a.k.a. screen position) is the same of the gm obj pos by default
        # - This rect is mostly used to hold the game object screen position (not world position), it's quite used.
        self.image_rect = self.image.get_rect(center=self.transform.world_position_read_only)

        # used by the camera to ignore the world position when rendering the GameObject,
        # by using the fixed_position_on_screen
        self.is_fixed_on_screen = False
        self._fixed_position_on_screen = pygame.Vector2(0, 0)

        # when a collider is added to the game object it changes this field to True, used mainly for gizmos
        self.has_collider = False
        # same but for rect trigger components
        self.has_rect_trigger = False
        # same but for circle trigger components
        self.has_circle_trigger = False

    # pygame is stupid and has already an update method for sprites(a.k.a. game obj super class)
    # so I had to call it this way, this is the most important method of the entire engine_JNeto_Productions
    # should be overriden by all GameObjects
    @abstractmethod
    def game_object_update(self) -> None:
        pass

    @abstractmethod
    def game_object_scene_set_start(self) -> None:
        pass

    def remove_component(self, component):
        if isinstance(component, TransformComponent):
            return
        for c in self.components_list:
            if c == component:
                self.components_list.remove(component)

    def add_component(self, component):
        if isinstance(component, TransformComponent):
            return
        self.components_list.append(component)

    def fix_game_object_on_screen(self, fixed_position_on_screen: pygame.Vector2):
        self.is_fixed_on_screen = True
        self._fixed_position_on_screen = fixed_position_on_screen

    def unfix_game_object_on_screen(self):
        self.is_fixed_on_screen = False

    def stop_rendering_this_game_object(self):
        self.should_be_rendered = False

    def start_rendering_this_game_object(self):
        self.should_be_rendered = True

    def remove_default_rect_image(self):
        self.image = pygame.Surface((0, 0))

    def get_index_in_scene_all_game_objects_list(self) -> int:
        for i in range(0, len(self.scene.game_object_list)):
            if self.scene.game_object_list[i] == self:
                return i
        return -1

    def get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list(self) -> int:
        for i in range(0, len(self.scene.camera._rendering_layers_list)):
            if self.scene.camera._rendering_layers_list[i] == self.rendering_layer:
                return i
        return -1

    def get_this_game_object_components_list_as_string(self):
        components_names = "None"
        if len(self.components_list) > 0:
            components_names = ""
            counter = 0
            max_comp_name_per_line = 3
            for component in self.components_list:
                counter += 1
                components_names += type(component).__name__ + ", "
                if counter == max_comp_name_per_line:
                    components_names += "\n"
                    counter = 0
            components_names = components_names[:-1]
            components_names = components_names[:-1]
        return components_names

    # it's meant to be overridden with a super().get_inspector_debugging_status() call in it
    def get_inspector_debugging_status(self) -> str:

        components_names = self.get_this_game_object_components_list_as_string()

        components_inspector_debugging_status = ""
        for component in self.components_list:
            components_inspector_debugging_status += component.get_inspector_debugging_status() + "\n"

        return f"GAME OBJECT INSPECTOR \n" \
               f"game object name: {self.name}\n" \
               f"class name: {type(self)} \n" \
               f"should be rendered: {self.should_be_rendered}\n" \
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"rendering layer index: {self.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
               f"components: [{components_names}]\n\n" \
               f"{components_inspector_debugging_status}"
