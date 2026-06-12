from config import SCREEN_WIDTH, UI_PATH, BORDER
from scene_manager import Scene
from assets_registry import Assets
from classes import Button, AnimatedButton, get_clicked_button, format_background, scale_hover, rotate_hover, tint_hover
import pygame
from enum import Enum
import os

class OfficeState(Enum):
    MENU = 0
    WORLD_MAP = 1
    DESK = 2
    IDLE = 3
    QUIT = 4

    

class OfficeScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.state = OfficeState.IDLE

        # scene actions
        self.state_actions = {
            OfficeState.MENU: self.go_to_menu,
            OfficeState.WORLD_MAP: self.go_to_world_map,
            OfficeState.DESK: self.go_to_desk,
            OfficeState.IDLE: self.idle,
        }

        # music and ambience
        self.music = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        # background
        self.office_background = format_background(self.screen, "button.png")

        # adjust these parameters ONLY, to reposition buttons and popup:
        button_x, button_y, button_y_buffer = 248, 386, 63
        self.buttons = [

            # define buttons' name, position, and destination state, no need to adjust:
            
            # world map icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.WORLD_MAP, 
                animation=Assets.animations.world_map_icon,
                x=SCREEN_WIDTH//2, 
                y=BORDER,
                text="map", 
                hover_transforms=[
                    tint_hover((0, 87, 72)),
                    scale_hover(1.1),
                    rotate_hover(-5)
                    ],
                sound = Assets.sounds.page_turning),

            # menu icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.MENU,
                animation=Assets.animations.menu_icon,
                x=BORDER,
                y=BORDER,
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    rotate_hover(5)
                    ],
                ), # top left button

            # desk icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.DESK,
                animation=Assets.animations.menu_icon,
                x=BORDER+100, 
                y=button_y,
                text="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    rotate_hover(5)
                    ],
                ), # top left button

            #map 1 icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.MENU, 
                animation=Assets.animations.menu_icon,
                x=button_x, 
                y=button_y,
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    rotate_hover(5)
                    ],
                ), # top left button


            #map 2 icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.MENU, 
                animation=Assets.animations.menu_icon,
                x=button_x, 
                y=button_y,
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    rotate_hover(5)
                    ],
                ), # top left button

            
            #map 3 icon
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.MENU, 
                animation=Assets.animations.menu_icon,
                x=button_x, 
                y=button_y,
                anchor="center",
                hover_transforms=[
                    tint_hover((87, 0, 72)),
                    scale_hover(1.1),
                    rotate_hover(5)
                    ],
                ), # top left button



        ]


        # self.map_one = pygame.image.load(os.path.join(UI_PATH, "button.png")).convert_alpha()
        # self.spacebar = pygame.image.load(os.path.join(UI_PATH, "spacebar.png")).convert_alpha()
        # self.spacebar = pygame.transform.scale(self.spacebar, (200, 70))
        # self.info = pygame.image.load(os.path.join(UI_PATH, "info.png")).convert()
        # self.info = pygame.transform.scale(self.info, self.screen.get_size())


        # button to world map
        # button to menu
        # button to desk

    def update(self):
        if self.state == OfficeState.MENU:
            self.state = OfficeState.IDLE
            return "menu"
        elif self.state == OfficeState.WORLD_MAP:
            self.state = OfficeState.IDLE
            return "world_map"
        elif self.state == OfficeState.DESK:
            self.state = OfficeState.IDLE
            return "desk"
        elif self.state == OfficeState.QUIT:
            self.state = OfficeState.IDLE
            return "quit"
        return None

    def render(self):
        self.screen.blit(self.office_background, (0, 0)) # display menu graphic
        for button in self.buttons: button.draw() # display button graphic
        for _ in self.handle_events(self.buttons): pass

    def go_to_menu(self):
        self.state = OfficeState.MENU

    def go_to_world_map(self):
        self.state = OfficeState.WORLD_MAP

    def go_to_desk(self):
        self.state = OfficeState.DESK


    def idle(self):
        self.screen.blit(self.office_background, (0, 0)) # display menu graphic
        for button in self.buttons: button.draw() # display button graphic
        for _ in self.handle_events(self.buttons): pass

        


    def handle_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = OfficeState.QUIT
                return # exit immediately
            # return button that was clicked, if there was one:
            clicked_button = get_clicked_button(event, buttons)
            if clicked_button:
                self.state = clicked_button.action() # go to new menu state
                yield clicked_button
                continue # process remaining events
            yield event # return remaining events, itteratively

