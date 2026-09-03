from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER, FONT
from scene_manager import Scene
from assets_registry import Assets, Animation, Frame
from classes import AnimatedButton, get_clicked_button, format_background, scale_hover, tint_hover
import pygame
from enum import Enum
from game_manager import game_data


def _invisible_anim(w: int, h: int) -> Animation:
    return Animation([Frame(color=(0, 0, 0, 0), size=(w, h))], ticks_per_frame=30)


# Default tint for each surveyor's map overlay; the desk overlay borrows the
# tint of whichever map is currently on the desk.
_MAP_TINTS = [
    (80, 140, 230),   # map 1 — blue
    (90, 200, 110),   # map 2 — green
    (230, 150, 80),   # map 3 — orange
]
_TINT_ALPHA = 55


def _tint_anim(w: int, h: int, rgb: tuple) -> Animation:
    return Animation([Frame(color=(*rgb, _TINT_ALPHA), size=(w, h))], ticks_per_frame=30)


# Original centres / sizes for the 3 surveyor map icons — adjust to match your artwork.
_MAP_ORIGINS = [
    (180, 150),   # map 1
    (300, 150),   # map 2
    (225, 250),   # map 3
]
_MAP_SIZES = [
    (120, 80),    # map 1
    (100, 90),    # map 2
    (200, 60),    # map 3
]
# How fast a map slides between wall and desk (0..1 per frame lerp factor).
_SLIDE_SPEED = 0.18


class OfficeState(Enum):
    MENU       = 0
    WORLD_MAP  = 1
    DESK       = 2
    IDLE       = 3
    QUIT       = 4
    SURVEYOR_1 = 5
    SURVEYOR_2 = 6
    SURVEYOR_3 = 7
    WEATHER_BOOK = 8


class OfficeScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__(screen, clock)
        self.state = OfficeState.IDLE

        self.music    = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        self.office_background = format_background(self.screen, "office_main.png")

        self.buttons = [
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.WORLD_MAP,
                animation=Assets.animations.world_map_icon,
                x=SCREEN_WIDTH - BORDER, y=BORDER,
                anchor="topright",
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
            # Surveyor map icons — positions updated each frame in render().
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_1,
                animation=_tint_anim(*_MAP_SIZES[0], _MAP_TINTS[0]),
                x=_MAP_ORIGINS[0][0], y=_MAP_ORIGINS[0][1],
                anchor="center",
                width=_MAP_SIZES[0][0], height=_MAP_SIZES[0][1],
                hover_transforms=[tint_hover((255, 255, 255))],
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_2,
                animation=_tint_anim(*_MAP_SIZES[1], _MAP_TINTS[1]),
                x=_MAP_ORIGINS[1][0], y=_MAP_ORIGINS[1][1],
                anchor="center",
                width=_MAP_SIZES[1][0], height=_MAP_SIZES[1][1],
                hover_transforms=[tint_hover((255, 255, 255))],
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=OfficeState.SURVEYOR_3,
                animation=_tint_anim(*_MAP_SIZES[2], _MAP_TINTS[2]),
                x=_MAP_ORIGINS[2][0], y=_MAP_ORIGINS[2][1],
                anchor="center",
                width=_MAP_SIZES[2][0], height=_MAP_SIZES[2][1],
                hover_transforms=[tint_hover((255, 255, 255))],
            ),
        ]

        self.record_book: AnimatedButton = AnimatedButton(
            surface=self.screen,
            next_state=OfficeState.WEATHER_BOOK,
            animation=Assets.animations.weather_book,
            x=50, y=SCREEN_HEIGHT - 15,
            anchor="bottomleft",
            width=19*3, height=26*3,
            hover_transforms=[tint_hover((105, 205, 205)), scale_hover(1.1)],
        )

        self._map_buttons = self.buttons[2:]

        # Desk hit area — only drawn and clickable when a map is selected.
        self._desk_button = AnimatedButton(
            surface=self.screen,
            next_state=OfficeState.DESK,
            animation=_invisible_anim(400, 100),
            x=SCREEN_WIDTH - BORDER,
            y=SCREEN_HEIGHT,
            anchor="bottomright",
            width=425, height=75,
            hover_transforms=[tint_hover((255, 255, 255))],
        )
        # Per-map slide progress: 0.0 = resting on the wall, 1.0 = spread on the desk.
        self._map_slide = [0.0, 0.0, 0.0]

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
        elif self.state == OfficeState.WEATHER_BOOK:
            self.state = OfficeState.IDLE
            return "weather_book"
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

        # Slide/expand each map between its wall origin and the desk hit area.
        desk_cx, desk_cy = self._desk_button.base_rect.center
        desk_w, desk_h = self._desk_button.base_rect.size
        for i, btn in enumerate(self._map_buttons):
            target = 1.0 if game_data.current_map == (i + 1) else 0.0
            self._map_slide[i] += (target - self._map_slide[i]) * _SLIDE_SPEED
            t = self._map_slide[i]
            ox, oy = _MAP_ORIGINS[i]
            ow, oh = _MAP_SIZES[i]
            btn.base_rect.size = (round(ow + (desk_w - ow) * t), round(oh + (desk_h - oh) * t))
            btn.base_rect.center = (round(ox + (desk_cx - ox) * t), round(oy + (desk_cy - oy) * t))

        for button in self.buttons:
            button.draw()

        if game_data.flags.check("rained_1797"):
            self.record_book.draw()
            clickable = self.buttons + [self.record_book]
        else:
            clickable = list(self.buttons)
        if game_data.current_map is not None:
            self._desk_button.draw()  # drawn last -> sits on top of the slid map
            # desk button first in the list so it wins clicks in the overlap zone
            clickable.insert(0, self._desk_button)
        for _ in self.handle_events(clickable):
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
