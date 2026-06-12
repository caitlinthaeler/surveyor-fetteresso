"""
user_data.player_name - name entered by player for dialogues
user_data.next_level - next uncompleted level, 0 by default
"""
import pygame
import os, sys
import json
from assets_registry import Assets
from classes import Button, BackButton, BUTTON_WIDTH, BUTTON_HEIGHT, Fade
from config import DIALOGUE_DIR, FONT, FPS, SCREEN_WIDTH, SCREEN_HEIGHT, BORDER, MUSIC_DIR
from enum import SurfaceState

# structure:
#   /assests/dialogue <- DIALOGUE_DIR
#       / introduction
#       / chapter1
#       / chapter2
#       / chapter3
#       / end
#       credits.png
#       dialogue_box.png
#       dialogue.json

class Dialogue:
    def __init__(self, screen, clock):
        self.screen = screen # pygame display
        self.clock = clock
        self.font = FONT
        self.background = None
        self.character = None
        self.transition = Fade(self.screen, self.clock)
        # set global components:
        self.back_button = BackButton(self.screen, SurfaceState.START)
        self.dialogue_box_height = 205
        self.dialogue_box_width = 510
        self.dialogue_box = pygame.transform.scale(pygame.image.load(os.path.join(DIALOGUE_DIR, "dialogue_box.png")).convert(), (self.dialogue_box_width, self.dialogue_box_height))
        dialogue_file = os.path.join(DIALOGUE_DIR, "dialogue.json")
        with open(dialogue_file, "r") as f: # get the dialogue data
            self.dialogue_config = json.load(f)

    def run_cutscene(self, next_level, player_name):
        level = str(next_level)
        print("cutscene: " + level)
        if level not in self.dialogue_config:
            raise AttributeError(f"There is no chapter {level}")
        
        # retrive data for this level
        chapter = self.dialogue_config[level]
        chapter_path = os.path.join(DIALOGUE_DIR, chapter["folder"])
        self.index = 0 # scene
        self.last_scene = len(chapter["scenes"]) - 1
        self.load_scene_assets(player_name, chapter_path, chapter)
        print('is busy', pygame.mixer.music.get_busy())
        
        transition = True
        self.end = False
        if next_level == 5:
            self.end = True

        while True: # handle events:
            if not pygame.mixer.music.get_busy():
                Assets.background_music.sf_menu.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.rect.collidepoint(event.pos):
                        self.back_button.play_sound()
                        return self.back_button.action()
                    
                    if self.text_button.rect.collidepoint(event.pos):
                        self.text_button.play_sound()
                        if self.pressed_play(player_name, chapter_path, chapter):
                            return self.text_button.action()
                        
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE) or (event.key == pygame.K_RIGHT):
                        if self.pressed_play(player_name, chapter_path, chapter):
                            return self.text_button.action()
                    if (event.key == pygame.K_LEFT) and (self.index !=0):
                        self.index -= 1
                        self.load_scene_assets(player_name, chapter_path, chapter)


            self.render_display()
            if transition:
                self.transition.fade_in()
                transition = False
            pygame.display.flip()
            self.clock.tick(FPS)

    def pressed_play(self, player_name, chapter_path, chapter):
        if self.index != self.last_scene:
            self.index += 1
            self.load_scene_assets(player_name, chapter_path, chapter)
            return False
        self.text_button.play_sound()
        return True

    def load_scene_assets(self, player_name, chapter_path, chapter):
        self.cur_scene= chapter["scenes"][self.index]

        # set background image:
        bg_path = os.path.join(chapter_path,self.cur_scene["background"])
        self.background = pygame.transform.scale(pygame.image.load(bg_path).convert(), self.screen.get_size())

        # set sprite image:
        if self.cur_scene.get("character"):
            char_path = os.path.join(chapter_path,self.cur_scene["character"])
            self.character = pygame.transform.scale(pygame.image.load(char_path).convert_alpha(), (300, 300))
            pos = self.cur_scene["character_pos"]
            self.character_pos = (pos[0], pos[1])
        else:
            self.character = None

        start_sound = pygame.mixer.Sound(os.path.join(MUSIC_DIR, "game_start.mp3"))
        start_sound.set_volume(0.5)

        # set button:
        if self.last_scene == self.index:
            self.text_button = Button(self.screen, SurfaceState.GAME, SCREEN_WIDTH-BUTTON_WIDTH-BORDER*3, SCREEN_HEIGHT-BUTTON_HEIGHT-BORDER*3, "Play ->", sound = start_sound) # goes to game stage
        else:
            self.text_button = Button(self.screen, None, SCREEN_WIDTH-BUTTON_WIDTH-BORDER*3, SCREEN_HEIGHT-BUTTON_HEIGHT-BORDER*3, "Next") # goes to game stage

        # get text
        self.text = self.cur_scene["text"].replace("{player}", player_name)
        self.lines = self.get_lines(self.text)


    def render_display(self):
        # display background:
        self.screen.blit(self.background, (0, 0))

        # display sprite:
        if self.character:
            self.screen.blit(self.character, self.character_pos)

        # display dialogue box:
        if not self.end:
            self.screen.blit(self.dialogue_box, (SCREEN_WIDTH-self.dialogue_box_width-BORDER, SCREEN_HEIGHT-self.dialogue_box_height-BORDER))

            # display text
            for i, line in enumerate(self.lines):
                rendered = self.font.render(line, False, (255, 255, 255))
                self.screen.blit(rendered, (SCREEN_WIDTH-self.dialogue_box_width+BORDER, SCREEN_HEIGHT - self.dialogue_box_height + BORDER + i * 20))

            # display buttons:
            self.text_button.draw()
        self.back_button.draw()

    def get_lines(self, text):
        max_width = self.dialogue_box_width - BORDER*3 -15

        words = text.split(" ")
        lines = []
        current = ""

        for word in words:
            if self.font.size(current + " " + word)[0] <= max_width:
                current += word + " " # append to line
            else:
                lines.append(current)
                current = word + " " # start a new line
        lines.append(current) # last line
        
        return lines

