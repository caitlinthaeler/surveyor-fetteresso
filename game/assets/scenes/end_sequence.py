# Final-decision scene: warn the player, let them pick a surveyor, then
# hand off to that surveyor's ending dialogue (player/end_<name>.json).
from enum import Enum

import pygame

from assets_registry import Assets
from classes import AnimatedButton, get_clicked_button, format_background, scale_hover, tint_hover
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER, FONT
from scene_manager import Scene
from dialogue_manager import DialogueManager
from game_manager import game_data


# (surveyor number, display name, ending dialogue file id in player/)
_PICKS = [
    (1, "Bob",     "end_bob"),
    (2, "Dave",    "end_dave"),
    (3, "Michael", "end_michael"),
]

_WARNING_LINES = [
    "This is your final decision.",
    "Once you name your assistant the survey begins,",
    "and there is no turning back.",
]

_COL_TEXT = (240, 235, 220)


class Stage(Enum):
    PROMPT  = 0   # "Proceed with Final Selection"
    WARNING = 1   # confirmation overlay
    CHOICES = 2   # pick a surveyor


class EndSequenceScene(Scene):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, game, vhs=None):
        super().__init__(screen, clock)
        self._game = game
        self._dialogue = DialogueManager(screen, clock, vhs)
        self.background = format_background(self.screen, "office_main.png")

        self.music    = Assets.background_music.sf_map
        self.ambience = Assets.sounds.thumping_rain

        self.stage = Stage.PROMPT
        self._next_scene: str | None = None

        cx = SCREEN_WIDTH // 2

        self.prompt_buttons = [
            self._button("proceed", "Proceed with Final Selection",
                         cx, SCREEN_HEIGHT // 2, 300, 50),
            self._back_button(),
        ]
        self.warning_buttons = [
            self._button("choices", "Decide now", cx - 95, SCREEN_HEIGHT - 110, 170, 46),
            self._button("prompt",  "Not yet",    cx + 95, SCREEN_HEIGHT - 110, 170, 46),
        ]
        self.choice_buttons = [
            self._button(f"pick_{num}", f"Choose {name} (Surveyor {num})",
                         cx, 190 + i * 95, 300, 62)
            for i, (num, name, _) in enumerate(_PICKS)
        ] + [self._back_button()]

    # ------------------------------------------------------------- button helpers

    def _button(self, action, text, x, y, w, h):
        return AnimatedButton(
            surface=self.screen,
            next_state=action,
            animation=Assets.animations.default_button,
            x=x, y=y, anchor="center",
            width=w, height=h,
            text=text,
            hover_transforms=[tint_hover((5, 5, 5)), scale_hover(1.05)],
        )

    def _back_button(self):
        return AnimatedButton(
            surface=self.screen,
            next_state="office",
            animation=Assets.animations.menu_icon,
            x=SCREEN_WIDTH - 200, y=BORDER,
            text="back",
            hover_transforms=[tint_hover((87, 0, 72)), scale_hover(1.1)],
        )

    # -------------------------------------------------------------------- loop

    def update(self) -> str | None:
        self.render()
        nxt, self._next_scene = self._next_scene, None
        return nxt

    def render(self):
        self.screen.blit(self.background, (0, 0))

        if self.stage is Stage.PROMPT:
            buttons = self.prompt_buttons
        elif self.stage is Stage.WARNING:
            self._draw_warning()
            buttons = self.warning_buttons
        else:
            self._draw_heading("Who will you take on as your assistant?")
            buttons = self.choice_buttons

        for b in buttons:
            b.draw()
        self._handle(buttons)

    # ------------------------------------------------------------------ drawing

    def _draw_heading(self, text: str):
        label = FONT.render(text, True, _COL_TEXT)
        self.screen.blit(label, label.get_rect(midtop=(SCREEN_WIDTH // 2, 70)))

    def _draw_warning(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        self.screen.blit(overlay, (0, 0))
        y = SCREEN_HEIGHT // 2 - 60
        for line in _WARNING_LINES:
            label = FONT.render(line, True, _COL_TEXT)
            self.screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 30

    # ------------------------------------------------------------------ events

    def _handle(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_scene = "quit"
                return
            clicked = get_clicked_button(event, buttons)
            if not clicked:
                continue
            action = clicked.action()
            if action == "office":
                self.stage = Stage.PROMPT
                self._next_scene = "office"
            elif action == "proceed":
                self.stage = Stage.WARNING
            elif action == "prompt":
                self.stage = Stage.PROMPT
            elif action == "choices":
                self.stage = Stage.CHOICES
            elif action.startswith("pick_"):
                self._run_ending(int(action.removeprefix("pick_")))
            return

    def _run_ending(self, num: int):
        start = next(fid for n, _, fid in _PICKS if n == num)
        game_data.flags.raise_flag("game_complete")
        self.stage = Stage.PROMPT
        self._next_scene = self._dialogue.run("player", self._game, start=start) or "menu"
