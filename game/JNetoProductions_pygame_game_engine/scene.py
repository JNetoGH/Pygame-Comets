import pygame

from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
import gc

class Scene:

    def __init__(self, camera):

        # It holds all game_loop objects of the scene When a game_loop Obj is instantiated,
        # it's automatically stored here using the scene passed as parameter in  its constructor
        self.all_game_obj = []
        # main camera will render the rendering layers
        self.main_camera = camera
        # they are here just to be accessed by the GameObjects
        self.all_rendering_layers = self.main_camera.rendering_layers_list

        # called once if i want to start stuff in here
        self.scene_start()

    def get_game_object_by_name(self, name: str):
        for game_obj in self.all_game_obj:
            if game_obj.name == name:
                return game_obj

    def get_rendering_layer_by_name(self, name: str):
        for r_layer in self.all_rendering_layers:
            if r_layer.name == name:
                return r_layer

    # in order to be garbage collected needs to be removed from both,
    # the scene game obj list and the rendering layer list, believe me, I tested it
    def remove_game_object(self, required_game_object):
        for gm in self.all_game_obj:
            if gm == required_game_object:
                self.all_game_obj.remove(gm)
                gm.rendering_layer.remove_game_object(gm)

    def scene_start(self):
        pass

    def scene_update(self):
        # first updates the components then the game_loop object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        # updates just for easy access to the layers
        self.all_rendering_layers = self.main_camera.rendering_layers_list
        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill(pygame.Color(64,64,64))
        # renders all rendering layers
        self.main_camera.render_layers()

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inspector
    def get_inspector_debugging_status(self) -> str:

        game_obj_names = []
        for gm_obj in self.all_game_obj:
            game_obj_names.append(gm_obj.name)

        tot_in_layers = 0
        info_about_each_layer = ""

        for render_layer in self.all_rendering_layers:
            tot_in_this_layer = len(render_layer._game_objects_to_render)
            tot_in_layers += tot_in_this_layer
            info_about_each_layer += f"{render_layer.name} tot objects: {tot_in_this_layer}\n"

        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.main_camera.rendering_layers_list)}\n" \
               f"total game objects in scene: {len(self.all_game_obj)}\n" \
               f"total game objects in rendering layers: {tot_in_layers}\n" \
               f"{info_about_each_layer}" #\
               #f"list of game objects: {game_obj_names}\n"

