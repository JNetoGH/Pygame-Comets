from engine_JNeto_Productions.systems.input_manager_system import InputManager
from engine_JNeto_Productions.components.component_base_class.component_base_class import Component


class KeyTrackerComponent(Component):

    def __init__(self, pygame_key_code, game_object_owner):
        super().__init__(game_object_owner)

        self.pygame_key_code = pygame_key_code
        self._total_times_fired: int = 0
        self._has_key_been_fired_at_this_frame = False
        self._has_key_been_released_at_this_frame = False
        self._is_key_being_held_down = False
        self._has_key_been_already_fired_but_not_released = False

    @property
    def has_key_been_released_at_this_frame_read_only(self):
        return self._has_key_been_released_at_this_frame

    @property
    def has_key_been_fired_at_this_frame_read_only(self):
        return self._has_key_been_fired_at_this_frame

    @property
    def is_key_being_held_down_read_only(self):
        return self._is_key_being_held_down

    @property
    def total_times_fired_read_only(self):
        return self._total_times_fired

    def rest_total_times_fired(self):
        self._total_times_fired = 0

    def component_update(self):

        # TRACKED KEY HELD DOWN
        self._is_key_being_held_down = InputManager.is_key_pressed(self.pygame_key_code)

        # TRACKED KEY FIRED AND RELEASED
        self._has_key_been_fired_at_this_frame = False
        self._has_key_been_released_at_this_frame = False
        if self._is_key_being_held_down and not self._has_key_been_already_fired_but_not_released and not self._has_key_been_fired_at_this_frame:
            self._has_key_been_fired_at_this_frame = True
            self._total_times_fired += 1
            self._has_key_been_already_fired_but_not_released = True
        if self._has_key_been_already_fired_but_not_released and not self._is_key_being_held_down:
            self._has_key_been_already_fired_but_not_released = False
            self._has_key_been_released_at_this_frame = True

    def get_inspector_debugging_status(self) -> str:
        return f"COMPONENT(KeyTrackerComponent)\n" \
               f"tracked key: {self.pygame_key_code}\n" \
               f"total times fired: {self._total_times_fired}\n" \
               f"this frame: (fired={self._has_key_been_fired_at_this_frame} | released={self._has_key_been_released_at_this_frame})\n" \
               f"is held down: {self._is_key_being_held_down}\n" \
