"""Decorator for logging purposes"""
import functools
import time
from inspect import getfullargspec
import textwrap

__AUTHOR__ = "Oscar Lundberg"


def return_wrapper(prefix):
    """Create wrapper object
    
    :param prefix(str): Which prefix to use for the indentation
    :returns wrap: Wrapper object, use wrap.fill(text) to wrap text 
    """
    wrap = textwrap.TextWrapper(initial_indent=prefix,
                                width=90,
                                subsequent_indent=" "*len(prefix))
    return wrap


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
        print(wrap.fill(f"{args} {kwargs}") + "\n")


        t_start = time.clock()
        output = func(*args, **kwargs)
        t_diff = time.clock()-t_start  # Time inside the function

        wrap = return_wrapper("    Output: ")
        print(wrap.fill(f"{output}"))

        print(f"##### Log {func.__name__} END (Time: {t_diff:.3} s) #####\n")

        return output

    return wrapper



if __name__ == '__main__':
    pass
