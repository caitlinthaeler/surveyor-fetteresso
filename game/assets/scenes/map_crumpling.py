import pygame
from scene_manager import Scene
from assets_registry import Assets, AudioChannel
from game_manager import game_data

_DURATION = 180   # frames to show before auto-advancing (~3 s at 60 fps)



class MapCrumplingScene(Scene):

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game):
        super().__init__(screen, clock)
        self.game = game
        self._timer = 0

    def update(self):
        if self._timer == 0:
            Assets.sounds.papers_shuffling.play(AudioChannel.SOUND_EFFECTS.value)

        self._timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if self._timer >= _DURATION:
            pygame.mixer.Channel(AudioChannel.SOUND_EFFECTS.value).stop()
            game_data.flags.raise_flag("map_crumpled")
            self.game.save()
            self._timer = 0
            return "desk"

        return None

    def render(self):
        self.screen.fill((10, 8, 15))
