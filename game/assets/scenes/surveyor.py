from scene_manager import Scene
from dialogue_manager import DialogueManager
from assets_registry import Assets
from classes import format_background
import pygame


class SurveyorScene(Scene):
    surveyor_dir: str = ""
    background_file: str = ""   # set per subclass; loaded in __init__ once screen exists

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game, vhs=None):
        super().__init__(screen, clock)
        self.game = game
        self.music = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain
        self._dialogue = DialogueManager(screen, clock, vhs)
        self.background = format_background(screen, self.background_file) if self.background_file else None

    def update(self) -> str | None:
        self.render()
        return self._dialogue.run(self.surveyor_dir, self.game) or "world_map"

    def render(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 15, 40))


class SurveyorOneScene(SurveyorScene):
    surveyor_dir = "surveyor_one"
    background_file = "surveyor_1_office.png"


class SurveyorTwoScene(SurveyorScene):
    surveyor_dir = "surveyor_two"
    background_file = "surveyor_2_office.png"


class SurveyorThreeScene(SurveyorScene):
    surveyor_dir = "surveyor_three"
    background_file = "surveyor_3_office.png"
