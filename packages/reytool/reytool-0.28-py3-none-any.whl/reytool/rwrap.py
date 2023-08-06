# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
══════════════════════════════
@Time    : 2022-12-05 14:12:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's decorators
══════════════════════════════
"""


import time
from varname import nameof
from threading import Thread
from functools import wraps as functools_wraps

from .rbasic import exc, check_parm
from .rtext import print_frame
from .rtype import Function, Method
from .rtime import now


def wrap_frame(func: "Function | Method") -> "Function":
    """
    Decorative frame.

    Parameters
    ----------
    func : Function or Method
        Decorator function.

    Retuens
    -------
    Function
        Decorator after decoration.

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

    check_parm(func, Function, Method)

    @functools_wraps(func)
    def wrap(_func: "Function | Method", *args: "object", _execute: "bool"=False, **kwargs: "object") -> "Function | object":
        """
        Decorative shell.
        """
        
        check_parm(_execute, bool)

        if _execute or args or kwargs:
            func_ret = func(_func, *args, **kwargs)
            return func_ret
        
        else:
            @functools_wraps(_func)
            def wrap_sub(*args: "object", **kwargs: "object") -> "object":
                """
                Decorative sub shell.
                """

                func_ret = func(_func, *args, **kwargs)
                return func_ret
            return wrap_sub
    return wrap

def wraps(*wrap_funcs: "Function | Method") -> "Function":
    """
    Batch decorate.

    parameters
    ----------
    wrap_funcs : Function or Method
        Decorator function.

    Retuens
    -------
    Function
        Function after decoration.

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

    check_parm(wrap_funcs, Function, Method, check_array=True)

    def func(): ...
    for wrap_func in wrap_funcs:
        
        @functools_wraps(func)
        def wrap(func: "Function | Method") -> "Function":
            """
            Decorative shell
            """

            @functools_wraps(func)
            def wrap_sub(*args: "object", **kwargs: "object") -> "object":
                """
                Decorative sub shell
                """

                func_ret = wrap_func(func, *args, _execute=True, **kwargs)
                return func_ret
            return wrap_sub
        func = wrap
    return wrap

@wrap_frame
def runtime(func: "Function | Method", *args: "object", **kwargs: "object") -> "object":
    """
    Print run time of the function.

    Parameters
    ----------
    func : Function or Method
        Function to be decorated.
    *args : object
        Position parameter of input parameter decorated function.
    *kwargs : object
        Keyword parameter of input parameter decorated function.

    Returns
    -------
    object
        Return of decorated function.
    """

    check_parm(func, Function, Method)

    start_datetime = now()
    start_timestamp = now("timestamp")
    func_ret = func(*args, **kwargs)
    end_datatime = now()
    end_timestamp = now("timestamp")
    spend_timestamp = end_timestamp - start_timestamp
    spend_second = round(spend_timestamp, 2)
    print_content = ["Start: %s -> Spend: %ss -> End: %s" % (start_datetime, spend_second, end_datatime)]
    title = func.__name__
    print_frame(print_content, title)
    return func_ret

@wrap_frame
def start_thread(func: "Function | Method", *args: "object", _daemon: "bool"=True, **kwargs: "object") -> "None":
    """
    Function start in thread.

    Parameters
    ----------
    func : Function or Method
        Function to be decorated.
    *args : object
        Position parameter of input parameter decorated function.
    _daemon : bool
        Whether it is a daemon thread.
    *kwargs : object
        Keyword parameter of input parameter decorated function.
    """

    check_parm(func, Function, Method)
    check_parm(_daemon, bool)

    thread_name = "%s_%s" % (func.__name__, str(int(time.time() * 1000)))
    thread = Thread(target=func, name=thread_name, args=args, kwargs=kwargs)
    thread.daemon = _daemon
    thread.start()

def try_exc(
    func: "Function | Method",
    *args: "object",
    **kwargs: "object"
) -> "object | None":
    """
    Execute function with 'try' syntax and print error information.

    Parameters
    ----------
    func : Function or Method
        Function to be decorated.
    *args : object
        Position parameter of input parameter decorated function.
    *kwargs : object
        Keyword parameter of input parameter decorated function.

    Returns
    -------
    object or None
        Return of decorated function or no return.
    """
    
    check_parm(func, Function, Method)

    try:
        func_ret = func(*args, **kwargs)
        return func_ret
    except:
        func_name = func.__name__
        exc(func_name)