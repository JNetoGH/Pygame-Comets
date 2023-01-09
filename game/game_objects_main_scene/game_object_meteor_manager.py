import random
import pygame
from engine_JNeto_Productions.components.rect_trigger_component import RectTriggerComponent
from engine_JNeto_Productions.components.text_render_component import TextRenderComponent
from engine_JNeto_Productions.components.timer_component import TimerComponent
from engine_JNeto_Productions.game_object_base_class import GameObject
from engine_JNeto_Productions.systems.scalable_game_screen_system import GameScreen
from game_objects_main_scene.game_object_meteor import Meteor
from game_objects_main_scene.game_object_score import ScoreUi


class CountDownUi(GameObject):
    def __init__(self, scene):
        super().__init__("count_down_ui", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))
        self.remove_default_rect_image()

        self.transform.move_world_position(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight-130))
        self.fix_game_object_on_screen(pygame.Vector2(GameScreen.HalfDummyScreenWidth, GameScreen.HalfDummyScreenHeight-130))
        self.count_text = TextRenderComponent("3", 150, pygame.Color("white"), 0, 0, self)
        self.count_text.text_surface.set_alpha(180)

class InSceneMeteorCounter(GameObject):
    def __init__(self, scene):
        super().__init__("in_scene_meteor_counter", scene, scene.camera.get_rendering_layer_by_name("cockpit_layer"))
        self.remove_default_rect_image()

        self.transform.move_world_position(pygame.Vector2(700, 30))
        self.fix_game_object_on_screen(pygame.Vector2(700, 30))
        self.tot_meteors_render = TextRenderComponent("meteors in scene: ", 12, pygame.Color("white"), 0, 0, self)


class MeteorManager(GameObject):

    DifficultyInSeconds = 0

    def __init__(self, scene, rendering_layer):
        super().__init__("MeteorManager", scene, rendering_layer)

        self.remove_default_rect_image()
        self.stop_rendering_this_game_object()

        self.sound_count_down = pygame.mixer.Sound("game_res/audio/annauncer/3 2 1.wav")
        self.sound_go = pygame.mixer.Sound("game_res/audio/annauncer/Go 2.wav")

        self._instantiation_rect_top = RectTriggerComponent(0, -470, 1000, 100, self)
        self._instantiation_rect_bottom = RectTriggerComponent(0, 470, 1000, 100, self)
        self._instantiation_rect_left = RectTriggerComponent(-550, 0, 100, 800, self)
        self._instantiation_rect_right = RectTriggerComponent(550, 0, 100, 800, self)
        self._instantiation_rect_list = [self._instantiation_rect_top, self._instantiation_rect_bottom,
                                         self._instantiation_rect_left, self._instantiation_rect_right]

        self.score_ui: ScoreUi = self.scene.get_game_object_by_name("score")
        self.difficulty_cap = 0.30  # 0.30
        self._inst_frequency_in_sec = 0.75  # 0.75 # a.k.a. how hard it is
        self._instantiation_timer = TimerComponent(self._inst_frequency_in_sec * 1000, self, self._instantiate_meteor)

        self.player = self.scene.get_game_object_by_name("player")
        self.can_instantiate = False
        self.tot_meteors_in_scene = 0
        self._instantiation_allower = TimerComponent(3 * 1000, self, self._allow_instantiation)

        self.meteor_in_scene_counter = InSceneMeteorCounter(scene)
        self.count_down_ui = CountDownUi(scene)

    def game_object_scene_set_start(self) -> None:
        self.can_instantiate = False
        self.count_down_ui.start_rendering_this_game_object()
        self.sound_count_down.play()

        # remove all remaining meteors from scene
        for meteor in self.scene.game_object_list:
            if isinstance(meteor, Meteor):
                #print("meteor removido pelo meteoro manager no start")
                meteor.transform.move_world_position(pygame.Vector2(10000000, 10000000))
                meteor._set_to_garbage_collection()

        self._instantiation_allower.activate()

    def _allow_instantiation(self):
        self.can_instantiate = True
        self.sound_go.play()
        self.count_down_ui.stop_rendering_this_game_object()

    def game_object_update(self) -> None:

        # Countdown ui
        if not self.can_instantiate:
            counting = self._instantiation_allower.elapsed_time_read_only / 1000
            display = -1
            if counting <= 1:
                display = 3
            elif 1 <= counting <= 1.9:
                display = 2
            elif counting >= 1.9:
                display = 1
            text = f"{display}" if display != -1 else " "
            self.count_down_ui.count_text.set_text(text)
            self.count_down_ui.count_text.text_surface.set_alpha(180)

        # segunranca tira meteoro e conta quantos tem na cena
        pre = 0
        for obj in self.scene.game_object_list:
            if isinstance(obj, Meteor):
                pre += 1
                if not self.can_instantiate:
                    #print("meteor removido pelo meteoro manager no counter")
                    obj.transform.move_world_position(pygame.Vector2(10000000, 10000000))
                    obj._set_to_garbage_collection()

        self.tot_meteors_in_scene = pre
        self.meteor_in_scene_counter.tot_meteors_render.set_text(f"meteors in scene: {self.tot_meteors_in_scene}")

        # basicament vai diminuiton o intervalo de instanciamento dos meteros até um cap de 0.3 segundos
        # testei e acho q esse é o limite do jogável
        progressive_difficulty = self.score_ui.score_points_read_only / 1500
        difficulty_in_sec = self._inst_frequency_in_sec - progressive_difficulty
        if difficulty_in_sec < self.difficulty_cap:
            difficulty_in_sec = self.difficulty_cap
        MeteorManager.DifficultyInSeconds = difficulty_in_sec

        # meteor instantiation
        if not self.can_instantiate:
            return
        if not self._instantiation_timer.is_timer_active_read_only:
            self._instantiation_timer.set_duration_in_ms(difficulty_in_sec*1000)
            self._instantiation_timer.activate()


    def _instantiate_meteor(self):

        if not self.player.is_alive:
            return

        #print("meteoro criado")

        initial_pos = pygame.Vector2(0, 0)
        direction = pygame.Vector2(0, 0)

        # picked randomly
        random_index = random.randint(0, len(self._instantiation_rect_list) - 1)
        instantiation_rect = self._instantiation_rect_list[random_index]
        #print(f"rando index {random_index}")

        # sets a random point inside the instantiation rect
        start_range_point_x = instantiation_rect.world_position_read_only.x - instantiation_rect.width / 2
        end_range_point_x = instantiation_rect.world_position_read_only.x + instantiation_rect.width / 2
        start_range_point_y = instantiation_rect.world_position_read_only.y - instantiation_rect.height / 2
        end_range_point_y = instantiation_rect.world_position_read_only.y + instantiation_rect.height / 2
        initial_pos.x = random.randint(round(start_range_point_x), round(end_range_point_x))
        initial_pos.y = random.randint(round(start_range_point_y), round(end_range_point_y))

        # direction
        if instantiation_rect == self._instantiation_rect_top or instantiation_rect == self._instantiation_rect_bottom:
            direction.y = 1 if instantiation_rect == self._instantiation_rect_top else direction.y
            direction.y = -1 if instantiation_rect == self._instantiation_rect_bottom else direction.y
            #                            x = 0.1 <=> 1                 sign + || -
            direction.x = (random.randint(1, 10) / 10) * random.choice([1, -1])  # output is like x = 0.7 or -0.7
        else:
            direction.x = 1 if instantiation_rect == self._instantiation_rect_left else direction.x
            direction.x = -1 if instantiation_rect == self._instantiation_rect_right else direction.x
            #                          y = 0.1 <=> 1                 sign + || -
            direction.y = (random.randint(1, 10) / 10) * random.choice([1, -1])  # output is like y = 0.4 or -0.4

        # rank
        # 50% small, 30% mid, 20% big
        rank = None
        rank_picker = random.randint(1, 10)
        if 1 <= rank_picker <= 5:
            rank = Meteor.MeteorRank.Small
        elif 6 <= rank_picker <= 8:
            rank = Meteor.MeteorRank.Mid
        elif rank_picker <= 10:
            rank = Meteor.MeteorRank.Big

        # ==============================================================================================================

        direction = direction.normalize()
        # print(f"meteor init: {initial_pos}, dir: {direction}, rank: {rank}")
        Meteor(self.scene, rank, initial_pos, direction)
