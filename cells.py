import numpy as np
import ctypes


class Cells:
    def __init__(self, cells_width: int = 100, cells_height: int = 100, random: bool = True):
        if random:
            array = np.random.randint(0, 2, cells_width * cells_height)
        else:
            array = np.zeros(cells_width * cells_height, dtype=np.int8)

        self.width = cells_width
        self.height = cells_height
        self.array = (ctypes.c_uint8 * (cells_width * cells_height))(*list(array))

        self.dll = ctypes.CDLL('c_functions/lib.so')
        self.dll.calculate_next_generation.argtypes = [ctypes.c_uint8 * len(self.array), ctypes.c_int, ctypes.c_int]

    def calculate_next_generation(self) -> None:
        self.dll.calculate_next_generation(self.array, self.width, self.height)
