import enum
import pygame


class OPERATION(enum.Enum):
    NULL = -1
    DISPLAY_NATIVE = 0
    UP_SCALE = 1
    DOWN_SCALE = 2


class ScalableGameScreen:

    # CANVAS SURFACES
    TargetResolutionForUpScaling = [1920, 1080]
    # DUMMY SCREEN: the screen where thing are drew into
    GameScreenDummySurface: pygame.Surface = None
    # REAL CANVAS: the actual displayed canvas, receives a up/down-scaled dummy canvas to display
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
        ScalableGameScreen.GameScreenDummySurface = pygame.Surface(dummy_screen_resolution)
        ScalableGameScreen.DummyScreenWidth = dummy_screen_resolution[0]
        ScalableGameScreen.DummyScreenHeight = dummy_screen_resolution[1]
        ScalableGameScreen.HalfDummyScreenWidth = ScalableGameScreen.DummyScreenWidth // 2
        ScalableGameScreen.HalfDummyScreenHeight = ScalableGameScreen.DummyScreenHeight // 2

        # Updates the real game_loop screen surface
        ScalableGameScreen.GameScreenRealSurface = pygame.display.set_mode(real_screen_resolution)
        ScalableGameScreen.RealScreenWidth = real_screen_resolution[0]
        ScalableGameScreen.RealScreenHeight = real_screen_resolution[1]
        ScalableGameScreen.HalfRealScreenWidth = ScalableGameScreen.RealScreenWidth // 2
        ScalableGameScreen.HalfRealScreenHeight = ScalableGameScreen.RealScreenHeight // 2

        # Updates the target resolution
        ScalableGameScreen.TargetResolutionForUpScaling = up_scaling_target_resolution

        # must be the last one called because it takes in consideration the set resolutions
        ScalableGameScreen._generate_current_operation()

    @staticmethod
    def render_final_scaled_result():
        # only up/down scales if it needs to, because it cost a lot in performance
        if ScalableGameScreen._CurrentOperation == OPERATION.DISPLAY_NATIVE:
            native_surface = ScalableGameScreen.GameScreenDummySurface
            native_surface_rect = ScalableGameScreen._get_centralized_surface_in_real_screen_rect(native_surface)
            ScalableGameScreen.GameScreenRealSurface.blit(native_surface, native_surface_rect)
        else:
            scaled_surface = ScalableGameScreen._get_up_scaled_surface_to_target_resolution(ScalableGameScreen.GameScreenDummySurface)
            scaled_surface_centralized_rect = ScalableGameScreen._get_centralized_surface_in_real_screen_rect(scaled_surface)
            ScalableGameScreen.GameScreenRealSurface.blit(scaled_surface, scaled_surface_centralized_rect)
        pygame.display.flip()

    @staticmethod
    def _get_centralized_surface_in_real_screen_rect(surface):
        centralized_frame_rect = surface.get_rect()
        centralized_frame_rect.x = (ScalableGameScreen.GameScreenRealSurface.get_width() - ScalableGameScreen.TargetResolutionForUpScaling[0]) // 2
        centralized_frame_rect.y = (ScalableGameScreen.GameScreenRealSurface.get_height() - ScalableGameScreen.TargetResolutionForUpScaling[1]) // 2
        return centralized_frame_rect

    @staticmethod
    def _get_up_scaled_surface_to_target_resolution(surface):
        # the dummy frame after scaling
        scaled_frame = pygame.transform.scale(surface, ScalableGameScreen.TargetResolutionForUpScaling)
        return scaled_frame

    @staticmethod
    def _generate_current_operation() -> None:
        if ScalableGameScreen.DummyScreenWidth == ScalableGameScreen.TargetResolutionForUpScaling[0] and ScalableGameScreen.DummyScreenHeight == ScalableGameScreen.TargetResolutionForUpScaling[1]:
            ScalableGameScreen._CurrentOperation = OPERATION.DISPLAY_NATIVE
        elif ScalableGameScreen.DummyScreenWidth < ScalableGameScreen.TargetResolutionForUpScaling[0] and ScalableGameScreen.DummyScreenHeight < ScalableGameScreen.TargetResolutionForUpScaling[1]:
            ScalableGameScreen._CurrentOperation = OPERATION.UP_SCALE
        else:
            ScalableGameScreen._CurrentOperation = OPERATION.DOWN_SCALE

    @staticmethod
    def get_inspector_debugging_status() -> str:
        return f"SCREEN SCALE SYSTEM\n" \
               f"res (dummy surface): {ScalableGameScreen.DummyScreenWidth} x {ScalableGameScreen.DummyScreenHeight}\n" \
               f"res (real surface):  {ScalableGameScreen.RealScreenWidth} x {ScalableGameScreen.RealScreenHeight}\n" \
               f"res (target):        {ScalableGameScreen.TargetResolutionForUpScaling[0]} x {ScalableGameScreen.TargetResolutionForUpScaling[1]}\n" \
               f"current operation: {ScalableGameScreen._CurrentOperation}\n"


