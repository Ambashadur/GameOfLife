from pygame import Color, Surface, draw, font


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font_size: int, color: str = 'grey',
                 hovered_color: str = 'dark grey'):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height
        self.font_size = font_size
        self.color = Color(color)
        self.hovered_color = Color(hovered_color)

        self.rendered_text = None
        self.is_hovered = False

    def _draw(self, surface: Surface, color: Color) -> None:
        if self.rendered_text is None:
            self.rendered_text = font.Font(None, self.font_size).render(self.text, True, Color('black'))

        draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        surface.blit(
            self.rendered_text,
            (self.x + self.width / 2 - self.rendered_text.get_width() / 2,
             self.y + self.height / 2 - self.rendered_text.get_height() / 2))

    def draw(self, surface: Surface) -> None:
        self._draw(surface, self.color)

    def is_mouse_on_button(self, surface: Surface, mouse_pos: tuple) -> bool:
        is_on_button: bool = (self.x <= mouse_pos[0] <= self.x + self.width and
                              self.y <= mouse_pos[1] <= self.y + self.height)

        if self.is_hovered and not is_on_button:
            self._draw(surface, self.color)
            self.is_hovered = False
        elif not self.is_hovered and is_on_button:
            self._draw(surface, self.hovered_color)
            self.is_hovered = True
