import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import os
from montage.utilities import loop_check


def montager(name_array, dir):
    """Easy use montage creator, by pasing a list of picture file names, and the containing directory.

        :param dir: directory containing the images you want to work with
        :param name_array: list of names with the right repetition for required dimensions
            i.e.: [['one.jpeg', 'two.jpeg', 'three.jpeg'],
                   ['four.jpeg, 'five.jpeg', three.jpeg'],
                   ['six.jpeg', 'six.jpeg', 'seven.jpeg']]
                
                    This will result in a 3x3 matrix of images where image 'three' is 2 row high
                    and 1 coloumn wide. While 'six' is 2 coloumn wide, but 1 row high."""

    if not isinstance(dir, str):
        raise TypeError('dir argument must be a string containing the path to target directory.')

    if not os.path.exists(dir):
        raise FileExistsError(f'Path of <{dir}> does not exist or unavailable!')

    name_array = loop_check(name_array=name_array)

    fig, ax = plt.subplot_mosaic(name_array, figsize=(20, 20), dpi=150)
    plt.tight_layout()
    for pic in name_array.flat:
        # Simple loop through all the values which get input into the mosaic
        if pic != '.':
            file = dir + pic
            print(f'Reading in {file}')
            imgplt = img.imread(file)
            iplot = ax[pic].imshow(imgplt)
            ax[pic].set_xticks([])
            ax[pic].set_yticks([])
    return fig