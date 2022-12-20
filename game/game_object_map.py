from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class Map(GameObject):

    def __init__(self, scene):
        super().__init__("map", scene, scene.get_rendering_layer_by_name("map_layer"))
        self.single_sprite = SingleSpriteComponent("res/bg4.jpg", self)
        self.single_sprite.scale_itself(1)

        self.collider_top = ColliderComponent(0, -800, 3000, 300, self)
        self.collider_bottom = ColliderComponent(0, 800, 3000, 300, self)
        self.collider_left = ColliderComponent(-1500, 0, 300, 3000, self)
        self.collider_right = ColliderComponent(1500, 0, 300, 3000, self)


    def game_object_update(self) -> None:
        pass
