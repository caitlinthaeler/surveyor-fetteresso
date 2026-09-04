import pygame

from scene_manager import Scene
from assets_registry import Assets
from classes import (
    AnimatedButton, Button, Page, TextComponent,
    get_clicked_button, scale_hover, format_background,
)
from config import BORDER, SCREEN_WIDTH, SCREEN_HEIGHT


# Book art is placed so its two pages line up with PAGE_LEFT/RIGHT_POS.
BOOK_POS = (SCREEN_WIDTH//2 - 320, -140)
PAGE_W, PAGE_H = 200, 200
PAGE_LEFT_POS  = (160, 100)
PAGE_RIGHT_POS = (PAGE_W + 170 + 60, 100)


PAGES = [
    Page(
        width=180, 
        height=180,
        components=[
        TextComponent("Diary of the Weather, Fetteresso Estate, Aberdeen", position=(100, 20), anchor='center', color='dark', width=180),
    ]),
    Page(
        width=180, 
        height=180,
        components=[
        TextComponent("1795", position=(PAGE_W // 2, 0), anchor='center', width=180, ),

        TextComponent("Winter", position=(0, 20)),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Cloudy", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Rain", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(
        width=180, 
         height=180,
        components=[
        TextComponent("1796", position=(PAGE_W // 2, 20), anchor='center', width=180),

        TextComponent("Winter", position=(0, 40), width=180),
        TextComponent("Dry", position=(PAGE_W, 40), anchor='topright'),


        TextComponent("Spring", position=(0, 60)),
        TextComponent("Cloudy", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Dry", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(width=180, 
        height=180,
        components=[
        TextComponent("1797", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40), anchor='topleft'),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Rain", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Rain", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Rain", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(components=[
        TextComponent("1798", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40)),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Dry", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Rain", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(components=[
        TextComponent("1799", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40), anchor='topleft'),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Cloudy", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Dry", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(components=[
        TextComponent("1795", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40)),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Rain", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Cloudy", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(components=[
        TextComponent("1800", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40)),
        TextComponent("Dry", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Cloudy", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Cloudy", position=(PAGE_W, 100), anchor='topright'),
    ]),
    Page(components=[
        TextComponent("1801", position=(PAGE_W // 2, 20), anchor='center'),

        TextComponent("Winter", position=(0, 40)),
        TextComponent("Rain", position=(PAGE_W, 40), anchor='topright'),

        TextComponent("Spring", position=(0, 60)),
        TextComponent("Cloudy", position=(PAGE_W, 60), anchor='topright'),

        TextComponent("Summer", position=(0, 80)),
        TextComponent("Dry", position=(PAGE_W, 80), anchor='topright'),

        TextComponent("Autumn", position=(0, 100)),
        TextComponent("Rain", position=(PAGE_W, 100), anchor='topright'),
    ]),
]


class WeatherBookScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game):
        super().__init__(screen, clock)
        self.game = game

        self.music    = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain
        self.background = format_background(screen, "office_desk.png")

        self.book_image = Assets.animations.weather_book_open.current_frame.image

        self.pages = PAGES
        self.spread = 0   # index of the left-hand page of the open spread

        self.nav_buttons = [
            AnimatedButton(
                surface=self.screen, next_state="menu",
                animation=Assets.animations.menu_icon,
                x=BORDER, y=BORDER,
                hover_transforms=[scale_hover(1.1)],
                text="menu",
            ),
            AnimatedButton(
                surface=self.screen, next_state="office",
                animation=Assets.animations.office_icon,
                width=96,
                height=96,
                x=SCREEN_WIDTH - BORDER, y=BORDER, anchor="topright",
                hover_transforms=[scale_hover(1.1)],
            ),
        ]
        self.prev_page_btn = Button(
            surface=self.screen, next_state="prev_page",
            x=PAGE_LEFT_POS[0], y=SCREEN_HEIGHT - 60,
            width=80, height=35, text="< prev",
        )
        self.next_page_btn = Button(
            surface=self.screen, next_state="next_page",
            x=PAGE_RIGHT_POS[0] + PAGE_W - 80, y=SCREEN_HEIGHT - 60,
            width=80, height=35, text="next >",
        )

    # ── loop ─────────────────────────────────────────────────────────────────

    def update(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            clicked = get_clicked_button(event, self._clickables())
            if clicked:
                result = self._dispatch(clicked.action())
                if result:
                    return result
        return None

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.book_image, BOOK_POS)

        # Only the open spread is drawn — two pages at a time.
        self.pages[self.spread].render(self.screen, PAGE_LEFT_POS)
        if self.spread + 1 < len(self.pages):
            self.pages[self.spread + 1].render(self.screen, PAGE_RIGHT_POS)

        for btn in self.nav_buttons:
            btn.draw()
        if self._has_prev():
            self.prev_page_btn.draw()
        if self._has_next():
            self.next_page_btn.draw()

    # ── helpers ──────────────────────────────────────────────────────────────

    def _has_prev(self) -> bool:
        return self.spread - 2 >= 0

    def _has_next(self) -> bool:
        return self.spread + 2 < len(self.pages)

    def _clickables(self) -> list:
        btns = list(self.nav_buttons)
        if self._has_prev():
            btns.append(self.prev_page_btn)
        if self._has_next():
            btns.append(self.next_page_btn)
        return btns

    def _dispatch(self, action: str) -> str | None:
        if action in ("menu", "office"):
            return action
        if action == "prev_page" and self._has_prev():
            Assets.sounds.page_turning.play()
            self.spread -= 2
        elif action == "next_page" and self._has_next():
            Assets.sounds.page_turning.play()
            self.spread += 2
        return None
