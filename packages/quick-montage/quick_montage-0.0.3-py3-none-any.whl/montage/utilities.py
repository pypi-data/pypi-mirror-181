import numpy as np


def format_check(
    file: str,
    supported_list: list = ['.jpeg', '.jpg', '.png', '.tiff', '.gif']    
):
    """Function to check if the file is a supported format."""

    if not isinstance(file, str):
        raise TypeError('file is of the wrong format')

    if not isinstance(supported_list, (list, np.ndarray)):
        raise TypeError('Given support list is of thw wrong type, must be a list')

    check_arr = [True if isinstance(x, str) else False for x in supported_list]
    if False in check_arr:
        raise ValueError('supported list contains elements of the wrong format, all must be a string')

    check = None
    for ext in supported_list:        
        if ext in file:
            return True
        else:
            check = False

    if check is False:
        return False


def loop_check(
    name_array: list,
    supported_list: list = ['.jpeg', '.jpg', '.png', '.tiff', '.gif']    
):
    """Function loops through the list of given strings
    and filters out all the ones that are not supported
    by replacing them with blank space on the mosaic"""
    if not isinstance(name_array, (list, np.ndarray, tuple)):
        raise TypeError('Wrong type was passed, must be a list, or a numpy.ndarray object')

    new_array = []
    shape = np.shape(name_array)
    for pic in np.asarray(name_array).flatten():
        if format_check(pic, supported_list):
            new_array.append(pic)
        else:
            new_array.append('.')

    return np.asarray(new_array).reshape(shape)