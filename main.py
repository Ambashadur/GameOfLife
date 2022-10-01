import pygame
from pygame.locals import *
from cells import *
from button import *


flags = DOUBLEBUF


class GameOfLife:
    def __init__(self, width: int = 400, height: int = 400, cell_size: int = 8, fps: int = 20) -> None:
        self.screen_width = width + 100
        self.screen_height = height
        self.cell_size = cell_size
        self.fps = fps

        self.cell_w_count = width // cell_size
        self.cell_h_count = height // cell_size
        self.cell_height = height
        self.cell_width = width

        self.cell_colors: dict = {0: 'white', 1: 'black'}

        self.display = pygame.display.set_mode((self.screen_width, self.screen_height), flags=flags)
        self.cells = Cells(self.cell_w_count, self.cell_h_count)
        self.clock = None

        self.buttons = [
            Button(width + 12, 10, 78, 30, 'Start', 25, 'grey'),
            Button(width + 12, 50, 78, 30, 'Stop', 25, 'grey')
        ]

    def draw_cells(self, cells_array: list):
        for y in range(0, self.cell_h_count):
            for x in range(0, self.cell_w_count):
                if cells_array[y * self.cell_w_count + x] < 128:
                    color: Color = Color(self.cell_colors[cells_array[y * self.cell_w_count + x]])
                    draw.rect(
                        self.display,
                        color,
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def draw_menu(self):
        draw.line(self.display, Color('black'), (self.cell_width + 1, 0), (self.cell_width + 1, self.screen_height))

        for button in self.buttons:
            button.draw(self.display)

    def mouse_process(self):
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.is_mouse_on_button(self.display, mouse_pos):
                return

    def init_pygame(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Game of life')
        pygame.event.set_allowed([QUIT])

        self.display.fill(Color('white'))
        self.draw_menu()

        self.draw_cells(self.cells.array)
        pygame.display.flip()

    def run(self) -> None:
        self.init_pygame()

        while 1:

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    return

            self.cells.calculate_next_generation()
            self.draw_cells(self.cells.array)

            self.mouse_process()

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = GameOfLife(600, 600, 3, 30)
    game.run()
