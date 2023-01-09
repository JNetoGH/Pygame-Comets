import pygame.time
from engine_JNeto_Productions.components.component_base_class._component_base_class import Component


class TimerComponent(Component):

    # can execute a function oce the timer is over
    def __init__(self, duration_in_ms, game_object_owner, func=None):
        super().__init__(game_object_owner)
        self.__duration_in_ms = duration_in_ms
        self.__start_time = 0
        self.__curren_moment = 0
        self.__is_active = False
        self.__has_finished_counting = False
        self.func = func

    @property
    def has_finished_counting_read_only(self):
        return not self.__has_finished_counting

    @property
    def is_timer_active_read_only(self):
        return self.__is_active

    @property
    def elapsed_time_read_only(self):
        return self.__curren_moment - self.__start_time

    @property
    def duration_in_ms_read_only(self):
        return self.__duration_in_ms

    def set_duration_in_ms(self, new_duration_in_ms):
        self.__duration_in_ms = new_duration_in_ms

    def activate(self):
        self.__is_active = True
        self.__has_finished_counting = False
        self.__start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.__is_active = False
        self.__has_finished_counting = True
        self.__start_time = 0

    def component_update(self):
        self.__curren_moment = pygame.time.get_ticks()
        if self.elapsed_time_read_only > self.__duration_in_ms and self.__is_active:
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
               f"total elapsed time since scene started: {self.__curren_moment}ms\n" \
               f"duration: {self.__duration_in_ms}ms\n" \
               f"timer start time: {self.__start_time}ms\n" \
               f"timer elapsed time: {self.elapsed_time_read_only}ms\n"
