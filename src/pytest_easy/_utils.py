from typing import Union


def read_image_as_numpy(
    path: str,
    do_read_as_rgba: bool = True
) -> 'np.ndarray':
    """
    *Optional dependency `numpy` (imported as `numpy`) required*
    
    *Optional dependency `pillow` (imported as `PIL`) required*

    Read an image from a file and transform it into a
    numpy array. It will force the 'size' if provided,
    or leave the original one if it is None.
    """
    from PIL import Image
    import numpy as np

    mode = (
        'RGBA'
        if do_read_as_rgba else
        'RGB'
    )

    with Image.open(path) as img:
        img = img.convert(mode)
        np_img = np.array(img, dtype = np.uint8)

    return np_img