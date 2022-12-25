import pygame

from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class ShootBar(GameObject):
    def __init__(self, x, y, width, height, color, scene):
        super().__init__("shoot_bar", scene, scene.camera.get_rendering_layer_by_name("bars_layer")) #"cockpit_layer" "bars_layer"
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.fix_game_object_on_screen(pygame.Vector2(x, y))


class RightShootUi(GameObject):

    TotWaitTime = 0
    ElapsedTime = 0

    def __init__(self, scene):
        super().__init__("right_shoot_ui", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))
        self.single_sprite = SpriteComponent("game_res/main_game_shoot_ui.png", self)
        self.single_sprite.scale_sprite(1.5)
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.DummyScreenWidth-self.image.get_width()/2+4, GameScreen.HalfDummyScreenHeight))

        self.shoot_bar = ShootBar(
            GameScreen.DummyScreenWidth-self.image.get_width()/2-20+23, GameScreen.HalfDummyScreenHeight+50,
            self.image.get_width()-16, 90, pygame.Color(210, 210, 210), self.scene)

        self.black_bar_x = GameScreen.DummyScreenWidth-self.image.get_width()/2-20+23
        self.black_bar_y_full_hidden = GameScreen.HalfDummyScreenHeight-40
        self.black_bar_y = self.black_bar_y_full_hidden

        self.black_bar = ShootBar(self.black_bar_x, self.black_bar_y, self.image.get_width()-16, 90, pygame.Color(48,48,48), self.scene)

        self.black_bar_y_full_cover = self.black_bar_y_full_hidden + self.black_bar.image.get_height()

        # 90
        self.PATH_LENGTH = self.black_bar_y_full_cover - self.black_bar_y_full_hidden

        # tot_wait_time => 100%
        # ElapsedTime => x

        # x tot_wait_time = 100 * TimeToNextBullet
        # x = 100 * TimeToNextBullet / tot_wait_time

        # 90 em y => 100%
        # x em y => tantos%

        # incremeto
        # 90 * tantosporcento = x * 100
        # x = 90 * tantosporcento / 100
        self.black_bar.fix_game_object_on_screen(pygame.Vector2(self.black_bar_x, self.black_bar_y_full_hidden))


    def game_object_update(self) -> None:
        if RightShootUi.TotWaitTime != 0 and RightShootUi.ElapsedTime != 0:
            percentage = 100 * RightShootUi.ElapsedTime / RightShootUi.TotWaitTime
            #print(f"tot time to wait: {LeftShootUi.TotWaitTime}")
            #print(f"elapsed time: {LeftShootUi.ElapsedTime}")
            #print(f"percentage: {percentage}%")
            increment = (self.PATH_LENGTH * percentage / 100)
            if increment < 0:
                increment = increment * -1
            new_pos_y = self.black_bar_y_full_cover - increment
            self.black_bar.fix_game_object_on_screen(pygame.Vector2(self.black_bar_x, new_pos_y ))
