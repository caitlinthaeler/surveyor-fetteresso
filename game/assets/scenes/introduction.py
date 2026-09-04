import pygame
from classes import format_background
from scene_manager import Scene
from dialogue_manager import DialogueManager
from assets_registry import Assets


class IntroductionScene(Scene):

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game, vhs=None):
        super().__init__(screen, clock)
        self._game = game
        self.music = Assets.background_music.sf_menu
        self.ambience = Assets.sounds.thumping_rain
        self._dialogue = DialogueManager(screen, clock, vhs)
        self.main_background = format_background(self.screen, "office_main.png")


    def update(self) -> str | None:
        self.render()
        return self._dialogue.run("player", self._game)

    def render(self):
        self.screen.blit(self.main_background, (0, 0))  