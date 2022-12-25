import pygame

from engine_JNeto_Productions.components.sprite_component import SpriteComponent
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.input_manager_system import InputManager
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class Cockpit(GameObject):
    def __init__(self, scene, rendering_layer):
        super().__init__("cockpit", scene, rendering_layer)

        # Sprite
        self.single_sprite = SpriteComponent("game_res/ui.png", self)
        self.single_sprite.scale_sprite(1.5)
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.DummyScreenHeight - 15 * 1.5))

        # Texts
        self.angle_text_render = TextRenderComponent("000.0º", 15, pygame.Color(255, 255, 255), -185, 1, self)
        self.speed_text_render = TextRenderComponent("000u/s", 15, pygame.Color(255, 255, 255), 15, 1, self)
        self.speed_status_text_render = TextRenderComponent("stop", 15, pygame.Color(255, 255, 255), 232, 0, self)

        # Player Itself
        self.player = self.scene.get_game_object_by_name("player")

    def game_object_update(self) -> None:

        # angle
        self.angle_text_render.set_text(f"{self.player.transform.rotation_angle_read_only:.1f}º")

        # speed text itself
        self.speed_text_render.set_text(f"{self.player.current_speed:.0f}u/s")

        # speed status
        if InputManager.Vertical_Axis == -1:

            if self.player.current_speed >= self.player.BASE_MAX_MOVE_SPEED:
                self.speed_status_text_render.set_text("MAX SPEED")
                self.speed_status_text_render.set_color(pygame.Color(255, 255, 150))
                self.speed_status_text_render.set_font_size(15)
                self.speed_status_text_render.offset_from_game_object_y = 1
                return

            self.speed_status_text_render.set_text("accelerating")
            self.speed_status_text_render.set_color(pygame.Color(120, 225, 120))
            self.speed_status_text_render.set_font_size(12)
            self.speed_status_text_render.offset_from_game_object_y = 0

        elif self.player.current_speed > 0:
            self.speed_status_text_render.set_text("decelerating")
            self.speed_status_text_render.set_color(pygame.Color(255, 120, 120))
            self.speed_status_text_render.set_font_size(12)
            self.speed_status_text_render.offset_from_game_object_y = 0

        elif self.player.current_speed == 0:
            self.speed_status_text_render.set_text("stop")
            self.speed_status_text_render.set_color(pygame.Color(255, 255, 255))
            self.speed_status_text_render.set_font_size(15)
            self.speed_status_text_render.offset_from_game_object_y = 0