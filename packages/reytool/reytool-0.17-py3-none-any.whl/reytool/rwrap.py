# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
══════════════════════════════
@Time    : 2022/12/05 14:12:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's decorators
══════════════════════════════
'''


import time
from threading import Thread

from .rbasic import check_parm
from .rtext import print_frame
from .rtype import function, method
from .rtime import now


def wrap_frame(func: "function | method") -> "function":
    """
    Decorative frame.

    Parameters
    ----------
    func : Function or method

    Retuens
    -------
    function
        After decoration.

    Examples
    --------
    Decoration function method one.

    >>> @wrap_func
    >>> def func(): ...
    >>> func_ret = func()
    
    Decoration function method two.

    >>> def func(): ...
    >>> func = wrap_func(func)
    >>> func_ret = func()
    
    Decoration function method three.

    >>> def func(): ...
    >>> func_ret = wrap_func(func, parameter, ...)
    """

    check_parm(func, function, method)

    def wrap(_func: "function | method", *args: "object", **kwargs: "object") -> "function | object":
        """
        Decorative shell.
        """
        
        if args or kwargs:
            func_ret = func(_func, *args, **kwargs)
            return func_ret
        
        else:
            def wrap_sub(*args: "object", **kwargs: "object") -> "object":
                """
                Decorative sub shell.
                """

                func_ret = func(_func, *args, **kwargs)
                return func_ret
            return wrap_sub
    return wrap

def wraps(*wrap_funcs: "function | method") -> "function":
    """
    Batch decorator.

    parameters
    ----------
    wrap_funcs : Decorator

    Retuens
    -------
    function
        After decoration.

    Examples
    --------
    Decoration function.

    >>> @wraps(print_funtime, state_thread)
    >>> def func(): ...
    >>> func_ret = func()
    
        Same up and down

    >>> @print_funtime
    >>> @state_thread
    >>> def func(): ...
    >>> func_ret = func()

        Same up and down

    >>> def func(): ...
    >>> func = print_funtime(func)
    >>> func = state_thread(func)
    >>> func_ret = func()
    """

    check_parm(wrap_funcs, function, method, check_array=True)

    for wrap_func in wrap_funcs:
        def wrap(func: "function | method") -> "function":
            """
            Decorative shell
            """

            def wrap_sub(*args: "object", **kwargs: "object") -> "object":
                """
                Decorative sub shell
                """

                func_ret = wrap_func(func, *args, **kwargs)
                return func_ret
            return wrap_sub
        func = wrap
    return wrap

@wrap_frame
def print_runtime(func: "function | method", *args: "object", **kwargs: "object") -> "function":
    """
    Print run time of the function.
    """

    check_parm(func, function, method)

    start_datetime = now()
    start_timestamp = time.time()
    func_ret = func(*args, **kwargs)
    end_datatime = now()
    end_timestamp = time.time()
    spend_timestamp = end_timestamp - start_timestamp
    spend_second = int(spend_timestamp)
    print_content = ["Start: %s -> Spend: %ss -> End: %s" % (start_datetime, spend_second, end_datatime)]
    title = func.__name__
    print_frame(print_content, title)
    return func_ret

@wrap_frame
def start_thread(func: "function | method", *args: "object", daemon: "bool"=True, **kwargs: "object") -> "None":
    """
    Function start in thread.
    """

    check_parm(func, function, method)
    check_parm(daemon, bool)

    thread_name = "%s_%s" % (func.__name__, str(int(time.time() * 1000)))
    thread = Thread(target=func, name=thread_name, args=args, kwargs=kwargs)
    thread.daemon = daemon
    thread.start()