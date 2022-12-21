import pygame.time
from engine_JNeto_Productions.components.component_base_class.component_base_class import Component


class TimerComponent(Component):

    # can execute a function oce the timer is over
    def __init__(self, duration_in_ms, game_object_owner, func = None):
        super().__init__(game_object_owner)
        self.duration_in_ms = duration_in_ms
        self._start_time = 0
        self.tot_time_elapsed_since_game_started = 0
        self._is_active = False
        self._has_finished_counting = False
        self.func = func

    @property
    def has_finished_counting_read_only(self):
        return not self._has_finished_counting

    @property
    def is_timer_active_read_only(self):
        return self._is_active

    @property
    def elapsed_time_read_only(self):
        if self._start_time != 0:
            return self.tot_time_elapsed_since_game_started - self._start_time
        return 0

    def activate(self):
        self._is_active = True
        self._has_finished_counting = False
        self._start_time = pygame.time.get_ticks()

    def deactivate(self):
        self._is_active = False
        self._has_finished_counting = True
        self._start_time = 0

    def component_update(self):
        self.tot_time_elapsed_since_game_started = pygame.time.get_ticks()
        if self.tot_time_elapsed_since_game_started - self._start_time > self.duration_in_ms and self._is_active:
            self.deactivate()
            # if function is not none
            if self.func:
                self.func()

    def get_inspector_debugging_status(self) -> str:

        is_carrying_a_function = self.func is not None
        text = f"is carrying a function: {is_carrying_a_function}"
        if is_carrying_a_function:
            text += f"function carried: {self.func.__name__}\n"

        return f"COMPONENT(TimerComponent)\n" \
               f"{text}" \
               f"total elapsed time since game started: {self.tot_time_elapsed_since_game_started}ms\n" \
               f"duration: {self.duration_in_ms}ms\n" \
               f"timer start time: {self._start_time}ms\n" \
               f"timer elapsed time: {self.elapsed_time_read_only}ms\n"
