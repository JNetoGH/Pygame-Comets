import pygame

from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.file_manager_system import FileManager
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class TextHolder(GameObject):
    def __init__(self, scene, rendering_layer):
        super().__init__("text_holder", scene, rendering_layer)

        self.path_to_file = "game_data/score_sheet.csv"
        FileManager.sort_csv_file_by_column_values(self.path_to_file, 1)

        self.image = pygame.Surface((GameScreen.DummyScreenWidth/5*3, GameScreen.DummyScreenHeight/5*4))
        self.image.fill(pygame.Color(50, 50, 50))
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight+100))


        self.scores = FileManager.read_from_csv_file(self.path_to_file)
        self.total_scores_for_exhibition = 10 if len(self.scores) >= 10 else len(self.scores)
        self.font_size = 22
        self.color = pygame.Color(255, 255, 255)
        self.initial_pos_y = -135
        self.spacing_y = 32
        self.spacing_x = 80

        title_font = 60
        self.title = TextRenderComponent("RANKING", title_font, self.color, 0, -GameScreen.HalfDummyScreenHeight-15, self)

        legenda_font_size = 30
        self.legenda1 = TextRenderComponent("NAME", legenda_font_size, self.color, -self.spacing_x, self.initial_pos_y - self.spacing_y - 10, self)
        self.legenda1 = TextRenderComponent("SCORE", legenda_font_size, self.color, self.spacing_x, self.initial_pos_y - self.spacing_y - 10, self)

        self.name_and_score_text_renderers = []
        self.scores = FileManager.read_from_csv_file(self.path_to_file)
        self.total_scores_for_exhibition = 10 if len(self.scores) >= 10 else len(self.scores)
        for i in range(0, self.total_scores_for_exhibition):
            name = TextRenderComponent(self.scores[i][0], self.font_size, self.color, -self.spacing_x, self.initial_pos_y + self.spacing_y * i, self)
            score = TextRenderComponent(self.scores[i][1], self.font_size, self.color, self.spacing_x, self.initial_pos_y + self.spacing_y * i, self)
            self.name_and_score_text_renderers.append([name, score])

    def game_object_update(self) -> None:
        self._sync_text()


    def _sync_text(self):

        self.scores = FileManager.read_from_csv_file(self.path_to_file)
        self.total_scores_for_exhibition = 10 if len(self.scores) >= 10 else len(self.scores)

        for i in range(0, self.total_scores_for_exhibition):
            if i >= len(self.name_and_score_text_renderers):
                name = TextRenderComponent(self.scores[i][0], self.font_size, self.color, -self.spacing_x, self.initial_pos_y + self.spacing_y * i, self)
                score = TextRenderComponent(self.scores[i][1], self.font_size, self.color, self.spacing_x, self.initial_pos_y + self.spacing_y * i, self)
                self.name_and_score_text_renderers.append([name, score])
            else:
                self.name_and_score_text_renderers[i][0].set_text(f"{self.scores[i][0]}")
                self.name_and_score_text_renderers[i][1].set_text(f"{self.scores[i][1]}")

