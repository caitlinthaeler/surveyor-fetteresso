from assets_registry import Assets
from classes import AnimatedButton, format_background, get_clicked_button, rotate_hover, scale_hover, tint_hover
from config import BORDER, SCREEN_WIDTH, SCREEN_HEIGHT
from scene_manager import Scene
import pygame
from enum import Enum


class WorldMapState(Enum):
    IDLE = 0
    SURVEYOR_1 = 1
    SURVEYOR_2 = 2
    SURVEYOR_3 = 3
    OFFICE = 4

class WorldMapScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        # Initialize world map-specific attributes here
        self.music = "The Spooky Papers-2.mp3"

        self.state = WorldMapState.IDLE

        # scene actions
        self.state_actions = {
            WorldMapState.IDLE: self.idle,
            WorldMapState.SURVEYOR_1: self.go_to_surveyor_1,
            WorldMapState.SURVEYOR_2: self.go_to_surveyor_2,
            WorldMapState.SURVEYOR_3: self.go_to_surveyor_3,
            WorldMapState.OFFICE: self.go_to_office,
        }

        # music and ambience
        self.music = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        # background
        self.world_map_background = format_background(self.screen, "main_map.png")

        # adjust these parameters ONLY, to reposition buttons and popup:
        button_x, button_y, button_y_buffer = 248, 386, 63
        self.buttons = [

            # define buttons' name, position, and destination state, no need to adjust:
            
            # home button
            # goes back to office
            AnimatedButton(
                surface=self.screen,
                next_state=WorldMapState.OFFICE, 
                animation=Assets.animations.world_map_icon,
                x=SCREEN_WIDTH//2, 
                y=SCREEN_HEIGHT//2,
                text="office", 
                anchor="center",
                hover_transforms=[
                    tint_hover((0, 87, 72)),
                    scale_hover(1.1),
                    ],
                sound = Assets.sounds.page_turning),


            # surveyor 1 icon
            AnimatedButton(
                surface=self.screen,
                next_state=WorldMapState.SURVEYOR_1, 
                animation=Assets.animations.surveyor_1_icon,
                x=300, 
                y=100,
                text="suveyor 1 office",
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    ],
                ),


            #surveyor 2 icon
            AnimatedButton(
                surface=self.screen,
                next_state=WorldMapState.SURVEYOR_2, 
                animation=Assets.animations.surveyor_2_icon,
                x=100, 
                y=400,
                text="suveyor 2 office",
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    ],
                ),

            
            #surveyor 3 icon
            AnimatedButton(
                surface=self.screen,
                next_state=WorldMapState.SURVEYOR_3, 
                animation=Assets.animations.surveyor_3_icon,
                x=600, 
                y=350,
                text="surveyor 3 office",
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    ],
                ),



        ]

    def update(self):
        if self.state == WorldMapState.OFFICE:
            self.state = WorldMapState.IDLE
            return "office"
        elif self.state == WorldMapState.SURVEYOR_1:
            self.state = WorldMapState.IDLE
            return "surveyor_one"
        elif self.state == WorldMapState.SURVEYOR_2:
            self.state = WorldMapState.IDLE
            return "surveyor_two"
        elif self.state == WorldMapState.SURVEYOR_3:
            self.state = WorldMapState.IDLE
            return "surveyor_three"

    def render(self):
        self.state_actions[self.state]()

    def idle(self):
        for button in self.buttons: button.draw()
        for _ in self.handle_events(self.buttons): pass

    def go_to_surveyor_1(self):
        self.state = WorldMapState.SURVEYOR_1

    def go_to_surveyor_2(self):
        self.state = WorldMapState.SURVEYOR_2

    def go_to_surveyor_3(self):
        self.state = WorldMapState.SURVEYOR_3

    def go_to_office(self):
        self.state = WorldMapState.OFFICE

    def handle_events(self, buttons):
        for event in pygame.event.get():
            # return button that was clicked, if there was one:
            clicked_button = get_clicked_button(event, buttons)
            if clicked_button:
                self.state = clicked_button.action() # go to new menu state
                yield clicked_button
                continue # process remaining events
            yield event # return remaining events, itteratively
