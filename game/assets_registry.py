import pygame
from pygame.locals import *
import config
from config import SPRITES_DIR, SOUNDS_DIR, BASE_TILE_SIZE
from enum import Enum


class Frame:
    def __init__(self, path: str=None, color: tuple[int, int, int]=None, size: tuple[int, int]=None, offset: tuple[int, int]=(0,0), angle: float=0):
        self.path  = path
        self.color = color
        self.size = size
        self.offset = (offset[0], offset[1])
        self.angle = angle  
        
        # load image once
        if self.path:
            self.path = SPRITES_DIR + path
            image = pygame.image.load(self.path).convert_alpha()
            if self.size:
                image = pygame.transform.scale(image, self.size)
        else:
            image = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
            image.fill(self.color)
        # set rotation
        if self.angle != 0:
            self.image = pygame.transform.rotate(image, self.angle)
        else:
            self.image = image


class Animation:
    def __init__(self, frames: list[Frame], ticks_per_frame: int=-1, loop: bool=False):
        self.frames = frames
        self.ticks_per_frame = ticks_per_frame
        self.current_frame_index = 0
        self.ticks_elapsed = 0
        self.loop = loop
        self.paused = False

    @property
    def current_frame(self) -> Frame:
        return self.frames[self.current_frame_index]
    
    def set_frame(self, index: int):
        self.current_frame_index = max(0, min(index, len(self.frames) - 1))
        self.paused = True
    
    def update(self):
        if self.paused or self.ticks_per_frame == -1:
            return  # nothing to update

        self.ticks_elapsed += 1
        if self.ticks_elapsed >= self.ticks_per_frame:
            self.ticks_elapsed = 0
            if self.loop:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            else:
                self.current_frame_index = min(self.current_frame_index + 1, len(self.frames) - 1)




class Sprite:
    def __init__(self, x: float, y: float, animation: Animation):
        self.x = x
        self.y = y
        self.animation = animation
    
    def draw(self, screen: pygame.Surface):
        frame = self.animation.current_frame
        pos = (
            int(self.x * BASE_TILE_SIZE + frame.offset[0] + config.camera_offset[0]), 
            int(self.y * BASE_TILE_SIZE + frame.offset[1] + config.camera_offset[1]))
        screen.blit(frame.image, pos)
    
    def set_pos(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def set_animation(self, animation: Animation):
        self.animation = animation
        self.animation.current_frame_index = 0
        self.animation.ticks_elapsed = 0

    def get_animation(self) -> Animation | None:
        return self.animation
    

class AudioChannel(Enum):
    SOUND_EFFECTS = 0
    BACKGROUND_AMBIENCE = 1
    PLAYER = 2
    BACKGROUND_MUSIC = 3

class SoundEffect:
    pygame.mixer.set_num_channels(6)


    def __init__(self, path: str, volume: float=0.8, loop=False):
        self.sound = pygame.mixer.Sound(SOUNDS_DIR + path)
        self.sound.set_volume(volume)
        self.loop = -1 if loop else 0

    def play(self, channel: pygame.mixer.Channel=0):
        pygame.mixer.Channel(channel).play(self.sound, loops=self.loop)

    def stop(self):
        self.sound.stop()

class BackgroundMusic:
    current_track = None
    
    def __init__(self, path: str, volume: float=0.4):
        self.path = SOUNDS_DIR + path
        self.volume = volume
        

    def play(self, loops=-1):
        if BackgroundMusic.current_track != self.path:
            pygame.mixer.music.load(self.path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops)
            BackgroundMusic.current_track = self.path
        
    def stop(self):
        pygame.mixer.music.stop()
        BackgroundMusic.current_track = None

    def pause(self):
        pygame.mixer.music.pause()
    
    def unpause(self):
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume: float):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
    
    @staticmethod
    def fade_out(ms: int):
        pygame.mixer.music.fadeout(ms)
        BackgroundMusic.current_track = None

player_fps = 10
player_run_fps = 5
class Animations:
    default_button = Animation([Frame(path="items/button2.png", size=(100, 50))], ticks_per_frame=30)
    world_map_icon= Animation([
        Frame(path="items/map_icon_fetteresso.png", size=(100, 100))
        ], ticks_per_frame=30)
    
    menu_icon = Animation([
        Frame(path="items/button2.png", size=(100, 50))
        ], ticks_per_frame=30)
    
    office_icon = Animation([
        Frame(path="items/home_map_icon.png"),
        ], ticks_per_frame=30)
    
    my_map_icon = Animation([
        Frame(path="items/player_map.png", size=(140, 100)),
        ],ticks_per_frame=30)
    
    map_1_icon = Animation([
        Frame(path="items/surveyor_1_map.png", size=(200, 150))
        ], ticks_per_frame=30)
    
    map_2_icon = Animation([
        Frame(path="items/surveyor_2_map.png", size=(200, 150))
        ], ticks_per_frame=30)
    
    map_3_icon = Animation([
        Frame(path="items/surveyor_3_map.png", size=(200, 150))
        ], ticks_per_frame=30)
    
    
    # map_1_on_desk = Animation([
    #     Frame(path="items/surveyor_1_map.png", size=(300, 225))
    #     ], ticks_per_frame=30)
    
    #  map_2_on_desk = Animation([
    #     Frame(path="items/surveyor_2_map.png", size=(300, 225))
    #     ], ticks_per_frame=30)
    
    #  map_3_on_desk = Animation([
    #     Frame(path="items/surveyor_3_map.png", size=(300, 225))
    #     ], ticks_per_frame=30)
    
    # surveyor icon animations
    surveyor_1_icon = Animation([Frame(path="items/surveyor_1_icon.png", size=(100, 100))], ticks_per_frame=30)
    surveyor_1_icon_hover = Animation([Frame(path="items/surveyor_1_icon.png", size=(100, 100))], ticks_per_frame=30)
    
    surveyor_2_icon = Animation([Frame(path="items/surveyor_2_icon.png", size=(100, 100))], ticks_per_frame=30)
    surveyor_2_icon_hover = Animation([Frame(path="items/surveyor_2_icon.png", size=(100, 100))], ticks_per_frame=30)
    
    surveyor_3_icon = Animation([Frame(path="items/surveyor_3_icon.png", size=(100, 100))], ticks_per_frame=30)
    surveyor_3_icon_hover = Animation([Frame(path="items/surveyor_3_icon.png", size=(100, 100))], ticks_per_frame=30)

    # dialog characters
    surveyor_1_idle = Animation([Frame(path="items/surveyor_1.png")], ticks_per_frame=30)

    surveyor_2_idle = Animation([Frame(path="items/surveyor_2.png")], ticks_per_frame=30)

    surveyor_3_idle = Animation([Frame(path="items/surveyor_3.png")], ticks_per_frame=30)


    my_map = Animation([Frame(path="items/player_map.png")], ticks_per_frame=30)
    map_1 = Animation([Frame(path="items/surveyor_1_map.png")], ticks_per_frame=30)
    map_2 = Animation([Frame(path="items/surveyor_2_map.png")], ticks_per_frame=30)
    map_3 = Animation([Frame(path="items/surveyor_3_map.png")])

    weather_book = Animation([Frame(path="items/book_fetteresso.png")], ticks_per_frame=30)
    weather_book_open = Animation([Frame(path="items/book_fetteresso_open.png")], ticks_per_frame=30)

class Sound:
    birds_chirping = SoundEffect(path="countryside.mp3")
    page_turning = SoundEffect(path="book.mp3", volume=2)
    confirm = SoundEffect(path="confirm.mp3")
    default_button_click = SoundEffect(path="menu_selection.mp3", volume=0.4, loop=True)
    drownshock = SoundEffect(path="shock.mp3")
    thumping_rain = SoundEffect(path="thumping_rain.mp3", volume=1.5, loop=True)
    game_start = SoundEffect(path="game_start.mp3")
    anomaly_click = SoundEffect(path="shock.mp3", volume=0.4)
    papers_shuffling = SoundEffect(path="papers_shuffling.mp3", volume=0.4)

class Music:
    sf_menu= BackgroundMusic(path="sf_menu.wav", volume=1)
    sf_map = BackgroundMusic(path="The Spooky Papers.wav")
    sf_game = BackgroundMusic(path="The Spooky Papers-2.wav")




class Assets:
    animations = Animations
    sounds = Sound
    background_music = Music