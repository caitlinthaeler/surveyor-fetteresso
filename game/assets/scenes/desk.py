import pygame
from enum import Enum
from scene_manager import Scene
from assets_registry import Assets
from classes import AnimatedButton, Button, get_clicked_button, scale_hover, tint_hover, format_background
from config import BORDER, SCREEN_WIDTH, SCREEN_HEIGHT, FONT

_MAP_SCALE = 0.85
from game_manager import game_data

_SURVEYOR_NAMES = {
    1: "Surveyor Bob",
    2: "Surveyor Dave",
    3: "Surveyor Michael",
}

_SURVEYOR_ICONS = {
    1: Assets.animations.surveyor_1_icon,
    2: Assets.animations.surveyor_2_icon,
    3: Assets.animations.surveyor_3_icon,
}

_COL_LABEL = (220, 200, 140)

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
    1: (680, 260, 50),
    2: (695, 320, 50),
    3: (545, 300, 50),
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

    def _scale_map(self, surf: pygame.Surface) -> pygame.Surface:
        w = int(surf.get_width() * _MAP_SCALE)
        h = int(surf.get_height() * _MAP_SCALE)
        return pygame.transform.scale(surf, (w, h))

    def _draw_maps(self):
        # Left — player's map
        my_map = self._scale_map(Assets.animations.my_map.current_frame.image)
        self.screen.blit(my_map, (50, 100))
        self._draw_map_label(50, 70, "Your Map", Assets.animations.my_map_icon)

        # Right — selected surveyor's map
        surveyor_anim = SURVEYOR_MAP_ANIM.get(game_data.current_map)
        if surveyor_anim:
            s_map = self._scale_map(surveyor_anim.current_frame.image)
            self.screen.blit(s_map, (450, 100))
            name = _SURVEYOR_NAMES.get(game_data.current_map, "")
            self._draw_map_label(450, 70, name, None)

            # Surveyor icon — bottom right
            icon = _SURVEYOR_ICONS.get(game_data.current_map)
            if icon:
                icon_surf = icon.current_frame.image
                self.screen.blit(icon_surf, (
                    SCREEN_WIDTH - BORDER - icon_surf.get_width(),
                    SCREEN_HEIGHT - BORDER - icon_surf.get_height(),
                ))

    def _draw_map_label(self, x: int, y: int, name: str, icon):
        icon_surf = icon.current_frame.image if icon else None
        draw_x = x
        if icon_surf:
            self.screen.blit(icon_surf, (draw_x, y))
            draw_x += icon_surf.get_width() + 6
        label = FONT.render(name, True, _COL_LABEL)
        label_y = y + ((icon_surf.get_height() - label.get_height()) // 2 if icon_surf else 0)
        self.screen.blit(label, (draw_x, label_y))

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
