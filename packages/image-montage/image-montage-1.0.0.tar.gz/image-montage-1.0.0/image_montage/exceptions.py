class PathNotExistsError(Exception):

    def __init__(self):
        super().__init__('This path not exists.')


class InvalidSheetSizeError(Exception):

    def __init__(self):
        super().__init__('This sheet size is invalid.')


class InvalidImagesWidthError(Exception):

    def __init__(self):
        super().__init__('This images width is invalid.')


class InvalidImagesHeightError(Exception):

    def __init__(self):
        super().__init__('This images height is invalid.')


class IsNotInstanceOfSheetError(Exception):

    def __init__(self):
        super().__init__('self.sheet must be an instance of Sheet.')


class InvalidImageAmount(Exception):

    def __init__(self):
        super().__init__('Invalid image amount.')
