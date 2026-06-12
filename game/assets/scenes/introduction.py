import pygame
from scene_manager import Scene
from dialogue_manager import DialogueManager


class IntroductionScene(Scene):

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game):
        super().__init__(screen, clock)
        self._game = game
        self._dialogue = DialogueManager(screen, clock)

    def update(self) -> str | None:
        self.render()
        return self._dialogue.run("player", self._game)

    def render(self):
        self.screen.fill((10, 8, 15))
