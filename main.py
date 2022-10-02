import pygame
from pygame.locals import *
from cells import *
from button import *
from label import *


flags = DOUBLEBUF


class GameOfLife:
    def __init__(self, width: int = 400, height: int = 400, cell_size: int = 8, fps: int = 60,
                 cells_update_time: int = 20) -> None:
        self._screen_width = width + 100
        self._screen_height = height
        self._cell_size = cell_size
        self._fps = fps
        self._update = cells_update_time

        self._cell_w_count = width // cell_size
        self._cell_h_count = height // cell_size
        self._cell_height = height
        self._cell_width = width

        self._cell_colors: dict = {0: 'white', 1: 'black'}

        self._display = pygame.display.set_mode((self._screen_width, self._screen_height), flags=flags)
        self._cells = Cells(self._cell_w_count, self._cell_h_count)
        self._clock: pygame.time.Clock = None
        self._is_running = False

        self._buttons = [
            Button(x=width + 12, y=10, width=78, height=30, func=self._run_func,
                   text='Start', font_size=25, color='grey'),
            Button(x=width + 12, y=50, width=78, height=30, func=self._stop_func,
                   text='Stop', font_size=25, color='grey'),
            Button(x=width + 12, y=90, width=78, height=30, func=self._clear,
                   text='Clear', font_size=25, color='grey'),
            Button(x=width + 12, y=130, width=78, height=30, func=self._set_random,
                   text='Random', font_size=25, color='grey')
        ]

        self._info_label = Label(x=width + 12, y=height - 50, width=78, height=30, text='Stopped', font_size=25)

    def _draw_cells(self, cells_array: list):
        for y in range(0, self._cell_h_count):
            for x in range(0, self._cell_w_count):
                if cells_array[y * self._cell_w_count + x] < 128:
                    color: Color = Color(self._cell_colors[cells_array[y * self._cell_w_count + x]])
                    draw.rect(
                        self._display,
                        color,
                        (x * self._cell_size, y * self._cell_size, self._cell_size, self._cell_size))

    def _draw_menu(self):
        draw.line(self._display, Color('black'), (self._cell_width + 1, 0), (self._cell_width + 1, self._screen_height))

        for button in self._buttons:
            button.draw(self._display)

        self._info_label.draw_text(self._display)

    def _mouse_process(self, mouse_click: bool):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > self._cell_width:
            for button in self._buttons:
                if button.is_mouse_on_button(self._display, mouse_pos) and mouse_click:
                    button.function()
                    return

        elif mouse_click:
            self._change_cell_value(mouse_pos)

    def _stop_func(self) -> None:
        self._is_running = False
        self._info_label.draw_text(self._display, 'Stopped')

    def _run_func(self) -> None:
        self._is_running = True
        self._info_label.draw_text(self._display, 'Running')

    def _clear(self) -> None:
        self._cells.clear_cells()
        draw.rect(self._display, Color('white'), (0, 0, self._cell_width, self._cell_height))

    def _set_random(self) -> None:
        self._cells.set_random_cells()
        self._draw_cells(self._cells.array)

    def _change_cell_value(self, mouse_pos: tuple) -> None:
        x: int = mouse_pos[0] // self._cell_size
        y: int = mouse_pos[1] // self._cell_size
        self._cells.change_cell(x, y)
        self._draw_cells(self._cells.array)

    def _update_cells(self) -> None:
        if self._is_running:
            self._cells.calculate_next_generation()
            self._draw_cells(self._cells.array)

    def _init_pygame(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000 // self._update)
        pygame.display.set_caption('Game of life')
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN])

        self._display.fill(Color('white'))
        self._draw_menu()

        self._draw_cells(self._cells.array)
        pygame.display.flip()

    def run(self) -> None:
        self._init_pygame()

        mouse_click: bool = False
        update_cells: bool = False

        while 1:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        return

                    case pygame.MOUSEBUTTONDOWN:
                        mouse_click = True

                    case pygame.USEREVENT:
                        update_cells = True

            self._mouse_process(mouse_click)
            mouse_click = False

            if update_cells:
                self._update_cells()
                update_cells = False

            pygame.display.update()
            self._clock.tick(self._fps)


if __name__ == '__main__':
    game = GameOfLife(600, 600, 3, 60, 30)
    game.run()
