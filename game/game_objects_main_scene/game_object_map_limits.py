from engine_JNeto_Productions.compenentes_dependencies.animation_clip import AnimationClip
from engine_JNeto_Productions.components.animation_controller_component import AnimationControllerComponent
from engine_JNeto_Productions.components.rect_collider_component import ColliderComponent
from engine_JNeto_Productions.components.sprite_component import SpriteComponent

from engine_JNeto_Productions.game_object_base_class import GameObject


class MapLimits(GameObject):
    def __init__(self, scene):
        super().__init__("map_limits", scene, scene.camera.get_rendering_layer_by_name("map_limits_layer"))
        self.single_sprite = SpriteComponent("game_res/limits.png", self)

        self.animation_clip = AnimationClip("limits", 10, "game_res/map_limits")
        self.animation_controller = AnimationControllerComponent([self.animation_clip], self)

        self.collider_top = ColliderComponent(0, -540, 3000, 300, self)
        self.collider_bottom = ColliderComponent(0, 547, 3000, 300, self)
        self.collider_left = ColliderComponent(-620, 0, 300, 3000, self)
        self.collider_right = ColliderComponent(620, 0, 300, 3000, self)

    def game_object_update(self) -> None:
        pass
