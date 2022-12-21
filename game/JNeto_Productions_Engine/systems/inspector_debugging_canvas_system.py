from typing import Union
import pygame

from JNeto_Productions_Engine.components.rect_collider_component import ColliderComponent
from JNeto_Productions_Engine.components.rect_trigger_component import TriggerComponent
from JNeto_Productions_Engine.systems.input_manager_system import InputManager
from JNeto_Productions_Engine.systems.scalable_game_screen_system import GameScreen
from JNeto_Productions_Engine.systems.game_time_system import GameTime
from JNeto_Productions_Engine.systems._gizmos_and_debugging_text_rendering_system import TextRenderOverlaySystem

from JNeto_Productions_Engine.scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, game_loop, scene: Scene, font_size=10):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.game_loop = game_loop
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('JNeto_Productions_Engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,

        # black transparent rect
        s = pygame.Surface(
            (GameScreen.DummyScreenWidth // 3, GameScreen.DummyScreenHeight - 20))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        GameScreen.GameScreenDummySurface.blit(s, (10, 10))  # (0,0) are the top-left coordinates

        # the msgs
        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n\n" \
               f"ENGINE INNER DETAILS\n" \
               f"fps: {self.game_loop.clock.get_fps():.1f}\n" \
               f"elapsed updates: {self.game_loop.elapsed_updates}\n" \
               f"delta-time: {str(GameTime.DeltaTime)}\n\n" \
               f"{GameScreen.get_inspector_debugging_status()}\n" + \
               f"{InputManager.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.camera.get_inspector_debugging_status()}"

        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth // 3,
                                          msgs, (30, 30), font, color=pygame.Color("white"))

    def render_game_object_inspector_debugging_status(self, index_of_game_obj, color: str):
        font = pygame.font.Font('JNeto_Productions_Engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,
        msgs = f"{self.current_scene.game_object_list[index_of_game_obj].get_inspector_debugging_status()}\n"
        # calls the method that displays text on the dummy screen
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth * 2,
                                          msgs, (GameScreen.DummyScreenWidth // 3 * 2, 20), font,
                                          color=pygame.Color(color))

    def render_scene_game_objects_gizmos(self):
        for gm_obj in self.current_scene.game_object_list:
            font_size = 15
            font = pygame.font.Font(
                'JNeto_Productions_Engine/_engine_resources/fonts/JetBrainsMono-Medium.ttf',
                font_size)  # create a text surface object

            # gizmos about the game obj
            if gm_obj.transform.is_center_point_appearing_on_screen_read_only:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_transform(gm_obj, "black", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_image_rect(gm_obj, "red", font, font_size)
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_debugging_stats(gm_obj, "black", font)

            if gm_obj.has_collider:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_colliders(gm_obj, "yellow", font, font_size)
            if gm_obj.has_rect_trigger:
                InspectorDebuggingCanvas._render_gizmos_of_game_obj_rect_triggers(gm_obj, "green", font, font_size)

    @staticmethod
    def _render_gizmos_of_game_obj_transform(gm_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = gm_obj.transform.screen_position_read_only

        description_spacing_x = 30
        description_spacing_y = 30

        # TRANSFORM GIZMOS
        # render the point
        pygame.draw.circle(GameScreen.GameScreenDummySurface, color, object_screen_pos, 5)
        # description
        text_transform = f"{gm_obj.name}'s Transform world_position\n({gm_obj.transform.world_position_read_only})\n" \
                         f"{gm_obj.name}'s Transform screen_position\n({gm_obj.transform.screen_position_read_only})"
        # render description
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth,
                                          text_transform,
                                          (object_screen_pos[0] + description_spacing_x,
                                           object_screen_pos[1] - font_size // 2 - description_spacing_y),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_image_rect(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only

        # IMAGE RECT GIZMOS
        # render the rect
        pygame.draw.rect(GameScreen.GameScreenDummySurface, color, game_obj.image_rect, 1)
        # description
        text_img_rect = "self.image.image_rect"
        # render render description
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth,
                                          text_img_rect,
                                          (object_screen_pos[0] - game_obj.image_rect.width // 2,
                                           object_screen_pos[1] - game_obj.image_rect.height // 2 - font_size - 5),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_gizmos_of_game_obj_debugging_stats(game_obj, color: str, font: pygame.font.Font) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only
        description_spacing_y = 30

        # THE DEBUGGING STATS IS ALSO GOING TO APPEAR AS GIZMOS
        components_names = game_obj.get_this_game_object_components_list_as_string()
        # description
        game_object_stats_text = \
            f"GAME OBJECT INSPECTOR \n" \
            f"\ngame object name: {game_obj.name}\n" \
            f"class name: {type(game_obj)} \n" \
            f"should be rendered: {game_obj.should_be_rendered}\n" \
            f"index in scene game objects list: {game_obj.get_index_in_scene_all_game_objects_list()}\n" \
            f"rendering layer index: {game_obj.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
            f"\ncomponents:\n[{components_names}]\n\n"
        # render description
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth,
                                          game_object_stats_text,
                                          (object_screen_pos[0] - game_obj.image_rect.width // 2,
                                           object_screen_pos[
                                               1] + game_obj.image_rect.height // 2 + description_spacing_y),
                                          font, color=pygame.Color(color))

    @staticmethod
    def _render_rect_of_rect_based_component(component: Union[ColliderComponent, TriggerComponent], color, font, font_size):

        game_obj = component.game_object_owner_read_only

        # THE REPRESENTATION OF THE COLLIDER/RECT TRIGGER AT SCREEN POSITION
        # the position of the collider/rect trigger is at world position,
        # so I have to treat its position for correct representation on screen
        representative_rect = component.inner_rect_read_only.copy()
        representative_rect.centerx = game_obj.transform.screen_position_read_only.x + component.offset_from_game_object_x
        representative_rect.centery = game_obj.transform.screen_position_read_only.y + component.offset_from_game_object_y

        # render the rect
        pygame.draw.rect(GameScreen.GameScreenDummySurface, color, representative_rect, 1)

        # description
        collider_text = f"{component.game_object_owner_read_only.name}'s {component.__class__.__name__}\n" \
                        f"offside.x: {component.offset_from_game_object_x} | offside.y: {component.offset_from_game_object_y}\n" \
                        f"width: {component.width} | height: {component.height}\n" \
                        f"world position ({component.world_position_read_only})"

        # render description
        TextRenderOverlaySystem.blit_text(GameScreen.GameScreenDummySurface, GameScreen.DummyScreenWidth,
                                          collider_text,
                                          (
                                              representative_rect.centerx - representative_rect.width // 2,
                                              representative_rect.centery - representative_rect.height // 2 - font_size * 4 - 20
                                          ),
                                          font, color=pygame.Color(color))

        # renders the middle circle
        pygame.draw.circle(GameScreen.GameScreenDummySurface, color, representative_rect.center, 5)

    @staticmethod
    def _render_gizmos_of_game_obj_colliders(game_obj, color: str, font: pygame.font.Font, font_size: int) -> None:
        # COLLIDERS GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, ColliderComponent):
                # render component
                InspectorDebuggingCanvas._render_rect_of_rect_based_component(component, color, font, font_size)

    @staticmethod
    def _render_gizmos_of_game_obj_rect_triggers(game_obj, color: str, font: pygame.font.Font, font_size: int):
        # RECT TRIGGER GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, TriggerComponent) and not isinstance(component, ColliderComponent):
                # render component
                InspectorDebuggingCanvas._render_rect_of_rect_based_component(component, color, font, font_size)
