from scene_manager import Scene
import pygame

class SurveyorOneScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.ambience = "thumping_rain.mp3"

    def update(self):
        # Handle surveyor logic, such as interactions or events
        pass

    def render(self):
        # Draw the surveyor on the given surface
        self.screen.fill((0, 0, 150))  # Example background color
        # Add code to draw surveyor elements here

class SurveyorTwoScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.ambience = "thumping_rain.mp3"

    def update(self):
        # Handle surveyor logic, such as interactions or events
        pass

    def render(self):
        # Draw the surveyor on the given surface
        self.screen.fill((0, 0, 200))  # Example background color
        # Add code to draw surveyor elements here

class SurveyorThreeScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.ambience = "thumping_rain.mp3"

    def update(self):
        # Handle surveyor logic, such as interactions or events
        pass

    def render(self):
        # Draw the surveyor on the given surface
        self.screen.fill((0, 0, 250))  # Example background color
        # Add code to draw surveyor elements here