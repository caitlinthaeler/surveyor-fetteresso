import pygame
import os
from config import FONT, SCREEN_WIDTH, SOUNDS_DIR, UI_PATH, FONT, BORDER, SCALE_FACTOR
from assets_registry import Animation, Frame


class Button:
    default_button_height = 35
    default_button_width = 123
    default_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "menu_selection.mp3"))
    default_sound.set_volume(0.8)

    def __init__(self, surface, next_state, x, y, text, font=FONT, text_colour=(20,20,20), width=default_button_width, height=default_button_height, sound=default_sound, enabled=True):
        self.screen = surface
        self.next_state = next_state # return value of clicking the button
        self.base_rect = pygame.Rect(x, y, width, height)
        self.rect = self.base_rect.copy() # copy, to be mutated
        self.text = text
        self.font = font
        self.text_colour = text_colour
        self.sound = sound
        self.enabled = enabled
        self.base_image = pygame.image.load(os.path.join(UI_PATH, "button2.png")).convert_alpha()
        self.background = pygame.transform.scale(self.base_image, self.rect.size)

    def draw(self):
        self.screen.blit(self.background, (self.rect.left, self.rect.top))
        label = self.font.render(self.text, True, self.text_colour)
        label_rect = label.get_rect(center=self.rect.center)
        if not self.enabled:
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 160))
            self.screen.blit(overlay, self.rect.topleft)
            self.screen.blit(label, label_rect)
            return
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
                 width: int = None,
                 height: int = None,
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
        w = width  if width  is not None else int(nw * scale)
        h = height if height is not None else int(nh * scale)
        self._custom_size = width is not None or height is not None
        self.base_rect = pygame.Rect(0, 0, w, h)
        setattr(self.base_rect, anchor, (x, y))
        self.rect = self.base_rect.copy()

    def draw(self):
        is_hovered = self.base_rect.collidepoint(pygame.mouse.get_pos())

        anim = self.hover_animation if (is_hovered and self.hover_animation) else self.idle_animation
        anim.update()

        if self._custom_size:
            image = pygame.transform.scale(anim.current_frame.image, self.base_rect.size)
        else:
            nw, nh = anim.current_frame.image.get_size()
            image = pygame.transform.scale(anim.current_frame.image, (int(nw * self.scale), int(nh * self.scale)))

        if is_hovered:
            for transform in self.hover_transforms:
                image = transform(image)

        self.rect = pygame.Rect(0, 0, *image.get_size())
        self.rect.center = self.base_rect.inflate(*self.hover_inflate).center if is_hovered else self.base_rect.center

        self.screen.blit(image, self.rect.topleft)

        if self.text:
            label = self.font.render(self.text, True, self.text_colour)
            label_rect = label.get_rect(center=self.rect.center)
            self.screen.blit(label, label_rect)
            self.rect = self.rect.union(label_rect)  # expand hit area to cover the label

    def action(self):
        return self.next_state

    def play_sound(self):
        self.sound.play()

class ImageComponent:
    """A single image to be drawn on a page at a given position."""
    def __init__(self, image: Frame, position: tuple[int, int], visible: bool = True):
        self.image = image
        self.position = position
        self.visible = visible

    def setVisible(self, visible: bool):
        self.visible = visible

    def render(self, surface: pygame.Surface, origin: tuple[int, int] = (0, 0)):
        """Blit this image onto surface at origin + position (page-relative coords)."""
        if not self.visible:
            return
        img = self.image.image if isinstance(self.image, Frame) else self.image
        surface.blit(img, (origin[0] + self.position[0], origin[1] + self.position[1]))

class TextComponent:
    font_sizes = {
        'small': pygame.font.Font(os.path.join(UI_PATH, "pixelfont.ttf"), 16),
        'medium': pygame.font.Font(os.path.join(UI_PATH, "pixelfont.ttf"), 20),
        'large': pygame.font.Font(os.path.join(UI_PATH, "pixelfont.ttf"), 24),
    }
    text_colors = {
        'dark': (20, 20, 20),
        'light': (0, 87, 72),
        'red': (220, 60, 60),
    }

    def __init__(self,
                 text: str, 
                 position: tuple[int, int], 
                 anchor: str = 'topleft',
                width: int = None, height: int = None,
                font_size: str = 'medium', 
                color: str = 'dark', 
                visible: bool = True):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.anchor = anchor
        self.font_size = font_size
        self.color = color
        self.visible = visible

    def setVisible(self, visible: bool):
        self.visible = visible

    def _lines(self, font) -> list[str]:
        if self.width:
            lines = []
            for paragraph in self.text.split("\n"):
                lines.extend(self._wrap_text(paragraph, font, self.width))
            return lines
        return self.text.split("\n")

    def _wrap_text(self, text: str, font, max_width: int) -> list[str]:
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if not current or font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]


    def render(self, surface: pygame.Surface, origin: tuple[int, int] = (0, 0)):
        if not self.visible or not self.text:
            return
        font = TextComponent.font_sizes.get(self.font_size, TextComponent.font_sizes['medium'])
        colour = TextComponent.text_colors.get(self.color, TextComponent.text_colors['dark'])

        x = origin[0] + self.position[0]
        y = origin[1] + self.position[1]
        for line in self._lines(font):
            label = font.render(line, True, colour)
            rect = label.get_rect()
            setattr(rect, self.anchor, (x, y))
            surface.blit(label, rect)
            y += font.get_height()

class Page:
    def __init__(self, base_image: pygame.Surface = None, width: int = 180, height: int = 180, components: list[TextComponent] = None):
        self.base_image = base_image
        self.width = width
        self.height = height
        self.components = components if components is not None else [] # can be image or text

    # def set_image(self, piece_image: Frame, position: tuple[int, int], visible: bool = True):
    #     self.components.append(ImageComponent(piece_image, position, visible))

    def set_text(self, text: str, position: tuple[int, int], text_align: str = 'topleft',
                 width: int = None, height: int = None,
                 font_size: str = 'medium', color: str = 'dark', visible: bool = True):
        self.components.append(TextComponent(text, position, text_align, width, height, font_size, color, visible))

    def render(self, surface: pygame.Surface, origin: tuple[int, int] = (0, 0)):
        if self.base_image:
            surface.blit(self.base_image, origin)
        for component in self.components:
            if component.visible:
                component.render(surface, origin)



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
        for button in buttons:
            if getattr(button, "enabled", True) and button.rect.collidepoint(event.pos):
                button.play_sound()
                return button
    return None
        

def format_background(screen: pygame.Surface, file_name: str):
    # load the background and scale it to fit the screen
    background_path = os.path.join(UI_PATH, file_name)
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())
    return background


class Image:
    def __init__(self, screen: pygame.Surface, file_name: str, scale: float = 1.0):
        self.screen = screen
        self.image = self.format_ui_image(file_name, scale)

    def draw(self, x: int, y: int):
        self.screen.blit(self.image, (x, y))

    def format_ui_image(file_name: str, scale: float = 1.0):
        # load the image and scale it to fit the screen
        image_path = os.path.join(UI_PATH, file_name)
        image = pygame.image.load(image_path).convert_alpha()
        w = int(image.get_width() * scale)
        h = int(image.get_height() * scale)
        image = pygame.transform.scale(image, (w, h))
        return image