import pygame
import sys


class InputManager:

    Horizontal_Axis = 0
    Vertical_Axis = 0

    @staticmethod
    def update() -> None:
        InputManager.__treat_exit()
        InputManager.__treat_axis()

    @staticmethod
    def __treat_exit() -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

    @staticmethod
    def __treat_axis() -> None:

        keys = pygame.key.get_pressed()

        # ----------------------------------------

        # HORIZONTAL PRESS
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            InputManager.Horizontal_Axis = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            InputManager.Horizontal_Axis = 1

        # HORIZONTAL RELEASE
        if not (keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            InputManager.Horizontal_Axis = 0

        # ----------------------------------------

        # VERTICAL PRESS
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            InputManager.Vertical_Axis = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            InputManager.Vertical_Axis = 1

        # VERTICAL RELEASE
        if not (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_DOWN]):
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
