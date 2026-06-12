from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER
from scene_manager import Scene
from assets_registry import Assets
from classes import AnimatedButton, get_clicked_button, format_background, scale_hover, tint_hover
import pygame
from enum import Enum
from game_manager import game_data

# Original centres for the 3 surveyor map icons — adjust to match your artwork.
_MAP_ORIGINS = [
    (200, 200),   # map 1
    (375, 225),   # map 2
    (274, 350),   # map 3
]
# Where the selected map icon slides to on the desk.
_MAP_DESK_CENTER = (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150)


class OfficeState(Enum):
    MENU       = 0
    WORLD_MAP  = 1
    DESK       = 2
    IDLE       = 3
    QUIT       = 4
    SURVEYOR_1 = 5
    SURVEYOR_2 = 6
    SURVEYOR_3 = 7


class OfficeScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.state = OfficeState.IDLE

        self.music    = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        self.office_background = format_background(self.screen, "button.png")

        self.buttons = [
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.WORLD_MAP,
                animation=Assets.animations.world_map_icon,
                x=SCREEN_WIDTH // 2 - 50, y=BORDER,
                text="map",
                hover_transforms=[tint_hover((0, 87, 72)), scale_hover(1.1)],
                sound=Assets.sounds.page_turning,
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.MENU,
                animation=Assets.animations.menu_icon,
                x=BORDER, y=BORDER,
                text="menu",
                hover_transforms=[tint_hover((87, 0, 72)), scale_hover(1.1)],
            ),
            # Desk icon — bottom right; clicking this navigates to the desk scene.
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.DESK,
                animation=Assets.animations.my_map_icon,
                x=SCREEN_WIDTH - BORDER, y=SCREEN_HEIGHT - BORDER,
                anchor="bottomright",
                text="my map",
                hover_transforms=[tint_hover((87, 0, 72)), scale_hover(1.1)],
            ),
            # Surveyor map icons — positions updated each frame in render().
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_1,
                animation=Assets.animations.map_1_icon,
                x=_MAP_ORIGINS[0][0], y=_MAP_ORIGINS[0][1],
                anchor="center",
                text="surveyor 1 map",
                hover_transforms=[tint_hover((87, 0, 72))],
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_2,
                animation=Assets.animations.map_2_icon,
                x=_MAP_ORIGINS[1][0], y=_MAP_ORIGINS[1][1],
                anchor="center",
                text="surveyor 2 map",
                hover_transforms=[tint_hover((87, 0, 72))],
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_3,
                animation=Assets.animations.map_3_icon,
                x=_MAP_ORIGINS[2][0], y=_MAP_ORIGINS[2][1],
                anchor="center",
                text="surveyor 3 map",
                hover_transforms=[tint_hover((87, 0, 72))],
            ),
        ]

        self._map_buttons = self.buttons[3:]

    def update(self):
        if self.state == OfficeState.MENU:
            self.state = OfficeState.IDLE
            return "menu"
        elif self.state == OfficeState.WORLD_MAP:
            self.state = OfficeState.IDLE
            return "world_map"
        elif self.state == OfficeState.DESK:
            self.state = OfficeState.IDLE
            if game_data.current_map is not None:
                if not game_data.flags.check("map_crumpled"):
                    return "map_crumpling"
                return "desk"
        elif self.state == OfficeState.SURVEYOR_1:
            game_data.current_map = None if game_data.current_map == 1 else 1
            self.state = OfficeState.IDLE
        elif self.state == OfficeState.SURVEYOR_2:
            game_data.current_map = None if game_data.current_map == 2 else 2
            self.state = OfficeState.IDLE
        elif self.state == OfficeState.SURVEYOR_3:
            game_data.current_map = None if game_data.current_map == 3 else 3
            self.state = OfficeState.IDLE
        elif self.state == OfficeState.QUIT:
            self.state = OfficeState.IDLE
            return "quit"
        return None

    def render(self):
        self.screen.blit(self.office_background, (0, 0))
        for i, btn in enumerate(self._map_buttons):
            btn.base_rect.center = _MAP_DESK_CENTER if game_data.current_map == (i + 1) else _MAP_ORIGINS[i]
        for button in self.buttons:
            button.draw()
        for _ in self.handle_events(self.buttons):
            pass

    def handle_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = OfficeState.QUIT
                return
            clicked_button = get_clicked_button(event, buttons)
            if clicked_button:
                self.state = clicked_button.action()
                yield clicked_button
                continue
            yield event
