import cv2
from pathlib import Path
from ps_utils.conversors import cm2px
from ps_utils.objects import Sheet
from ps_utils import exceptions


class MontageMaker():

    def __init__(self, **kwargs):
        self._images = []
        self._sheet = kwargs.get('sheet', Sheet())
        self._test_sheet()
        self._images_width = cm2px(kwargs.get('images_width', 6.5))
        self._test_images_width()
        self._images_height = cm2px(kwargs.get('images_height', 6.5))
        self._test_images_height()
        self.current_number_of_images = 0
        self._update_total_number_of_images()
        self._update_gap()
        self._download_directory = Path(
            kwargs.get('download_directory', Path.home() / 'Downloads')
        )
        self._test_download_directory()

    @property
    def sheet(self):
        return self._sheet

    @property
    def images_width(self):
        return self._images_width

    @property
    def images_height(self):
        return self._images_height

    @property
    def download_directory(self):
        return self._download_directory

    @sheet.setter
    def sheet(self, value):
        self._sheet = value
        self._test_sheet()
        self._update_total_number_of_images()
        self._update_gap()

    @images_width.setter
    def images_width(self, value):
        self._images_width = cm2px(value)
        self._test_images_width()
        self._update_total_number_of_images()
        self._update_gap()
        self._images = []

    @images_height.setter
    def images_height(self, value):
        self._images_height = cm2px(value)
        self._test_images_height()
        self._update_total_number_of_images()
        self._update_gap()
        self._images = []

    @download_directory.setter
    def download_directory(self, value):
        self._download_directory = Path(value)
        self._test_download_directory()

    def _update_total_number_of_images(self):
        self._number_of_columns = self.sheet.width // self.images_width
        self._number_of_rows = self.sheet.height // self.images_height
        self.total_number_of_images = (
            self._number_of_columns * self._number_of_rows
        )

    def _update_gap(self):
        self._update_column_gap()
        self._update_row_gap()

    def _update_column_gap(self):
        total_gap = (
            self.sheet.width - self.images_width * self._number_of_columns
        )
        number_of_gaps = self._number_of_columns - 1
        self._column_gap = total_gap // number_of_gaps

    def _update_row_gap(self):
        total_gap = (
            self.sheet.height - self.images_height * self._number_of_rows
        )
        number_of_gaps = self._number_of_rows - 1
        self._row_gap = total_gap // number_of_gaps

    def add_image(self, image, amount):
        image.amount = int(amount)
        image.array = cv2.resize(
            image.array, (self.images_width, self.images_height)
        )
        self._images.append(image)
        self._test_image_amount()
        self.current_number_of_images += int(amount)

    def make_montage(self):
        self._current_column = 0
        self._current_row = 0
        self._place_images()
        self._write_final_image()
        self._images = []

    def _place_images(self):
        for image in self._images:
            self._place_image(image)

    def _place_image(self, image):
        while image.amount > 0:
            y1 = (
                self._current_row * self.images_height
                + self._current_row * self._row_gap
            )
            y2 = y1 + self.images_height
            x1 = (
                self._current_column * self.images_width
                + self._current_column * self._column_gap
            )
            x2 = x1 + self.images_width
            self.sheet.array[y1:y2, x1:x2] = image.array
            self._change_position()
            image.amount -= 1

    def _change_position(self):
        if self._current_column == self._number_of_columns - 1:
            self._current_column = 0
            self._current_row += 1
        elif self._current_column != self._number_of_columns - 1:
            self._current_column += 1

    def _write_final_image(self):
        cv2.imwrite(
            str(self.download_directory / 'final_image.jpg'),
            self.sheet.array,
        )

    def _test_sheet(self):
        if not isinstance(self.sheet, Sheet):
            raise exceptions.IsNotInstanceOfSheetError()

    def _test_images_width(self):
        if self.images_width > self.sheet.width or self.images_width <= 0:
            raise exceptions.InvalidImagesWidthError()

    def _test_images_height(self):
        if self.images_height > self.sheet.height or self.images_height <= 0:
            raise exceptions.InvalidImagesHeightError()

    def _test_download_directory(self):
        if not self.download_directory.exists():
            raise exceptions.PathNotExistsError()

    def _test_image_amount(self):
        total_amount = sum([image.amount for image in self._images])
        if total_amount > self.total_number_of_images:
            self._images.pop()
            raise exceptions.InvalidImageAmount()
