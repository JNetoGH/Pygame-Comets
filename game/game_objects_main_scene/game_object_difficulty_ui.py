import pygame

from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_objects_main_scene.game_object_meteor_manager import MeteorManager


class Emoji(GameObject):

    AvailableEmojis = {
        "smile": "game_res/emojis/smile.png",
        "poker": "game_res/emojis/poker.png",
        "limao_azedo": "game_res/emojis/limao_azedo.png",
        "satan": "game_res/emojis/satan.png",
        "robot": "game_res/emojis/robot.png",
    }

    def __init__(self, scene):
        super().__init__("emoji", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))
        self.transform.move_world_position(pygame.Vector2(self.image.get_width() / 2-25, GameScreen.HalfDummyScreenHeight - 63))
        self.fix_game_object_on_screen(pygame.Vector2(self.image.get_width() / 2-27, GameScreen.HalfDummyScreenHeight - 63))
        self.single_sprite = SpriteComponent("game_res/emojis/smile.png", self)
        self.single_sprite.scale_sprite(0.4)


class DifficultyUi(GameObject):
    def __init__(self, scene, rendering_layer):
        super().__init__("difficulty_ui", scene, rendering_layer)

        # Sprite
        self.single_sprite = SpriteComponent("game_res/dif_ui.png", self)
        self.single_sprite.scale_sprite(1.5)
        self.fix_game_object_on_screen(pygame.Vector2(self.image.get_width()/2-3, GameScreen.HalfDummyScreenHeight))

        # Emoji
        self.emoji = Emoji(self.scene)

        self.has_difficulty_changed = False
        self.difficulty = 0


    def game_object_update(self) -> None:

        if MeteorManager.DifficultyInSeconds != self.difficulty:
            self.has_difficulty_changed = True
            self.difficulty = MeteorManager.DifficultyInSeconds
        else:
            self.has_difficulty_changed = False
        if not self.has_difficulty_changed:
            return

        #print(f"difficulty: {self.difficulty}seconds")

        if self.difficulty >= 0.65:
            self.check_if_is_already_using_a_emoji_case_not_change_it(Emoji.AvailableEmojis["smile"])
        elif 0.65 > self.difficulty >= 0.55:
            self.check_if_is_already_using_a_emoji_case_not_change_it(Emoji.AvailableEmojis["poker"])
        elif 0.55 > self.difficulty >= 0.45:
            self.check_if_is_already_using_a_emoji_case_not_change_it(Emoji.AvailableEmojis["limao_azedo"])
        elif 0.45 > self.difficulty >= 0.35:
            self.check_if_is_already_using_a_emoji_case_not_change_it(Emoji.AvailableEmojis["satan"])
        elif 0.35 > self.difficulty:
            self.check_if_is_already_using_a_emoji_case_not_change_it(Emoji.AvailableEmojis["robot"])

    def check_if_is_already_using_a_emoji_case_not_change_it(self, path):
        if self.emoji.single_sprite.get_img_path() != path:
            self.emoji.single_sprite.change_image(path)
            self.emoji.single_sprite.scale_sprite(0.4)