# contains all the flags and condition values throughout the game
from enum import Enum

class Flags():
    def __init__(self):
        self.flag_one = False
        self.flag_two = False
        self.flag_three = False
        # add more flags as needed

class GameState(Enum):
    RUNNING = 0
    PAUSED = 1
    SUCCESS = 2
    GAME_OVER = 3
    RESTART = 4
    START = 5
    RESUME = 6


class NewGame():
    def __init__(self):
        self.flags = Flags()
        self.state = GameState.RUNNING
        pass

    def raise_flag(self, flag_name):
        setattr(self.flags, flag_name, True)

    def is_running(self):
        return self.state == GameState.RUNNING

    def quit(self):
        self.state = GameState.GAME_OVER
    
# class LoadGame():
#     def __init__(self):
#         # load saved game data here
#         pass


