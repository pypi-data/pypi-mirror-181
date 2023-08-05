# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
══════════════════════════════
@Time    : 2022/12/05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey"s basic methods
══════════════════════════════
'''


from varname import nameof


def check_parm(value: "object", *args: "object", check_array: "bool"=False, print_var_name: "bool"=True) -> "None":
    """
    Check the content or type of the value.

    Parametes
    ---------
    value : object
        Check object.
    *args : object
        Correct range, can be type.
    check_array : bool
        Whether check element in value.
    print_var_name : bool
        When the check fail, whether print value variable name.
    """

    if check_array:
        for _value in value:
            check_parm(_value, *args, print_var_name=False)
    else:
        if type(value) in args:
            return
        args_id = [id(element) for element in args]
        if id(value) in args_id:
            return
        if print_var_name:
            try:
                var_name = nameof(value, frame=2)
                var_name = " '%s'" % var_name
            except:
                var_name = ""
        else:
            var_name = ""
        correct_range_str = ", ".join([repr(element) for element in args])
        error_text = "parameter%s the value content or type must in [%s], now: %s" % (var_name, correct_range_str, repr(value))
        error(error_text, ValueError)
    
def check_parm_least_one(*args: "object") -> "None":
    """
    Check that at least one of multiple values is not None.

    Parameters
    ----------
    *args : object
        Check values.
    """

    for value in args:
        if value != None:
            return
    try:
        vars_name = nameof(*args, frame=2)
    except:
        vars_name = None
    if vars_name:
        vars_name_str = " " + " and ".join(["\"%s\"" % var_name for var_name in vars_name])
    else:
        vars_name_str = ""
    error_text = "at least one of parameters%s is not None" % vars_name_str
    error(error_text, ValueError)

def check_parm_only_one(*args: "object") -> "None":
    """
    Check that at most one of multiple values is not None.

    Parameters
    ----------
    *args : object
        Check values.
    """

    none_count = 0
    for value in args:
        if value != None:
            none_count += 1
    if none_count > 1:
        try:
            vars_name = nameof(*args, frame=2)
        except:
            vars_name = None
        if vars_name:
            vars_name_str = " " + " and ".join(["\"%s\"" % var_name for var_name in vars_name])
        else:
            vars_name_str = ""
        error_text = "at most one of parameters%s is not None" % vars_name_str
        error(error_text, ValueError)

def is_iterable(obj: "object", exclude_type: "list"=[str, bytes]) -> "bool":
    """
    Judge whether it is iterable.

    Parameters
    ----------
    obj : object
        Judge object.
    exclude_type : list[type, ...]
        Exclusion type.

    Returns
    -------
    bool
        Judgment result.
    """

    check_parm(exclude_type, list)

    obj_type = type(obj)
    if obj_type in exclude_type:
        return False
    try:
        obj_dir = obj.__dir__()
    except TypeError:
        return False
    if "__iter__" in obj_dir:
        return True
    else:
        return False

def is_number_str(text: "str", return_value: "bool"=False) -> "bool | int | float":
    """
    Judge whether it is number string.

    Parameters
    ----------
    text : str
        Judge text.
    return_value : bool
        Whether return value.
    
    Returns
    -------
    bool or int or float
        Judgment result or transformed value.
    """

    check_parm(text, str)
    check_parm(return_value, bool)

    try:
        if "." in text:
            number = float(text)
        else:
            number = int(text)
    except ValueError:
        return False
    if return_value:
        return number
    return True

def get_first_notnull(*args: "object", default: "object"=None, exclude: "list"=[]) -> object:
    """
    Get first notnull element.
    """

    check_parm(exclude, list)
    
    for element in args:
        if element not in [None, *exclude]:
            return element
    return default

def error(throw: "object"=True, info: "object"=None, error_type: "BaseException"= AssertionError) -> "object":
    """
    Throw error or return information.

    Parameters
    ----------
    judge : object
        whether throw error.
    info : object
        Error information or return information.
    error_type : BaseException
        Error type.

    Returns
    -------
    object
        Throw error or return information.
    """

    if throw:
        if info == None:
            error = error_type
        else:
            error = error_type(info)
        raise error
    else:
        return info