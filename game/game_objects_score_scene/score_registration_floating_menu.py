import pygame

from engine_JNeto_Productions.prefabs.game_object_button import Button

from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.file_manager_system import FileManager
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_objects_score_scene.black_filter_game_object import BlackFilter
from engine_JNeto_Productions.prefabs.game_object_text_input_box import TextInputBox


class ScoreRegistrationFloatingMenu(GameObject):

    TotalPoints = 9999999
    Show: bool = False

    def __init__(self, scene, rendering_layer):
        super().__init__("score_registration_menu", scene, rendering_layer)

        self.cant_do_his_sound = pygame.mixer.Sound("game_res/audio/annauncer/Cant do this 1.wav")

        self.remove_default_rect_image()
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight))

        self.black_filter = BlackFilter(self.scene, self.scene.camera.get_rendering_layer_by_name("score_layer3"))

        text0 = f"CONGRATS! YOU'VE MADE {ScoreRegistrationFloatingMenu.TotalPoints} POINTS!"
        self.text0_render = TextRenderComponent(text0, 30, pygame.Color("white"), 0, -140, self)
        text1 = "YOU HAVE MANAGED TO GET INTO THE RANKING"
        self.text1_render = TextRenderComponent(text1, 20, pygame.Color("white"), 0, -100, self)
        text2 = "insert 3 characters to represent your score"
        self.text2_render = TextRenderComponent(text2, 20, pygame.Color("white"), 0, -75, self)
        text3 = "status"
        self.text3_render = TextRenderComponent(text3, 15, pygame.Color("white"), 0, 10, self)

        self.save_button = Button("game_res/score_menu/save.png", "game_res/score_menu/save_active.png",
                                   pygame.Vector2(GameScreen.HalfDummyScreenWidth,
                                                  GameScreen.HalfRealScreenHeight +150), 2,
                                   self.func_save_button, self.scene, self.scene.camera.get_rendering_layer_by_name("score_layer4"))

        self.text_input_box = TextInputBox(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight+50, 100,
                                           self.scene, self.scene.camera.get_rendering_layer_by_name("score_layer4"))

        # tem q ficar desativado por padrao
        self.deactivate()

    # press the button
    def func_save_button(self):
        # validation
        is_valid = False
        name = ""
        value = self.text_input_box.text
        if len(value) != 3:
            self.text3_render.set_text("amount of characters invalid!")
            self.text3_render.set_color(pygame.Color("red"))
        else:
            is_valid = True
            name = value
        if not is_valid:
            self.cant_do_his_sound.play()
            return

        # when is valid
        self.text3_render.set_text("status")
        self.text3_render.set_color(pygame.Color("white"))

        # registration
        print(f"{name} registered with {ScoreRegistrationFloatingMenu.TotalPoints} points\n")
        FileManager.write_new_row_in_csv_file("game_data/score_sheet.csv", [name, ScoreRegistrationFloatingMenu.TotalPoints])
        FileManager.sort_csv_file_by_column_values("game_data/score_sheet.csv", 1)
        self.deactivate()

    def game_object_update(self) -> None:
        # syncs this render because, it can be set more than once
        text0 = f"CONGRATS! YOU'VE MADE {ScoreRegistrationFloatingMenu.TotalPoints} POINTS!"
        self.text0_render.set_text(text0)

        if ScoreRegistrationFloatingMenu.Show:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        ScoreRegistrationFloatingMenu.Show = True
        self.black_filter.start_rendering_this_game_object()
        self.text0_render.start_rendering_text()
        self.text1_render.start_rendering_text()
        self.text2_render.start_rendering_text()
        self.text3_render.start_rendering_text()
        self.save_button.activate()
        self.text_input_box.activate()

    def deactivate(self):
        ScoreRegistrationFloatingMenu.Show = False
        self.black_filter.stop_rendering_this_game_object()
        self.text0_render.stop_rendering_text()
        self.text1_render.stop_rendering_text()
        self.text2_render.stop_rendering_text()
        self.text3_render.stop_rendering_text()
        self.save_button.deactivate()
        self.text_input_box.deactivate()

