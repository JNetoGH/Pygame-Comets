import enum
import pygame


class OPERATION(enum.Enum):
    NULL = -1
    DISPLAY_NATIVE = 0
    UP_SCALE = 1
    DOWN_SCALE = 2


class GameScreen:

    # CANVAS SURFACES
    TargetResolutionForUpScaling = [1920, 1080]
    # DUMMY SCREEN: the screen where thing are drew into
    GameScreenDummySurface: pygame.Surface = None
    # REAL CANVAS: the actual displayed canvas, receives an up/down-scaled dummy canvas to display
    # thing should not be drawn directly at the GameScreenRealSurface
    GameScreenRealSurface: pygame.Surface = None

    """
    HOW THE SCREEN SCALING SYSTEM WORKS
    
                                              DummySurface is                 RealSurface blits
                       things are drawn       up/down-scaled to the           the Dummy surface into itself
    DummySurface       to the DummySurface    TargetResolutionForUpScaling   
    |------------|     |------------|         |-------------------|            RealSurface:
    |            | =>  |   X    o   |    =>   |                   |      =>  |-------------------| 
    |------------|     |------------|         |                   |          |    DummySurface   |  =>  pygame shows
                                              |-------------------|          |                   |      the RealSurface
                                                                             |-------------------|                 
    """

    DummyScreenWidth = 1280
    DummyScreenHeight = 720
    HalfDummyScreenWidth = DummyScreenWidth // 2
    HalfDummyScreenHeight = DummyScreenHeight // 2

    RealScreenWidth = 1920
    RealScreenHeight = 1080
    HalfRealScreenWidth = RealScreenWidth // 2
    HalfRealScreenHeight = RealScreenHeight // 2

    _CurrentOperation = OPERATION.NULL

    @staticmethod
    def init_screens(dummy_screen_resolution: list[int], real_screen_resolution: list[int], up_scaling_target_resolution):

        # Updates the dummy game_loop screen surface
        GameScreen.GameScreenDummySurface = pygame.Surface(dummy_screen_resolution)
        GameScreen.DummyScreenWidth = dummy_screen_resolution[0]
        GameScreen.DummyScreenHeight = dummy_screen_resolution[1]
        GameScreen.HalfDummyScreenWidth = GameScreen.DummyScreenWidth // 2
        GameScreen.HalfDummyScreenHeight = GameScreen.DummyScreenHeight // 2

        # Updates the real game_loop screen surface
        GameScreen.GameScreenRealSurface = pygame.display.set_mode(real_screen_resolution)
        GameScreen.RealScreenWidth = real_screen_resolution[0]
        GameScreen.RealScreenHeight = real_screen_resolution[1]
        GameScreen.HalfRealScreenWidth = GameScreen.RealScreenWidth // 2
        GameScreen.HalfRealScreenHeight = GameScreen.RealScreenHeight // 2

        # Updates the target resolution
        GameScreen.TargetResolutionForUpScaling = up_scaling_target_resolution

        # must be the last one called because it takes in consideration the set resolutions
        GameScreen.__generate_current_operation()

    @staticmethod
    def render_final_scaled_result():
        # only up/down scales if it needs to, because it cost a lot in performance
        if GameScreen._CurrentOperation == OPERATION.DISPLAY_NATIVE:
            native_surface = GameScreen.GameScreenDummySurface
            native_surface_rect = GameScreen.__get_centralized_surface_in_real_screen_rect(native_surface)
            GameScreen.GameScreenRealSurface.blit(native_surface, native_surface_rect)
        else:
            scaled_surface = GameScreen.__get_scaled_surface_to_target_resolution(GameScreen.GameScreenDummySurface)
            scaled_surface_centralized_rect = GameScreen.__get_centralized_surface_in_real_screen_rect(scaled_surface)
            GameScreen.GameScreenRealSurface.blit(scaled_surface, scaled_surface_centralized_rect)
        pygame.display.flip()

    @staticmethod
    def __get_centralized_surface_in_real_screen_rect(surface):
        centralized_frame_rect = surface.get_rect()
        centralized_frame_rect.x = (GameScreen.GameScreenRealSurface.get_width() - GameScreen.TargetResolutionForUpScaling[0]) // 2
        centralized_frame_rect.y = (GameScreen.GameScreenRealSurface.get_height() - GameScreen.TargetResolutionForUpScaling[1]) // 2
        return centralized_frame_rect

    @staticmethod
    def __get_scaled_surface_to_target_resolution(surface):
        # the dummy frame after scaling
        scaled_frame = pygame.transform.scale(surface, GameScreen.TargetResolutionForUpScaling)
        return scaled_frame

    @staticmethod
    def __generate_current_operation() -> None:
        if GameScreen.DummyScreenWidth == GameScreen.TargetResolutionForUpScaling[0] and GameScreen.DummyScreenHeight == GameScreen.TargetResolutionForUpScaling[1]:
            GameScreen._CurrentOperation = OPERATION.DISPLAY_NATIVE
        elif GameScreen.DummyScreenWidth < GameScreen.TargetResolutionForUpScaling[0] and GameScreen.DummyScreenHeight < GameScreen.TargetResolutionForUpScaling[1]:
            GameScreen._CurrentOperation = OPERATION.UP_SCALE
        else:
            GameScreen._CurrentOperation = OPERATION.DOWN_SCALE

    @staticmethod
    def get_inspector_debugging_status() -> str:
        return f"SCREEN SCALE SYSTEM\n" \
               f"res (dummy surface): {GameScreen.DummyScreenWidth} x {GameScreen.DummyScreenHeight}\n" \
               f"res (real surface):  {GameScreen.RealScreenWidth} x {GameScreen.RealScreenHeight}\n" \
               f"res (target):        {GameScreen.TargetResolutionForUpScaling[0]} x {GameScreen.TargetResolutionForUpScaling[1]}\n" \
               f"current operation: {GameScreen._CurrentOperation}\n"
