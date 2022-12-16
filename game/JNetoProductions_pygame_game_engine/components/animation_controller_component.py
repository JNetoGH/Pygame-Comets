from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.animation_clip import AnimationClip
from JNetoProductions_pygame_game_engine.components.component_base_class.component_base_class import Component
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


# sets the current animation in a animation list and the current frame of the animation according to a speed
class AnimationControllerComponent(Component):

    def __init__(self, animation_clips, game_object_owner: GameObject):
        super().__init__(game_object_owner)

        self.animation_clips_list: list[AnimationClip] = animation_clips
        self.current_animation_clip: AnimationClip = self.animation_clips_list[0]
        self.current_animation_clip_name = self.current_animation_clip.name

        self.current_frame_index = 0  # the current img of the animation clip
        self.animation_speed = 0
        self._stop_animation_clip = False

    def add_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.append(animation)

    def remove_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.remove(animation)

    # doesnt change if it's the same clip as the one set to be animated
    def set_current_animation(self, animation_clip_name) -> None:
        for animation_clip in self.animation_clips_list:
            if animation_clip.name == animation_clip_name and self.current_animation_clip != animation_clip:
                self.current_animation_clip = animation_clip
                self.current_animation_clip_name = animation_clip_name

    def stop_animation(self, true_false) -> None:
        self._stop_animation_clip = true_false

    def component_update(self) -> None:
        if not self._stop_animation_clip and self.animation_clips_list != []:
            # jump from frame to frame
            self.current_frame_index += self.animation_speed * GameTime.DeltaTime
            self.animation_speed = self.current_animation_clip.animation_speed
            # sets back to the first frame if it's bigger than the size of the animation

            if self.current_frame_index >= len(self.current_animation_clip.images):
                self.current_frame_index = 0
            self.game_object_owner.image = self.current_animation_clip.images[int(self.current_frame_index)]

    def scale_all_animations_of_this_controller(self, scale) -> None:
        for animation in self.animation_clips_list:
            animation.scale_all_frames_of_this_animation(scale)

    def get_inspector_debugging_status(self) -> str:
        in_memory_animation_clips_names = ""
        for clip in self.animation_clips_list:
            in_memory_animation_clips_names += clip.name + ", "
        in_memory_animation_clips_names = in_memory_animation_clips_names[:-1]
        in_memory_animation_clips_names = in_memory_animation_clips_names[:-1]
        return f"COMPONENT(AnimationControllerComponent)\n" \
               f"current animation clip: {self.current_animation_clip.name}\n" \
               f"current clip truncate index: {int(self.current_frame_index)}\n" \
               f"animation speed: {self.animation_speed}\n" \
               f"animation clips in memory: [{in_memory_animation_clips_names}]\n" \
               f"list len: {len(self.current_animation_clip.images)}\n"

