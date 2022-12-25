import pygame

from engine_JNeto_Productions.components.key_tracker_component import KeyTrackerComponent
from engine_JNeto_Productions.components.rect_trigger_component import RectTriggerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class TextInputBox(GameObject):
    def __init__(self, x, y, width, scene, rendering_layer):
        super().__init__("text_box_input", scene, rendering_layer)

        self.remove_default_rect_image()

        path_to_font = 'engine_JNeto_Productions/_engine_resources/fonts/JetBrainsMono-Medium.ttf'
        self.__FONT_SIZE = 15
        self.__font = pygame.font.Font(path_to_font, self.__FONT_SIZE)

        self.transform.move_world_position(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight))
        self.fix_game_object_on_screen(pygame.Vector2(x, y))

        self.color = (255, 255, 255)
        self.backcolor = None
        self.width = width
        self.__is_active = True
        self.text = ""
        self.render_text()
        self.rect_trigger = RectTriggerComponent(0, 0, self.width, 40, self)

        self.keys = [
            ["a", KeyTrackerComponent(pygame.K_a, self)], ["b", KeyTrackerComponent(pygame.K_b, self)],
            ["c", KeyTrackerComponent(pygame.K_c, self)], ["d", KeyTrackerComponent(pygame.K_d, self)],
            ["e", KeyTrackerComponent(pygame.K_e, self)], ["f", KeyTrackerComponent(pygame.K_f, self)],
            ["g", KeyTrackerComponent(pygame.K_g, self)], ["h", KeyTrackerComponent(pygame.K_h, self)],
            ["i", KeyTrackerComponent(pygame.K_i, self)], ["j", KeyTrackerComponent(pygame.K_j, self)],
            ["k", KeyTrackerComponent(pygame.K_k, self)], ["l", KeyTrackerComponent(pygame.K_l, self)],
            ["m", KeyTrackerComponent(pygame.K_m, self)], ["n", KeyTrackerComponent(pygame.K_n, self)],
            ["o", KeyTrackerComponent(pygame.K_o, self)], ["p", KeyTrackerComponent(pygame.K_p, self)],
            ["q", KeyTrackerComponent(pygame.K_q, self)], ["r", KeyTrackerComponent(pygame.K_r, self)],
            ["s", KeyTrackerComponent(pygame.K_s, self)], ["t", KeyTrackerComponent(pygame.K_t, self)],
            ["u", KeyTrackerComponent(pygame.K_u, self)], ["v", KeyTrackerComponent(pygame.K_v, self)],
            ["x", KeyTrackerComponent(pygame.K_x, self)], ["y", KeyTrackerComponent(pygame.K_y, self)],
            ["z", KeyTrackerComponent(pygame.K_z, self)], ["backspace", KeyTrackerComponent(pygame.K_BACKSPACE, self)]
        ]

    def game_object_update(self):
        if not self.__is_active:
            return
        for i in range(len(self.keys)):
            if self.keys[i][1].has_key_been_fired_at_this_frame_read_only:
                if self.keys[i][0] == "backspace":
                    self.text = self.text[:-1]
                else:
                    self.text += self.keys[i][0]
                self.render_text()

    def render_text(self):
        t_surf = self.__font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+20), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 10))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)

    def deactivate(self):
        self.__is_active = False
        self.stop_rendering_this_game_object()

    def activate(self):
        self.__is_active = True
        self.start_rendering_this_game_object()
