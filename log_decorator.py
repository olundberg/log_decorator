"""Decorator for logging purposes"""
import numpy as np
import functools
import time
from inspect import getfullargspec
import textwrap

__AUTHOR__ = "Oscar Lundberg"

def return_wrapper(prefix):
    """Text wrapper to indent text

    :param prefix: Prefix for the first line, e.g. "Input: "
    :returns: Wrapper object. wrap.fill(text) where text is the text to be filled
    """
    wrap = textwrap.TextWrapper(initial_indent=prefix,
                                width=90,
                                subsequent_indent=" "*len(prefix))
    return wrap

def modify_args(args):
    """Instead of printing numpy array matrix, print the shape

    If one of the arguments is a type(nd.array), print the shape of the object
    instead of all the elements for convenience.

    :param args: list with the arguments
    :returns args_mod:
    """
    if isinstance(args, list) or isinstance(args, tuple):
        args_mod = []
        for arg in args:
            if type(arg) is np.ndarray:
                if arg.size > 10:
                    args_mod.append(f"nd.array.shape: {arg.shape}")
                else:
                    args_mod.append(arg)
            elif type(arg) is list and len(arg) > 10:
                args_mod.append(arg[:10])
            else:
                args_mod.append(arg)
    else:
        if type(args) is np.ndarray:
            if args.size > 10:
                args_mod = f"nd.array.shape: {args.shape}"
            else:
                args_mod = args
        elif type(args) is list and len(args) > 10:
            args_mod = args[:10]
        else:
            args_mod = args

    return args_mod

def log_decorator(func):
    """Decorator for logging (printing) functions.

    This is a general prupose decorator that only maps the input -> output.

    More specific decorators/debugs might be needed inside some functions/methods

    :param func: The functions to be wrapped
    :returns wrapper: The wrapper which now has wrapped the function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper to print input and outputs of functions

        :param *args:
        :param **kwargs:
        """
        argspec = getfullargspec(func)

        print(f"\n##### @Log {func.__name__} #####")

        wrap = return_wrapper("    Args: ")
        print(wrap.fill(f"{argspec.args}"))

        wrap = return_wrapper("    Default Args: ")
        print(wrap.fill(f"{argspec.defaults}") + "\n")

        wrap = return_wrapper("    Input: ")
        print(wrap.fill(f"{modify_args(args)} {kwargs}") + "\n")


        t_start = time.clock()
        output = func(*args, **kwargs)
        t_diff = time.clock()-t_start  # Time inside the function

        wrap = return_wrapper("    Output: ")
        print(wrap.fill(f"{modify_args(output)}"))

        print(f"##### Log {func.__name__} END (Time: {t_diff:.3} s) #####\n")

        return output

    return wrapper



if __name__ == '__main__':

    @log_decorator
    def add(a,b):
        """Just to test decorator"""
        return a + b, a, b

    @log_decorator
    def test(a):

        @log_decorator
        def test_2(b):
            return b
        b = test_2(a)
        dict_ = dict()
        dict_["a"] = 1
        return dict_

    @log_decorator
    def test_matrix(a, b=0):
        return np.zeros((3, 3, 3))

    add(3,5)
    test(1)
    print(type(np.zeros((2,2,2))))
    test_matrix(np.zeros((2,2,2)))
