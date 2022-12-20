from JNetoProductions_pygame_game_engine.camera import Camera
from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.game_loop import GameLoop
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.rendering_layer import RenderingLayer
from JNetoProductions_pygame_game_engine.scene import Scene
from game_object_cockpit import Cockpit
from game_object_meteor import Meteor
from game_object_map import Map
from game_object_player import Player



class MapLimits(GameObject):
    def __init__(self, scene):
        super().__init__("map_limits", scene, scene.get_rendering_layer_by_name("map_limits_layer"))
        self.single_sprite = SingleSpriteComponent("res/limits.png", self)


game_loop = GameLoop()
map_rendering_layer = RenderingLayer("map_layer")
player_rendering_layer = RenderingLayer("player_layer")
map_limits_layer = RenderingLayer("map_limits_layer")
over_player_layer = RenderingLayer("over_player_layer")
cockpit_layer = RenderingLayer("cockpit_layer")

main_camera = Camera(map_rendering_layer, player_rendering_layer, over_player_layer, map_limits_layer, cockpit_layer)
main_scene = Scene(main_camera)

map = Map(main_scene)
map_limits = MapLimits(main_scene)
player = Player(main_scene)
cockpit = Cockpit(main_scene, cockpit_layer)
meteor = Meteor(main_scene)

# GAME LOOP
game_loop.set_current_scene(main_scene)
game_loop.run_game_loop()

