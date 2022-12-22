import pygame

from button_game_object import Button
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_object_score_scene.black_filte_game_object import BlackFilter


class ScoreRegistrationFloatingMenu(GameObject):

    TotalPoints = 9999999

    def __init__(self, scene, rendering_layer):
        super().__init__("score_registration_menu", scene, rendering_layer)
        self.remove_default_rect_image()
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight))

        self.black_filter = BlackFilter(self.scene, self.scene.camera.get_rendering_layer_by_name("score_layer3"))

        text0 = f"CONGRATS! YOU'VE MADE {ScoreRegistrationFloatingMenu.TotalPoints} POINTS!"
        self.text0_render = TextRenderComponent(text0, 30, pygame.Color("white"), 0, -140, self)
        text1 = "YOU HAVE MANAGED TO GET INTO THE RANKING"
        self.text1_render = TextRenderComponent(text1, 20, pygame.Color("white"), 0, -100, self)
        text2 = "insert 3 characters to represent your score"
        self.text2_render = TextRenderComponent(text2, 20, pygame.Color("white"), 0, -75, self)

        self.save_button = Button("game_res/score_menu/save.png", "game_res/score_menu/save_active.png",
                                   pygame.Vector2(GameScreen.HalfDummyScreenWidth,
                                                  GameScreen.HalfRealScreenHeight +150), 2,
                                   self.func_save_button, self.scene, self.scene.camera.get_rendering_layer_by_name("score_layer4"))

        # tem q ficar desativado por pradao
        self.deactivate()

    def func_save_button(self):
        # aqui
        self.deactivate()
        print("saved")

    def game_object_update(self) -> None:
        # syncs this render because, it can be set more than once
        text0 = f"CONGRATS! YOU'VE MADE {ScoreRegistrationFloatingMenu.TotalPoints} POINTS!"
        self.text0_render.set_text(text0)

    def activate(self):
        self.black_filter.start_rendering_this_game_object()
        self.text0_render.start_rendering_text()
        self.text1_render.start_rendering_text()
        self.text2_render.start_rendering_text()
        self.save_button.activate()

    def deactivate(self):
        self.black_filter.stop_rendering_this_game_object()
        self.text0_render.stop_rendering_text()
        self.text1_render.stop_rendering_text()
        self.text2_render.stop_rendering_text()
        self.save_button.deactivte()


