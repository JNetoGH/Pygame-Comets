import math
from typing import Union
import pygame

from engine_JNeto_Productions.components.circle_trigger_component import CircleTriggerComponent
from engine_JNeto_Productions.components.rect_collider_component import ColliderComponent
from engine_JNeto_Productions.components.rect_trigger_component import RectTriggerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class GizmosSystem:

    def __init__(self):

        # current scene
        self._current_scene = None

        # Descriptions
        path_to_font = 'engine_JNeto_Productions/_engine_resources/fonts/JetBrainsMono-Medium.ttf'
        self._FONT_SIZE = 15
        self._font = pygame.font.Font(path_to_font, self._FONT_SIZE)

        # Creating new surface every frame is too expensive, so, I try to cache all the gizmos surfaces
        self._cached_text_surfaces = {}

    def set_current_scene(self, scene):
        self._current_scene = scene

    def render_scene_game_objects_gizmos(self):
        if self._current_scene is None:
            return

        # game objects gizmos
        for gm_obj in self._current_scene.game_object_list:
            self.__render_gizmos_of_game_obj_image_rect(gm_obj, pygame.Color("red"))
            if gm_obj.has_collider:
                self.__render_gizmos_of_game_obj_colliders(gm_obj, pygame.Color("yellow"))
            if gm_obj.has_rect_trigger:
                self.__render_gizmos_of_game_obj_rect_triggers(gm_obj, pygame.Color("green"))
            if gm_obj.has_circle_trigger:
                self.__render_gizmos_of_game_obj_circle_triggers(gm_obj, pygame.Color("green"))
            if gm_obj.transform.is_center_point_appearing_on_screen_read_only:
                self._render_gizmos_of_game_obj_transform(gm_obj, pygame.Color("cyan"))

    def _get_cached_surface_or_cache_new_one(self, msg, color: pygame.Color) -> pygame.Surface:
        if msg not in self._cached_text_surfaces:
            self._cached_text_surfaces[msg] = self._font.render(msg, True, color).convert_alpha()
        return self._cached_text_surfaces[msg]

    def _render_text(self, text: str, position: pygame.Vector2, color: pygame.Color):
        text_surface = self._get_cached_surface_or_cache_new_one(text, color)
        GameScreen.GameScreenDummySurface.blit(text_surface, position)

    # ==================================================================================================================
    #                                                  TRANSFORM
    # ==================================================================================================================

    def _render_gizmos_of_game_obj_transform(self, gm_obj: GameObject, color: pygame.Color) -> None:

        object_screen_pos = gm_obj.transform.screen_position_read_only  # it's a copy

        # render the point
        pygame.draw.circle(GameScreen.GameScreenDummySurface, color, object_screen_pos, 5)

        # forward line render
        width = 1

        length = 40
        pos_initial: pygame.Vector2 = object_screen_pos
        pos_final: pygame.Vector2 = pos_initial + gm_obj.transform.forward_direction * length
        pygame.draw.line(GameScreen.GameScreenDummySurface, color, pos_initial, pos_final, width)

        length_linhas_desviadas = length/3*2
        desvio_degrees = 20
        # I need to add/sub more 180 because my default orientation for 0 is ↑ sited of 0º aiming ↓ by default
        rad_desvio1 = math.radians(gm_obj.transform.rotation_angle_read_only + desvio_degrees - 180)
        rad_desvio2 = math.radians(gm_obj.transform.rotation_angle_read_only - desvio_degrees - 180)
        # makes the direction: normalizing can't throw a division by 0 exception, cuz a (0,0) direction is impossible
        dir_desvio1 = pygame.Vector2(math.sin(rad_desvio1), math.cos(rad_desvio1)).normalize()
        dir_desvio2 = pygame.Vector2(math.sin(rad_desvio2), math.cos(rad_desvio2)).normalize()
        # os pontos gerados dos desvios
        ponto_desvio1 = pos_initial + dir_desvio1 * length_linhas_desviadas
        ponto_desvio2 = pos_initial + dir_desvio2 * length_linhas_desviadas
        # desenha com pygame
        pygame.draw.line(GameScreen.GameScreenDummySurface, color, pos_final, ponto_desvio2, width)
        pygame.draw.line(GameScreen.GameScreenDummySurface, color, pos_final, ponto_desvio1, width)

        if gm_obj.name == "player":
            print(gm_obj.transform.forward_direction)


        """
        # render description
        text = f"{gm_obj.name}'s TransformComponent"
        text_position = pygame.Vector2(object_screen_pos.x + 30, object_screen_pos.y - self._FONT_SIZE + 3)
        self._render_text(text, text_position, color)
        """

    # ==================================================================================================================
    #                                             IMAGE RECTANGLE
    # ==================================================================================================================

    def __render_gizmos_of_game_obj_image_rect(self, game_obj, color: pygame.Color) -> None:

        object_screen_pos = game_obj.transform.screen_position_read_only  # it's a copy

        # render the rect
        pygame.draw.rect(GameScreen.GameScreenDummySurface, color, game_obj.image_rect, 1)

        """
        # render description
        text = f"{game_obj.name}'s image_rect"
        text_position = pygame.Vector2(0, 0)
        text_position.x = object_screen_pos[0] - game_obj.image_rect.width // 2
        text_position.y = object_screen_pos[1] - game_obj.image_rect.height // 2 - self._FONT_SIZE * 2
        self._render_text(text, text_position, color)
        """

    # ==================================================================================================================
    #                                          RECTANGLE TRIGGERS/COLLIDERS
    # ==================================================================================================================

    def __render_gizmos_of_game_obj_colliders(self, game_obj, color: pygame.Color) -> None:
        # COLLIDERS GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, ColliderComponent):
                # render component
                self.__render_rect_of_rect_based_component(component, color)

    def __render_gizmos_of_game_obj_rect_triggers(self, game_obj, color: pygame.Color):
        # RECT TRIGGER GIZMOS
        for component in game_obj.components_list:
            if isinstance(component, RectTriggerComponent) and not isinstance(component, ColliderComponent):
                # render component
                self.__render_rect_of_rect_based_component(component, color)

    def __render_rect_of_rect_based_component(self, component: Union[ColliderComponent, RectTriggerComponent], color: pygame.Color):

        game_obj = component.game_object_owner_read_only  # it's a copy

        # THE REPRESENTATION OF THE COLLIDER/RECT TRIGGER AT SCREEN POSITION
        # the position of the collider/rect trigger is at world position,
        # so I have to treat its position for correct representation on screen
        representative_rect = component.inner_rect_read_only.copy()
        representative_rect.centerx = game_obj.transform.screen_position_read_only.x + component.offset_from_game_object_x
        representative_rect.centery = game_obj.transform.screen_position_read_only.y + component.offset_from_game_object_y

        # render the rect
        pygame.draw.rect(GameScreen.GameScreenDummySurface, color, representative_rect, 1)

        # renders the middle circle
        pygame.draw.circle(GameScreen.GameScreenDummySurface, color, representative_rect.center, 5)

        """
        # render description
        text = f"{game_obj.name}'s {component.__class__.__name__}\n"
        text_position = pygame.Vector2()
        text_position.x = representative_rect.centerx + 30
        if isinstance(component, RectTriggerComponent) and not isinstance(component, ColliderComponent):
            text_position.y = representative_rect.centery - self._FONT_SIZE * 2
        else:
            text_position.y = representative_rect.centery + self._FONT_SIZE // 2
        self._render_text(text, text_position, color)
        """

    # ==================================================================================================================
    #                                                   CIRCLE TRIGGERS
    # ==================================================================================================================

    def __render_gizmos_of_game_obj_circle_triggers(self, gm_obj, color):
        for component in gm_obj.components_list:
            if isinstance(component, CircleTriggerComponent):
                # THE REPRESENTATION OF THE CIRCLE TRIGGER AT SCREEN POSITION
                # the position of the trigger is at world position,
                # so I have to treat its position for correct representation on screen
                representative_circle_x = gm_obj.transform.screen_position_read_only.x + component.offset_from_game_object_x
                representative_circle_y = gm_obj.transform.screen_position_read_only.y + component.offset_from_game_object_y
                circle_center = pygame.Vector2(representative_circle_x, representative_circle_y)
                pygame.draw.circle(GameScreen.GameScreenDummySurface, color, circle_center, component.radius, 1)

                """
                # render description
                text = f"{gm_obj.name}'s {component.__class__.__name__}\n"
                text_position = pygame.Vector2()
                text_position.x = circle_center.x + 30
                text_position.y = circle_center.y - self._FONT_SIZE * 2
                self._render_text(text, text_position, color)
                """
