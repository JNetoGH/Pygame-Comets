import pygame
import gc

from engine_JNeto_Productions.game_object_base_class import GameObject
from game_objects_main_scene.game_object_bullet import Bullet
from game_objects_main_scene.game_object_meteor import Meteor
from game_objects_main_scene.game_object_player import Player
from game_objects_main_scene.game_object_score import ScoreUi


class MainSceneReseter(GameObject):

    def __init__(self, scene):
        super().__init__("main_phase_reseter", scene, scene.camera.get_rendering_layer_by_name("map_layer"))

        self.remove_default_rect_image()
        self.player: Player = self.scene.get_game_object_by_name("player")
        self.score: ScoreUi = self.scene.get_game_object_by_name("score")

    def game_object_update(self) -> None:
        pass

    def reset_phase(self):
        # player
        self.player.transform.move_world_position(pygame.Vector2(0, 0))
        self.player.angle = 0
        self.player._rotate_player()
        self.player.current_speed = 0
        self.score.reset_score()

        # bullets
        Bullet.In_Scene_Bullets.clear()

        # remove meteors in scene
        for gm in self.scene.game_object_list:
            if isinstance(gm, Meteor):
                self.scene.remove_game_object(gm)
        gc.collect()
