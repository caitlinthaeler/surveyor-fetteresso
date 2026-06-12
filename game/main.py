
import pygame
from pygame.locals import *
pygame.init()
try:
    pygame.mixer.init()
except Exception:
    raise Exception("An audio output is required to run this game!")
from config import SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
from scene_manager import Fade, SceneManager
from assets.scenes.menu import MenuScene
from assets.scenes.office import OfficeScene
from assets.scenes.world_map import WorldMapScene
from assets.scenes.desk import DeskScene
from assets.scenes.surveyor import SurveyorOneScene, SurveyorTwoScene, SurveyorThreeScene
from assets.scenes.map_crumpling import MapCrumplingScene
from assets.scenes.introduction import IntroductionScene
from game_manager import NewGame

clock = pygame.time.Clock()
fade = Fade(screen, clock)

game = NewGame()
scene_manager = SceneManager()
scene_manager.scenes["menu"] = MenuScene(screen, clock, game)
scene_manager.scenes["office"] = OfficeScene(screen, clock)
scene_manager.scenes["world_map"] = WorldMapScene(screen, clock)
scene_manager.scenes["desk"] = DeskScene(screen, clock, game)
scene_manager.scenes["surveyor_one"] = SurveyorOneScene(screen, clock, game)
scene_manager.scenes["surveyor_two"] = SurveyorTwoScene(screen, clock, game)
scene_manager.scenes["surveyor_three"] = SurveyorThreeScene(screen, clock, game)
scene_manager.scenes["map_crumpling"] = MapCrumplingScene(screen, clock, game)
scene_manager.scenes["introduction"] = IntroductionScene(screen, clock, game)

scene_manager.switch_scene("menu")

while game.is_running():
    next_scene = scene_manager.current_scene.update()
    if next_scene == "quit":
        game.quit()
    elif next_scene:
        scene_manager.switch_scene(next_scene, fade=fade)
    else:
        scene_manager.current_scene.render()
    pygame.display.flip()
    clock.tick(60)
