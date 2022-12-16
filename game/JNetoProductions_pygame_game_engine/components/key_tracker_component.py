from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager
from JNetoProductions_pygame_game_engine.components.component_base_class.component_base_class import Component


class KeyTrackerComponent(Component):

    def __init__(self, pygame_key_code, game_object_owner):
        super().__init__(game_object_owner)
        self.pygame_key_code = pygame_key_code
        self.has_key_been_fired_at_this_frame = False
        self.has_key_been_released_at_this_frame = False
        self.is_key_being_held_down = False
        self._has_key_been_already_fired_but_not_released = False
        self.total_times_fired: int = 0

    def component_update(self):

        self.has_key_been_fired_at_this_frame = False
        self.has_key_been_released_at_this_frame = False

        self.is_key_being_held_down = InputManager.is_key_pressed(self.pygame_key_code)

        if self.is_key_being_held_down and not self._has_key_been_already_fired_but_not_released and not self.has_key_been_fired_at_this_frame:
            self.has_key_been_fired_at_this_frame = True
            self.total_times_fired += 1
            self._has_key_been_already_fired_but_not_released = True

        if self._has_key_been_already_fired_but_not_released and not self.is_key_being_held_down:
            self._has_key_been_already_fired_but_not_released = False
            self.has_key_been_released_at_this_frame = True

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(KeyTrackerComponent)\n" \
               f"tracked key: {self.pygame_key_code}\n" \
               f"total times fired: {self.total_times_fired}\n" \
               f"this frame: (fired={self.has_key_been_fired_at_this_frame} | released={self.has_key_been_released_at_this_frame})\n" \
               f"is held down: {self.is_key_being_held_down}\n" \

