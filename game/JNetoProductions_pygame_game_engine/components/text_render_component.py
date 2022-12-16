import pygame
from JNetoProductions_pygame_game_engine.components.component_base_class.component_base_class import Component


# its rendered straight by the camera, there is a spacial part inside the camera for thi component
class TextRenderComponent(Component):
    def __init__(self, text: str, font_size, color: pygame.Color, offset_from_game_object_x, offset_from_game_object_y, game_object_owner):
        super().__init__(game_object_owner)

        self._text = text
        self._color: pygame.Color = color

        self._font = pygame.font.Font(
            'JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
            font_size)

        # create a text surface object, on which text is drawn on it by the camera.
        self.text_surface = self._font.render(self._text, True, color)

        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y

        # the position on screen where the camera should render the text
        # is the same of the game object owner screen position
        self.position_on_screen = pygame.Vector2(0, 0)
        self.update_position()

        self.should_be_rendered = True

    def change_font_size(self, font_size):
        self._font = pygame.font.Font(
            'JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf', font_size)
        # updates the text surface object, on which text is drawn on it by the camera.
        self.text_surface = self._font.render(self._text, True, self._color)

    def change_color(self, color: pygame.Color):
        self._color = color
        self.text_surface = self._font.render(self._text, True, self._color)

    def change_text(self, text: str):
        self._text = text
        self.text_surface = self._font.render(self._text, True, self._color)

    def stop_rendering_text(self):
        self.should_be_rendered = False

    def start_rendering_text(self):
        self.should_be_rendered = True

    def change_off_set_from_game_object(self, offset_from_game_object_x, offset_from_game_object_y):
        self.offset_from_game_object_x = offset_from_game_object_x
        self.offset_from_game_object_y = offset_from_game_object_y

    def update_position(self):
        # UPDATES THE TEXT POSITION ON SCREEN
        self.position_on_screen = pygame.Vector2(
            self.game_object_owner.transform.screen_position_read_only.x,
            self.game_object_owner.transform.screen_position_read_only.y)

        """
        centralizes the text at the desired position, because by default it's rendered like this:
            point .
                  |-------------|
                  |    Text     |
                  |-------------|
        """
        self.position_on_screen.x -= self.text_surface.get_width() / 2
        self.position_on_screen.y -= self.text_surface.get_height() / 2

        # ADDS THE OFF-SET FROM THE game_object_owner
        self.position_on_screen.x += self.offset_from_game_object_x
        self.position_on_screen.y += self.offset_from_game_object_y

    def component_update(self):
        self.update_position()

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(Text Render)\n" \
               f"text: {self._text}\n" \
               f"screen position: {self.position_on_screen}"