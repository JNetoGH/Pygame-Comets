from JNeto_Productions_Engine.components.rect_trigger_component import TriggerComponent


class ColliderComponent(TriggerComponent):

    def __init__(self, offset_from_game_object_x, offset_from_game_object_y, width, height, game_object_owner):
        super().__init__(offset_from_game_object_x, offset_from_game_object_y, width, height, game_object_owner)

        self.game_object_owner.has_collider = True

    def get_inspector_debugging_status(self) -> str:
        return "Component(ColliderComponent)\n"
