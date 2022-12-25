import pygame

from engine_JNeto_Productions.scene_camera import SceneCamera
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class Scene:

    def __init__(self, camera):

        # It holds all game objects of the scene When a game obj is instantiated,
        # it's automatically stored here using the scene passed as parameter in  its constructor
        self.game_object_list = []
        # main camera will render the rendering layers
        self.camera: SceneCamera = camera
        # called once everytime the scene is set if I want to start stuff and game objects in here
        self.scene_start()

    def get_game_object_by_name(self, name: str):
        for game_obj in self.game_object_list:
            if game_obj.name == name:
                return game_obj

    # in order to be garbage collected needs to be removed from both,
    # the scene game obj list and the rendering layer list, believe me, I tested it
    def remove_game_object(self, required_game_object):
        for gm in self.game_object_list:
            if gm == required_game_object:
                self.game_object_list.remove(gm)
                gm.rendering_layer.remove_game_object(gm)

    def scene_start(self):
        for gm in self.game_object_list:
            gm.game_object_scene_set_start()

    def scene_update(self):
        # first updates the components then the game object itself
        for gm in self.game_object_list:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        # clears the screen for rendering
        GameScreen.GameScreenDummySurface.fill(pygame.Color(64, 64, 64))
        # renders all rendering layers
        self.camera.render_layers()

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inspector
    def get_inspector_debugging_status(self) -> str:

        game_obj_names = []
        for gm_obj in self.game_object_list:
            game_obj_names.append(gm_obj.name)

        # rendering layers debugging
        tot_in_layers = 0
        info_about_each_layer = ""
        for render_layer in self.camera._rendering_layers_list:
            tot_in_this_layer = len(render_layer.game_objects_to_render_read_only)
            tot_in_layers += tot_in_this_layer
            info_about_each_layer += f"{render_layer.name} tot objects: {tot_in_this_layer}\n"

        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.camera._rendering_layers_list)}\n" \
               f"total game objects in scene: {len(self.game_object_list)}\n" \
               f"total game objects in rendering layers: {tot_in_layers}\n" \
               f"{info_about_each_layer}" \
               f"list of game objects: {game_obj_names}\n"
