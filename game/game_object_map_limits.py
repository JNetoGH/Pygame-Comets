from JNeto_Productions_Engine.animation_clip import AnimationClip
from JNeto_Productions_Engine.components.animation_controller_component import AnimationControllerComponent
from JNeto_Productions_Engine.components.rect_collider_component import ColliderComponent
from JNeto_Productions_Engine.components.single_sprite_component import SingleSpriteComponent

from JNeto_Productions_Engine.game_object_base_class import GameObject


class MapLimits(GameObject):
    def __init__(self, scene):
        super().__init__("map_limits", scene, scene.camera.get_rendering_layer_by_name("map_limits_layer"))
        self.single_sprite = SingleSpriteComponent("res/limits.png", self)

        self.animation_clip = AnimationClip("limits", 6, "res/map_limits")
        self.animation_controller = AnimationControllerComponent([self.animation_clip], self)

        self.collider_top = ColliderComponent(0, -540, 3000, 300, self)
        self.collider_bottom = ColliderComponent(0, 547, 3000, 300, self)
        self.collider_left = ColliderComponent(-620, 0, 300, 3000, self)
        self.collider_right = ColliderComponent(620, 0, 300, 3000, self)

    def game_object_update(self) -> None:
        pass
