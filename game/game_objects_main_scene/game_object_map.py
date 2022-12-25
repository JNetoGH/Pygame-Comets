from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.game_object_base_class import GameObject


class Map(GameObject):

    def __init__(self, scene):
        super().__init__("map", scene, scene.camera.get_rendering_layer_by_name("map_layer"))
        self.single_sprite = SpriteComponent("game_res/bg4.jpg", self)
        self.single_sprite.scale_sprite(1)

    def game_object_update(self) -> None:
        pass

