from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class Map(GameObject):

    def __init__(self, scene):
        super().__init__("map", scene, scene.get_rendering_layer_by_name("map_layer"))
        self.single_sprite = SingleSpriteComponent("res/bg4.jpg", self)
        self.single_sprite.scale_itself(1)

    def game_object_update(self) -> None:
        pass