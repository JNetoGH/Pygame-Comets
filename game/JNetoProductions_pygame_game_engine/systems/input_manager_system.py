import pygame
import sys

class InputManager:

    Horizontal_Axis = 0
    Vertical_Axis = 0

    @staticmethod
    def update() -> None:
        InputManager._treat_exit()
        InputManager._treat_axis()

    @staticmethod
    def _treat_exit() -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

    @staticmethod
    def _treat_axis() -> None:
        keys = pygame.key.get_pressed()

        # HORIZONTAL RELEASE
        if keys[pygame.K_a]:
            InputManager.Horizontal_Axis = -1
        elif keys[pygame.K_d]:
            InputManager.Horizontal_Axis = 1

        # HORIZONTAL PRESS
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            InputManager.Horizontal_Axis = 0

        # VERTICAL PRESS
        if keys[pygame.K_w]:
            InputManager.Vertical_Axis = -1
        elif keys[pygame.K_s]:
            InputManager.Vertical_Axis = 1

        # VERTICAL RELEASE
        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            InputManager.Vertical_Axis = 0

    @staticmethod
    def is_key_pressed(key_pygame_code):
        keys = pygame.key.get_pressed()
        return keys[key_pygame_code]

    @staticmethod
    def get_inspector_debugging_status() -> str:
        return f"INPUT MANAGER SYSTEM\n" \
               f"horizontal: {InputManager.Horizontal_Axis}\n" \
               f"vertical:   {InputManager.Vertical_Axis}\n" \

