import pygame
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class BlackFilter(GameObject):
    def __init__(self, scene, rendering_layer):
        super().__init__("black_filter", scene, rendering_layer)
        self.image = pygame.Surface((GameScreen.DummyScreenWidth, GameScreen.DummyScreenHeight))
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight))
        self.image.fill(color="black")
        self.image.set_alpha(180)
