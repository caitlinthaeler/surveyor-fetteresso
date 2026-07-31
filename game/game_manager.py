import os
import json
from enum import Enum

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.json")


class FlagStore:
    def __init__(self):
        self._flags: dict[str, bool] = {}

    def raise_flag(self, name: str):
        self._flags[name] = True

    def lower_flag(self, name: str):
        self._flags[name] = False

    def check(self, name: str) -> bool:
        return self._flags.get(name, False)

    def check_all(self, names: list) -> bool:
        return all(self.check(n) for n in names)

    def check_none(self, names: list) -> bool:
        return not any(self.check(n) for n in names)

    def to_dict(self) -> dict:
        return dict(self._flags)

    def _reset(self):
        self._flags = {}

    def _load(self, data: dict):
        self._flags = dict(data)


class GameData:
    def __init__(self):
        self.flags = FlagStore()
        self.player_name: str = "Player"
        self.current_map: int | None = None   # 1, 2, or 3

    def _reset(self):
        self.flags._reset()
        self.player_name = "Player"
        self.current_map = None

    def _load(self, data: dict):
        self.flags._load(data.get("flags", {}))
        self.player_name = data.get("player_name", "Player")
        self.current_map = data.get("current_map")

    def _to_dict(self) -> dict:
        return {
            "player_name": self.player_name,
            "current_map": self.current_map,
            "flags": self.flags.to_dict(),
        }


# Module-level singleton — import and read from anywhere:
#   from game_manager import game_data
game_data = GameData()


class RunState(Enum):
    RUNNING = 0
    PAUSED = 1
    SUCCESS = 2
    GAME_OVER = 3
    RESTART = 4
    START = 5
    RESUME = 6


class NewGame:
    """Manages save / load / quit. Operates on the global game_data singleton."""

    def __init__(self):
        game_data._reset()
        self.state = RunState.RUNNING

    # convenience proxies so scenes that already hold a game ref still work
    @property
    def flags(self):
        return game_data.flags

    def raise_flag(self, name: str):
        game_data.flags.raise_flag(name)
        self.save()

    def check_flag(self, name: str) -> bool:
        return game_data.flags.check(name)

    def is_running(self) -> bool:
        return self.state == RunState.RUNNING

    def quit(self):
        self.state = RunState.GAME_OVER

    def save(self):
        with open(SAVE_PATH, "w") as f:
            json.dump(game_data._to_dict(), f, indent=2)

    def load(self) -> bool:
        if not os.path.exists(SAVE_PATH):
            return False
        with open(SAVE_PATH) as f:
            data = json.load(f)
        game_data._load(data)
        return True

    @staticmethod
    def has_save() -> bool:
        return os.path.exists(SAVE_PATH)
