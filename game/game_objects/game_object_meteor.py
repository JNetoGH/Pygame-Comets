import enum
import pygame


from engine_JNeto_Productions.components.circle_trigger_component import CircleTriggerComponent
from engine_JNeto_Productions.components.single_sprite_component import SingleSpriteComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.game_time_system import GameTime
from game_objects.game_object_player import Player


class Meteor(GameObject):

    class MeteorRank(enum.Enum):
        Small = 1
        Mid = 2
        Big = 4

    def __init__(self, scene, rank: MeteorRank, initial_position: pygame.Vector2, direction: pygame.Vector2):
        super().__init__("meteor", scene, scene.camera.get_rendering_layer_by_name("over_player_layer"))

        # scales the meteor to its ranks value
        self.sigle_sprite = SingleSpriteComponent("game_res/meteor.png", self)
        self.sigle_sprite.scale_itself(rank.value)

        # circle trigger
        self.circle_trigger = CircleTriggerComponent(0,0, self.image.get_width()//2, self)

        # lifetime
        self.life_time_is_seg = 20
        self.life_time_timer = TimerComponent(self.life_time_is_seg*1000, self, self._set_to_garbage_collection)
        self.life_time_timer.activate()

        # moves to initial position
        self.transform.move_world_position(initial_position)

        # move and direction
        self.move_speed = 100
        self.direction = direction

        self.player: Player = self.scene.get_game_object_by_name("player")

    def game_object_update(self) -> None:
        self.move_to_direction()
        if self.circle_trigger.is_there_a_point_inside(self.player.transform.world_position_read_only):
            print("player dentro de mim")

    def move_to_direction(self):
        pos_increment = pygame.Vector2(self.direction * self.move_speed * GameTime.DeltaTime)
        self.transform.translate_world_position(pos_increment)

    def _set_to_garbage_collection(self):
        self.scene.remove_game_object(self)