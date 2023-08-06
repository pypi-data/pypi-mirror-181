from pathlib import Path
import numpy as np
import cv2
from ps_utils.exceptions import PathNotExistsError, InvalidSheetSizeError
from ps_utils.settings import SHEET_SIZES_IN_PIXELS


class Image():

    def __init__(self, path):
        self._path = str(path)
        self._test_path()
        self.array = cv2.imread(self._path)

    def _test_path(self):
        if not Path(self._path).exists():
            raise PathNotExistsError()


class Sheet():

    def __init__(self, size='A4'):
        self._size = str(size).upper()
        self._test_sheet_size()
        self.width = SHEET_SIZES_IN_PIXELS[self._size]['width']
        self.height = SHEET_SIZES_IN_PIXELS[self._size]['height']
        self.array = np.full((self.height, self.width, 3), 255)

    def _test_sheet_size(self):
        if not SHEET_SIZES_IN_PIXELS.get(self._size):
            raise InvalidSheetSizeError()
