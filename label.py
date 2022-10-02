from pygame import Surface, Color, font, draw


class Label:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font_size: int, color: str = 'grey'):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._font_size = font_size
        self._color: Color = Color(color)

    def draw_text(self, surface: Surface, text: str = None):
        if text is not None:
            self._text = text

        rendered_text = font.Font(None, self._font_size).render(self._text, True, self._color)
        draw.rect(surface, Color('white'), (self._x, self._y, self._width, self._height))
        surface.blit(
            rendered_text,
            (self._x + self._width / 2 - rendered_text.get_width() / 2,
             self._y + self._height / 2 - rendered_text.get_height() / 2))
