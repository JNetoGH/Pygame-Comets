import pygame

from JNetoProductions_pygame_game_engine.components.rect_trigger_component import RectTriggerComponent
from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.systems._text_rendering_system import TextRenderOverlaySystem
from JNetoProductions_pygame_game_engine.components.collider_component import ColliderComponent
from JNetoProductions_pygame_game_engine.scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, game_loop, scene: Scene, font_size=10):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.game_loop = game_loop
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,

        # black transparent rect
        s = pygame.Surface((ScalableGameScreen.DummyScreenWidth // 3, ScalableGameScreen.DummyScreenHeight - 20))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        ScalableGameScreen.GameScreenDummySurface.blit(s, (10, 10))  # (0,0) are the top-left coordinates

        # the msgs
        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n\n" \
               f"ENGINE INNER DETAILS\n" \
               f"fps: {self.game_loop.clock.get_fps():.1f}\n" \
               f"elapsed updates: {self.game_loop.elapsed_updates}\n" \
               f"delta-time: {str(GameTime.DeltaTime)}\n\n" \
               f"{ScalableGameScreen.get_inspector_debugging_status()}\n" + \
               f"{InputManager.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.main_camera.get_inspector_debugging_status()}"

        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth // 3,
                                          msgs, (30, 30), font, color=pygame.Color("white"))

    def render_game_object_inspector_debugging_status(self, index_of_game_obj, color: str):
        font = pygame.font.Font('JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf', self.font_size)  # create a text surface object,
        msgs = f"{self.current_scene.all_game_obj[index_of_game_obj].get_inspector_debugging_status()}\n"
        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth * 2,
                                          msgs, (ScalableGameScreen.DummyScreenWidth//3*2, 20), font, color=pygame.Color(color))

    def render_scene_game_objects_gizmos(self):
        for gm_obj in self.current_scene.all_game_obj:
            font_size = 15
            font = pygame.font.Font('JNetoProductions_pygame_game_engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf', font_size)  # create a text surface object
            """
            # os gismoz foram desabilidatos por agr
            if gm_obj.transform.is_center_point_appearing_on_screen_read_only:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_transform(gm_obj, "black", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_image_rect(gm_obj, "red", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_debugging_stats(gm_obj, "black", font)
            """
            if gm_obj.has_collider:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_colliders(gm_obj, "yellow", font, font_size)
            if gm_obj.has_rect_trigger:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_rect_triggers(gm_obj,"green", font, font_size)

    @staticmethod
    def _render_gizmos_of_game_obj_transform(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        description_spacing_x = 30
        description_spacing_y = 30

        # TRANSFORM GIZMOS
        # render the point
        pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, color, object_screen_pos, 5)
        # description
        text_transform = f"{game_obj.name}'s TransformComponent.world_position\n(x:{game_obj.transform.world_position.x} | y:{game_obj.transform.world_position.y})\n" \
                         f"{game_obj.name}'s TransformComponent.screen_position\n(x:{game_obj.transform.screen_position_read_only.x} | y:{game_obj.transform.screen_position_read_only.y})"
        # render description
        TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                          text_transform,
                                          (object_screen_pos[0] + description_spacing_x,
                              object_screen_pos[1] - font_size // 2 - description_spacing_y),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_image_rect(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        # IMAGE RECT GIZMOS
        # render the rect
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, color, game_obj.image_rect, 1)
        # description
        text_img_rect = "self.image.image_rect"
        # render render description
        TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                          text_img_rect,
                                          (object_screen_pos[0] - game_obj.image_rect.width // 2,
                              object_screen_pos[1] - game_obj.image_rect.height // 2 - font_size - 5),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_debugging_stats(game_obj, color: str, font: pygame.font.Font) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        description_spacing_x = 30
        description_spacing_y = 30

        # THE DEBUGGING STATS IS ALSO GOING TO APPEAR AS GIZMOS
        components_names = game_obj.get_this_game_object_components_list_as_string()
        # description
        game_object_stats_text = \
            f"GAME OBJECT INSPECTOR \n" \
            f"\ngame_loop object name: {game_obj.name}\n" \
            f"class name: {type(game_obj)} \n" \
            f"should be rendered: {game_obj.should__be_rendered}\n" \
            f"index in scene game_loop objects list: {game_obj.get_index_in_scene_all_game_objects_list()}\n" \
            f"rendering layer index: {game_obj.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
            f"\ncomponents:\n[{components_names}]\n\n"
        # render description
        TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                          game_object_stats_text,
                                          (object_screen_pos[0] - game_obj.image_rect.width // 2,
                              object_screen_pos[1] + game_obj.image_rect.height // 2 + description_spacing_y),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_colliders(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        # COLLIDERS GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, ColliderComponent):
                # render

                # THE REPRESENTATION OF THE COLIDER AT SCREEN POSITION
                # the position of the collider is at world position,
                # so I have to treat its position for correct representation on screen
                representative_screen_collider_rect = component.collider_rect.copy()
                representative_screen_collider_rect.centerx = object_screen_pos.x + component.offset_from_game_object_x
                representative_screen_collider_rect.centery = object_screen_pos.y + component.offset_from_game_object_y

                # render the rect
                pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, color, representative_screen_collider_rect, 1)

                # description
                collider_text = f"{component.game_object_owner_read_only.name}'s collider\n" \
                                f"offside.x: {component.offset_from_game_object_x} | offside.y: {component.offset_from_game_object_y}\n" \
                                f"width: {component.width} | height: {component.height}\n" \
                                f"world position ({component.world_position_get_only})"

                # render description
                TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                                  collider_text,
                                                  (representative_screen_collider_rect.centerx - representative_screen_collider_rect.width // 2,
                                                   representative_screen_collider_rect.centery - representative_screen_collider_rect.height // 2 - font_size * 4 - 20),
                                                  font, color=pygame.Color(color))

                # renders the middle circle
                pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, color, representative_screen_collider_rect.center, 5)

    @staticmethod
    def _render_gizmos_of_game_obj_rect_triggers(game_obj, color: str, font: pygame.font.Font, font_size: int):

        object_screen_pos = game_obj.transform.screen_position_read_only

        # COLLIDERS GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, RectTriggerComponent):
                # render

                # THE REPRESENTATION OF THE COLIDER AT SCREEN POSITION
                # the position of the collider is at world position,
                # so I have to treat its position for correct representation on screen
                representative_screen_rect_trigger = component.trigger_inner_rectangle.copy()
                representative_screen_rect_trigger.centerx = object_screen_pos.x + component.offset_from_game_object_x
                representative_screen_rect_trigger.centery = object_screen_pos.y + component.offset_from_game_object_y

                # render the rect
                pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, color, representative_screen_rect_trigger, 1)

                # description
                collider_text = f"{component.game_object_owner_read_only.name}'s rect-trigger\n" \
                                f"offside.x: {component.offset_from_game_object_x} | offside.y: {component.offset_from_game_object_y}\n" \
                                f"width: {component.width} | height: {component.height}\n" \
                                f"world position ({component.world_position_get_only})"

                # render description
                TextRenderOverlaySystem.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth,
                                                  collider_text,
                                                  (
                                                  representative_screen_rect_trigger.centerx - representative_screen_rect_trigger.width // 2,
                                                  representative_screen_rect_trigger.centery - representative_screen_rect_trigger.height // 2 - font_size * 4 - 20),
                                                  font, color=pygame.Color(color))

                # renders the middle circle
                pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, color, representative_screen_rect_trigger.center, 5)