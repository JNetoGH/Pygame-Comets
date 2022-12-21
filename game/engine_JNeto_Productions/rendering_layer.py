from engine_JNeto_Productions.game_object_base_class import GameObject


class RenderingLayer:

    def __init__(self, name):
        self.name = name
        self._game_objects_to_render: list[GameObject] = []

    @property
    def game_objects_to_render_read_only(self):
        return self._game_objects_to_render.copy()

    def add_game_object(self, game_object: GameObject):
        self._game_objects_to_render.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        self._game_objects_to_render.remove(game_object)
