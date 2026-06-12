from scene_manager import Scene
import pygame

# happens in user's office
class DeskScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        # Initialize desk-specific attributes here
        self.music = "The Spooky Papers.mp3"
        self.ambience = "thumping_rain.mp3"

        # map comparison

        # investigate button

    def update(self):
        # Handle desk logic, such as interactions or events
        pass

    def render(self):
        # Draw the desk on the given surface
        self.screen.fill((150, 75, 0))  # Example background color
        # Add code to draw desk elements here