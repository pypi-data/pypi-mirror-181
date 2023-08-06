# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
══════════════════════════════
@Time    : 2022-12-11 23:25:36
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's regular methods
══════════════════════════════
"""


import re
from re import RegexFlag

from .rbasic import check_parm


def re_search(pattern: "str", text: "str", method: "RegexFlag"=None) -> "str | tuple | None":
    """
    Regular matching text.

    Parameters
    ----------
    pattern : str
        Regular pattern.
    text : str
        Match text.

    Returns
    -------
    str or tuple [str or None, ...] or None
        Matching result.

        - When match to and not use group, then return string.
        - When match to and use group, then return tuple with value string or None.
        - When no match, then return none.
    """

    check_parm(pattern, str)
    check_parm(text, str)
    check_parm(method, RegexFlag, None)

    obj_re = re.search(pattern, text)
    if obj_re != None:
        result = obj_re.groups()
        if result == ():
            result = obj_re[0]
        return result

def res(text: "str", *patterns: "str", return_first: "bool"=True) -> "str | tuple | None":
    """
    Batch regular matching text.

    Parameters
    ----------
    text : str
        Match text.
    *pattern : str
        Regular pattern.
    return_first : bool
        Whether return first successful match.

    Returns
    -------
    str or tuple [str or None, ...] or None
        Matching result.

        - When match to and not use group, then return string.
        - When match to and use group, then return tuple with value string or None.
        - When no match, then return none.
    """

    check_parm(text, str)
    check_parm(patterns, str, check_array=True)
    check_parm(return_first, bool)

    if return_first:
        for pattern in patterns:
            result = re_search(pattern, text)
            if result != None:
                return result
    else:
        result = [re_search(pattern, text) for pattern in patterns]
        return result