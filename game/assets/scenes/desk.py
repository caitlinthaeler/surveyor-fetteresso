import pygame
from enum import Enum
from scene_manager import Scene
from assets_registry import Assets
from classes import AnimatedButton, Button, get_clicked_button, scale_hover, tint_hover, format_background
from config import BORDER, SCREEN_WIDTH
from game_manager import game_data


SURVEYOR_MAP_ANIM = {
    1: Assets.animations.map_1,
    2: Assets.animations.map_2,
    3: Assets.animations.map_3,
}

SURVEYORS = {
    1: "surveyor_one",
    2: "surveyor_two",
    3: "surveyor_three",
}

# Per-map anomaly button positions: (center_x, center_y, radius)
_ANOMALY_POS = {
    1: (500, 200, 50),
    2: (600, 350, 50),
    3: (550, 500, 50),
}

anomaly_flags = {
    1: "bob_anomaly_found",
    2: "dave_anomaly_found",
    3: "michael_anomaly_found",
}


class DeskState(Enum):
    MENU             = 0
    BACK             = 1
    QUIT             = 2
    IDLE             = 3
    SHOW_INVESTIGATE = 4
    INVESTIGATE      = 5


class DeskScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game):
        super().__init__(screen, clock)
        self.game = game
        self.state = DeskState.IDLE
        self.show_investigate_button = False

        self.music    = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        self.desk_background = format_background(screen, "office_desk.png")

        # Nav buttons — always visible
        self.nav_buttons = [
            AnimatedButton(
                surface=self.screen,
                next_state=DeskState.MENU,
                animation=Assets.animations.menu_icon,
                x=BORDER, y=BORDER,
                text="menu",
                hover_transforms=[tint_hover((87, 0, 72)), scale_hover(1.1)],
            ),
            AnimatedButton(
                surface=self.screen,
                next_state=DeskState.BACK,
                animation=Assets.animations.menu_icon,
                x=SCREEN_WIDTH - 200, y=BORDER,
                text="back",
                hover_transforms=[tint_hover((87, 0, 72)), scale_hover(1.1)],
            ),
        ]

        # One anomaly button per map — only the one matching current_map is drawn/clickable
        self.anomaly_buttons = {
            map_num: Button(
                surface=self.screen,
                next_state=DeskState.SHOW_INVESTIGATE,
                x=cx - r, y=cy - r,
                width=r * 2, height=r * 2,
                text=f"anomaly {map_num}",
                sound=Assets.sounds.anomaly_click,
            )
            for map_num, (cx, cy, r) in _ANOMALY_POS.items()
        }

        # Investigate button — hidden until an anomaly is clicked
        self.investigate_button = Button(
            self.screen, DeskState.INVESTIGATE,
            248, 410, "Investigate",
        )

    # ------------------------------------------------------------------ loop

    def update(self) -> str | None:
        if self.state == DeskState.BACK:
            self.show_investigate_button = False
            self.state = DeskState.IDLE
            return "office"
        elif self.state == DeskState.MENU:
            self.show_investigate_button = False
            self.state = DeskState.IDLE
            return "menu"
        elif self.state == DeskState.SHOW_INVESTIGATE:
            self.show_investigate_button = True
            self.state = DeskState.IDLE
        elif self.state == DeskState.INVESTIGATE:
            game_data.flags.raise_flag(anomaly_flags.get(game_data.current_map, ""))
            self.state = DeskState.IDLE
            return SURVEYORS.get(game_data.current_map, "office")
        elif self.state == DeskState.QUIT:
            self.state = DeskState.IDLE
            return "quit"
        return None

    def render(self):
        self.screen.blit(self.desk_background, (0, 0))
        self._draw_maps()
        self._draw_buttons()
        for _ in self._handle_events():
            pass

    # --------------------------------------------------------------- drawing

    def _draw_maps(self):
        self.screen.blit(Assets.animations.my_map.current_frame.image, (50, 100))

        surveyor_anim = SURVEYOR_MAP_ANIM.get(game_data.current_map)
        if surveyor_anim:
            self.screen.blit(surveyor_anim.current_frame.image, (450, 100))

    def _draw_buttons(self):
        for btn in self.nav_buttons:
            btn.draw()

        # Anomaly buttons are invisible — draw a red circle outline only after clicked
        if self.show_investigate_button and game_data.current_map in _ANOMALY_POS:
            cx, cy, r = _ANOMALY_POS[game_data.current_map]
            pygame.draw.circle(self.screen, (220, 30, 30), (cx, cy), r, 3)
            self.investigate_button.draw()

    # ----------------------------------------------------------------- events

    def _handle_events(self):
        active = self.anomaly_buttons.get(game_data.current_map)
        clickable = list(self.nav_buttons)
        if active:
            clickable.append(active)
        if self.show_investigate_button:
            clickable.append(self.investigate_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = DeskState.QUIT
                return
            clicked = get_clicked_button(event, clickable)
            if clicked:
                self.state = clicked.action()
                yield clicked
                continue
            yield event
