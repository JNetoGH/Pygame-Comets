import pygame
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen


class Camera:

    def __init__(self, *rendering_layers):

        self._rendering_layers_list = rendering_layers
        self._followed_game_object = None

        # - The movement off-set base on the followed game object
        # - Basically is how much the camera has to move every non-fixed on-screen GameObject
        #   if the focused GameObject world_position_x is 3, the offset will be 3 in x and everything else will be
        #   moved (-3) to compensate.
        #  - The off_set.x = (world_pos.x - Half_screen__width), and off_set.y = (world_pos.y - Half_screen_height)
        #    half because the camera focus in the middle of the screen
        self.followed_object_offset = pygame.Vector2()

    def get_rendering_layer_by_name(self, name: str):
        for r_layer in self._rendering_layers_list:
            if r_layer.name == name:
                return r_layer

    def get_followed_game_object(self) -> GameObject:
        return self._followed_game_object

    def follow_game_object(self, game_object: GameObject) -> None:
        for rendering_layer in self._rendering_layers_list:
            for gm in rendering_layer.game_objects_to_render_read_only:
                if gm == game_object:
                    self._followed_game_object = game_object
                    print(f"__followed_game_object set to {self._followed_game_object.name}")
                    return
        print("game_object not found in any rendering layer, impossible to follow, __followed_game_object set to None")
        self._followed_game_object = None

    def stop_following_current_set_game_object(self):
        self._followed_game_object = None

    @property
    def world_position_read_only(self) -> pygame.Vector2:
        world_position_in_x = self.followed_object_offset.x + GameScreen.HalfDummyScreenWidth
        world_position_in_y = self.followed_object_offset.y + GameScreen.HalfDummyScreenHeight
        return pygame.Vector2(world_position_in_x, world_position_in_y)

    @property
    def screen_position_read_only(self) -> pygame.Vector2:
        return pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight)

    # - Kinda fakes a game object position to artificially set the camera there
    # - I don't even have to say that it doesn't work if the camera is already following a game object
    def focus_camera_at_world_position(self, world_position: pygame.Vector2):
        self.followed_object_offset.x = world_position.x - GameScreen.HalfDummyScreenWidth
        self.followed_object_offset.y = world_position.y - GameScreen.HalfDummyScreenHeight
        # to invert: position.x = offset.x + ScalableGameScreen.HalfDummyScreenWidth

    # the real deal, what really renders the whole game
    def render_layers(self):
        # - The camera stops following a GameObject its position on map will be the last position captured of the
        #   no more followed GameObject
        # - By default it's set to render at position 0,0, so if a camera has never followed a game object,
        #   it will  ber rendering the position 0,0
        if self._followed_game_object is not None:

            # essential for moving, it´´s the difference of the followed game obj position in relation to the screen,
            # in other words, how much should every other game object should move on screen (not on world)
            self.followed_object_offset.x = self._followed_game_object.transform.world_position_read_only.x - GameScreen.HalfDummyScreenWidth
            self.followed_object_offset.y = self._followed_game_object.transform.world_position_read_only.y - GameScreen.HalfDummyScreenHeight

        for r_layer in self._rendering_layers_list:
            for game_obj in r_layer.game_objects_to_render_read_only:

                # the final result of the render takes in consideration the game object world position
                # that's why I pre-update the image_rect
                game_obj.image_rect = game_obj.image.get_rect(center=game_obj.transform.world_position_read_only)

                # the followed game object must be treated in a different way
                if game_obj != self._followed_game_object:

                    # fixed on screen game objects are simply rendered at their fixed position on screen
                    # by setting their image_ret to that fixed position
                    if game_obj.is_fixed_on_screen:
                        game_obj.image_rect.center = game_obj._fixed_position_on_screen

                    # non fixed on screen objects have to be moved according to the offset generated by the followed object
                    # so their image_rect is updated subtracting the offset.
                    else:
                        game_obj.image_rect.center -= self.followed_object_offset

                # updates the sprite image_rect position the followed game object image rect ,
                # it's different from the orders because it's always n the center
                else:
                    screen_center = (GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight)
                    self._followed_game_object.image_rect = self._followed_game_object.image.get_rect(center=screen_center)

                # render the game object on screen according to its screen position (not world position) a.k.a. image_rect position
                if game_obj.should_be_rendered:
                    GameScreen.GameScreenDummySurface.blit(game_obj.image, game_obj.image_rect)

                    # blits all the text render components of the game object, but updates the position before for extra accuracy
                    for component in game_obj.components_list:
                        if isinstance(component, TextRenderComponent) and component.should_be_rendered:
                            component._update_position()
                            GameScreen.GameScreenDummySurface.blit(component.text_surface, component.position_on_screen)

                # - Should be the last thing executing at the rendering system
                # - Just updates what is show at the transform for extra accuracy
                # - Nice to mention, the transform is just a way the get the screen position easily, it doesn't change it
                # - Also updates if it is appearing on screen
                game_obj.transform.component_update()

    def get_inspector_debugging_status(self) -> str:
        text = "CAMERA SYSTEM\n"
        if self._followed_game_object is not None:
            text += f"following: {self._followed_game_object.name}\n"

        else:
            text += f"following GameObject: None\n"

        text += f"following GameObject off-set: {self.followed_object_offset}\n"
        # position.x = offset.x + ScalableGameScreen.HalfDummyScreenWidth
        text += f"world position: {self.world_position_read_only}"

        return text
