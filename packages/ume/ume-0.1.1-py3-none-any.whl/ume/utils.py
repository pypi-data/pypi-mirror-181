from functools import wraps
from io import BytesIO
from urllib.request import urlopen

import numpy as np
from PIL import Image


class classproperty:  # NOQA
    def __init__(self, method=None):
        self.method = method

    def __get__(self, instance, cls=None):
        return self.method(cls)

    def getter(self, method):
        self.method = method
        return self


def returns(value):
    def function(*args, **kwargs):
        return value

    return function


def with_parameters(**kw):
    """
    # Adds flag-like parameters accessible from the function variable to use inside the function

    @with_parameters(image="image", pdf="pdf", csv="csv")
    def process_file(file, file_type):
        if file_type == process_file.image:
            ...
        elif file_type == process_file.pdf:
            ...
        elif file_type == process_file.csv:
            ...
        else:
            ...

    process_file(file, file_type=process_file.image)

    # Also optionally it allows you to pass down the parameters into a new function

    @process_file.apply_params
    def process_input(file, file_type):
        # Now you can use the same parameters from the process_file function
        if file_type == process_input.image:
            ...
        elif file_type == process_input.pdf:
            ...
        elif file_type == process_input.csv:
            ...
        else:
            ...

    # You can also access the parameters dictionary with

    process_input.params_dict

    """
    def decorator(f):
        for key, value in kw.items():
            setattr(f, key, value)
        f.params_dict = kw
        f.apply_params = with_parameters(**f.params_dict)
        return f
    return decorator


@with_parameters(URL="URL", PATH="PATH", PIL_IMAGE="PIL_IMAGE")
def get_pil_image(source, input_type):
    if input_type == get_pil_image.URL:
        image = Image.open(BytesIO(urlopen(source).read()))
    elif input_type == get_pil_image.PATH:
        image = Image.open(source)
    elif input_type == get_pil_image.PIL_IMAGE:
        image = source
    else:
        raise ValueError(
            f"Invalid input type: '{input_type}', please provide an input_type keyword argument, possible options:\n"
            f"{get_pil_image.__name__}.{get_pil_image.URL},\n"
            f"{get_pil_image.__name__}.{get_pil_image.PATH},\n"
            f"{get_pil_image.__name__}.{get_pil_image.PIL_IMAGE}"
        )
    return image


class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    @classmethod
    def from_data(cls, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = cls.from_data(value)
        return cls(**data)


def sewar_patcher(sewar_metric):
    # This is a wrapper around sewar metric functions to make them work with urls, paths and PIL images
    # instead of numpy arrays.
    @wraps(sewar_metric)
    @get_pil_image.apply_params
    def wrapper(gt, p, input_type, *args, **kwargs):
        gt = np.asarray(get_pil_image(gt, input_type=input_type))
        p = np.asarray(get_pil_image(p, input_type=input_type))
        return sewar_metric(gt, p, *args, **kwargs)

    return wrapper


def image_hash_patcher(image_hasher):
    # This is a wrapper around image hash functions to make them work with urls, paths and PIL images
    # instead of just PIL images.
    @wraps(image_hasher)
    @get_pil_image.apply_params
    def wrapper(image, input_type, *args, **kwargs):
        image = get_pil_image(image, input_type=input_type)
        return image_hasher(image, *args, **kwargs)

    return wrapper


