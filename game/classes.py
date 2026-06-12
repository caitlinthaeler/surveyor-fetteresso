import pygame
import os
from config import FONT, SCREEN_WIDTH, SOUNDS_DIR, UI_PATH, FONT, BORDER, SCALE_FACTOR
from assets_registry import Animation

class Button:
    default_button_height = 35
    default_button_width = 123
    default_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "menu_selection.mp3"))
    default_sound.set_volume(0.8)

    def __init__(self, surface, next_state, x, y, text, font=FONT, text_colour=(20,20,20), width=default_button_width, height=default_button_height, sound=default_sound):
        self.screen = surface
        self.next_state = next_state # return value of clicking the button
        self.base_rect = pygame.Rect(x, y, width, height) # original button dimentions and position
        self.rect = self.base_rect.copy() # copy, to be mutated
        self.text = text
        self.font = font
        self.text_colour = text_colour
        self.sound = sound
        self.base_image = pygame.image.load(os.path.join(UI_PATH, "button.png")).convert_alpha()
        self.background = pygame.transform.scale(self.base_image, self.rect.size)

    def draw(self):
        self.screen.blit(self.background, (self.rect.left, self.rect.top))
        label = self.font.render(self.text, False, self.text_colour)
        label_rect = label.get_rect(center=self.rect.center)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover()
        else:
            self.rect = self.base_rect
        self.background = pygame.transform.scale(self.base_image, self.rect.size)
        self.screen.blit(label, label_rect)

    def on_hover(self):
        self.rect = self.base_rect.inflate(5, 5)
        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(overlay, (87, 0, 72, 95), overlay.get_rect(), border_radius = 4)
        self.screen.blit(overlay, self.rect)

    def action(self):
        return self.next_state
    
    def play_sound(self):
        self.sound.play()

class BackButton(Button):
    def __init__(self, screen, previous_state):
        super().__init__(screen, previous_state, SCREEN_WIDTH-100-BORDER, BORDER, "Back", width=100)




class AnimatedButton:
    def __init__(self, surface, next_state,
                 animation: Animation,
                 x: int, y: int,
                 anchor: str = "topleft",
                 scale: float = SCALE_FACTOR,
                 hover_animation: Animation = None,
                 hover_inflate: tuple = (0, 0),
                 hover_transforms: list = None,
                 text: str = None,
                 font=FONT,
                 text_colour=(20, 20, 20),
                 sound=None):
        self.screen = surface
        self.next_state = next_state
        self.idle_animation = animation
        self.hover_animation = hover_animation
        self.scale = scale
        self.hover_inflate = hover_inflate
        self.hover_transforms = hover_transforms or []
        self.text = text
        self.font = font
        self.text_colour = text_colour
        self.sound = sound or Button.default_sound

        nw, nh = animation.current_frame.image.get_size()
        self.base_rect = pygame.Rect(0, 0, int(nw * scale), int(nh * scale))
        setattr(self.base_rect, anchor, (x, y))
        self.rect = self.base_rect.copy()

    def draw(self):
        is_hovered = self.base_rect.collidepoint(pygame.mouse.get_pos())

        anim = self.hover_animation if (is_hovered and self.hover_animation) else self.idle_animation
        anim.update()

        nw, nh = anim.current_frame.image.get_size()
        image = pygame.transform.scale(anim.current_frame.image, (int(nw * self.scale), int(nh * self.scale)))

        if is_hovered:
            for transform in self.hover_transforms:
                image = transform(image)

        self.rect = pygame.Rect(0, 0, *image.get_size())
        self.rect.center = self.base_rect.inflate(*self.hover_inflate).center if is_hovered else self.base_rect.center

        self.screen.blit(image, self.rect.topleft)

        if self.text:
            label = self.font.render(self.text, False, self.text_colour)
            self.screen.blit(label, label.get_rect(center=self.rect.center))

    def action(self):
        return self.next_state

    def play_sound(self):
        self.sound.play()


def scale_hover(factor: float):
    return lambda surf: pygame.transform.scale(
        surf, (int(surf.get_width() * factor), int(surf.get_height() * factor)))

def rotate_hover(angle: float):
    return lambda surf: pygame.transform.rotate(surf, angle)

def tint_hover(colour: tuple, alpha: int = 80):
    def _tint(surf):
        result = surf.copy()
        overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        overlay.fill((*colour, alpha))
        result.blit(overlay, (0, 0))
        return result
    return _tint


def get_clicked_button(event, buttons):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for button in buttons: # determine if user clicked a button
            if button.rect.collidepoint(event.pos):
                button.play_sound()
                return button
    return None
        

def format_background(screen: pygame.Surface, file_name: str):
    # load the background and scale it to fit the screen
    background_path = os.path.join(UI_PATH, file_name)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())
    return background