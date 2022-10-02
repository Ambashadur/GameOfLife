import numpy as np
import ctypes


class Cells:
    def __init__(self, cells_width: int = 100, cells_height: int = 100):
        array = np.zeros(cells_width * cells_height, dtype=np.uint8)

        self.width = cells_width
        self.height = cells_height
        self.array = (ctypes.c_uint8 * (cells_width * cells_height))(*list(array))
        self._array_len = cells_width * cells_height

        self._dll = ctypes.CDLL('c_functions/lib.so')
        self._dll.calculate_next_generation.argtypes = [ctypes.c_uint8 * self._array_len,
                                                        ctypes.c_uint32, ctypes.c_uint32]
        self._dll.change_cell_value.argtypes = [ctypes.c_uint8 * self._array_len, ctypes.c_int,
                                                ctypes.c_int, ctypes.c_int, ctypes.c_int]

    def calculate_next_generation(self) -> None:
        self._dll.calculate_next_generation(self.array, self.width, self.height)

    def clear_cells(self) -> None:
        self.array = (ctypes.c_uint8 * self._array_len)(*list(np.zeros(self._array_len, dtype=np.uint8)))

    def set_random_cells(self) -> None:
        self.array = (ctypes.c_uint8 * self._array_len)(*list(np.random.randint(0, 2, self._array_len)))

    def change_cell(self, x: int, y: int) -> None:
        self._dll.change_cell_value(self.array, x, y, self.width, self.height)
