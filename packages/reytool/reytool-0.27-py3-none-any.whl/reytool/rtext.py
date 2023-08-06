# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
══════════════════════════════
@Time    : 2022-12-08 13:18:24
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's print methods
══════════════════════════════
"""


import pprint
from urwid import old_str_util
from varname import nameof

from .rbasic import check_parm, is_iterable, error, convert_type, is_iterable


def pformat(content: "object", width: "int"=100) -> "str":
    """
    Based on module pprint.pformat, modify the chinese width judgment.
    """

    def _format(_self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if objid in context:
            stream.write(pprint._recursion(object))
            _self._recursive = True
            _self._readable = False
            return
        rep = _self._repr(object, context, level)
        max_width = _self._width - indent - allowance
        width = get_width(rep)
        if width > max_width:
            p = _self._dispatch.get(type(object).__repr__, None)
            if p is not None:
                context[objid] = 1
                p(_self, object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            elif isinstance(object, dict):
                context[objid] = 1
                _self._pprint_dict(object, stream, indent, allowance,
                                context, level + 1)
                del context[objid]
                return
        stream.write(rep)

    pprint.PrettyPrinter._format = _format
    content_str = pprint.pformat(content, width=width, sort_dicts=False)
    return content_str

def split_text(text: "str", length: "int", by_width: "bool"=False) -> "list":
    """
    Split text by length or not greater than display width.
    """

    check_parm(text, str)
    check_parm(length, int)
    check_parm(by_width, bool)

    texts = []
    if by_width:
        str_group = []
        str_width = 0
        for char in text:
            char_width = get_width(char)
            str_width += char_width
            if str_width > length:
                string = "".join(str_group)
                texts.append(string)
                str_group = [char]
                str_width = char_width
            else:
                str_group.append(char)
        string = "".join(str_group)
        texts.append(string)
    else:
        test_len = len(text)
        split_n = test_len // length
        if test_len % length:
            split_n += 1
        for n in range(split_n):
            start_indxe = length * n
            end_index = length * (n + 1)
            text_group = text[start_indxe:end_index]
            texts.append(text_group)
    return texts

def get_width(text: "str") -> "int":
    """
    Get text display width.
    """

    check_parm(text, str)
    
    total_width = 0
    for char in text:
        char_unicode = ord(char)
        char_width = old_str_util.get_width(char_unicode)
        total_width += char_width
    return total_width

def get_info(data: "object", info: "dict"={"size": 0, "total": 0, "types": {}}, surface: "bool"=True) -> "dict":
    """
    Get data informationTrue.
    """

    check_parm(info, dict)
    check_parm(surface, bool)

    data_type = type(data)
    info["total"] += 1
    info["types"][data_type] = info["types"].get(data_type, 0) + 1
    if data_type == dict:
        for element in data.values():
            get_info(element, info, False)
    elif is_iterable(data):
        for element in data:
            get_info(element, info, False)
    else:
        info["size"] = info["size"] + 1
    if surface:
        sorted_func = lambda key: info["types"][key]
        sorted_key = sorted(info["types"], key=sorted_func, reverse=True)
        info["types"] = {key: info["types"][key] for key in sorted_key}
        return info

def fill_width(text: "str", char: "str", width: "int", align: "str"="right") -> "str":
    """
    Text fill character by display width.

    Parameters
    ----------
    text : str
        Fill text.
    char : str
        Fill character.
    width : width
        Fill width.
    align : str {'left', 'right', 'center'}
        Align orientation.

        - 'left' : Fill right, align left.
        - 'right' : Fill left, align right.
        - 'center': Fill both sides, align center.
    
    Returns
    -------
    str
        Text after fill.
    """

    check_parm(text, str)
    check_parm(char, str)
    check_parm(width, int)
    check_parm(align, str)

    if get_width(char) != 1:
        error("parameter char value error", ValueError)
    text_width = get_width(text)
    fill_width = width - text_width
    if fill_width > 0:
        if align == "left":
            new_text = "%s%s" % (char * fill_width, text)
        elif align == "right":
            new_text = "%s%s" % (text, char * fill_width)
        elif align == "center":
            fill_width_left = int(fill_width / 2)
            fill_width_right = fill_width - fill_width_left
            new_text = "%s%s%s" % (char * fill_width_left, text, char * fill_width_right)
        else:
            error("parameter align value error", ValueError)
    else:
        new_text = text
    return new_text

def print_frame(contents: "object | iter", title: "str"=None, width: "int"=100, full_frame: "bool"=True) -> "None":
    """
    Print contents and frame.

    Parameters
    ----------
    contents : iterator
        Print content or array of contents.
    title : str
        Print frame title.
    width : int
        Print frame width.
    full_frame : bool
        Whether print full frame, otherwise print half frame.

        - True : 
            ╔╡ title ╞╗
            ║Content n║
            ║ot can ex║
            ║ceed the ║
            ║frame.   ║
            ╚═════════╝
        - False :
            ╒╡ title ╞╕
            Content can exceed the frame.
            ╘═════════╛
    """

    check_parm(title, str, None)
    check_parm(width, int)
    check_parm(full_frame, bool)
    
    if is_iterable(contents):
        contents = convert_type(contents, list)
    else:
        contents = [contents]
    width -= 2
    _id = id("--")
    for index, block in enumerate(contents):
        if full_frame:
            if id(block) == _id:
                frame_split_line = "╠%s╣" % ("═" * width)
                contents[index] = frame_split_line
            else:
                try:
                    block_str = str(block)
                    rows_str = block_str.split("\n")
                    rows_str =[_row_str for row_str in rows_str for _row_str in split_text(row_str, width, True)]
                    rows_str = ["║%s║" % fill_width(string, " ", width) for string in rows_str]
                    block_str = "\n".join(rows_str)
                    contents[index] = block_str
                except:
                    full_frame = False
                    break
        else:
            if id(block) == _id:
                frame_split_line = "╞%s╡" % ("═" * width)
                contents[index] = frame_split_line
    if title == None or len(title) > width - 4:
        title = ""
    else:
        title = f"╡ {title} ╞"
    if full_frame:
        frame_top = "╔%s╗" % fill_width(title, "═", width, "center")
        frame_bottom = "╚%s╝" % ("═" * width)
    else:
        frame_top = "╒%s╕" % fill_width(title, "═", width, "center")
        frame_bottom = "╘%s╛" % ("═" * width)
    contents.insert(0, frame_top)
    contents.append(frame_bottom)
    for content in contents:
        print(content)

def rprint(
        *contents: "object",
        title: "str"=None,
        width: "int"=100,
        print_info: "bool"=False,
        format: "bool"=True,
        full_frame: "bool"=True,
    ) -> "None":
    """
    Print formatted contents and contents information.

    Parameters
    ----------
    *contents : object
        Print contents.
    title : str
        Print frame title.
    width : int
        Print frame width.
    print_info : bool
        Whether print contents information.
    format : bool
        Whether to print formatted contents, use the pformat function of pprint package.
    full_frame : bool
        Whether print full frame, otherwise print half frame.

        - True : 
            ╔╡ title ╞╗
            ║Content n║
            ║ot can ex║
            ║ceed the ║
            ║frame.   ║
            ╚═════════╝
        - False :
            ╒╡ title ╞╕
            Content can exceed the frame.
            ╘═════════╛
    """

    check_parm(width, int)
    check_parm(title, str, None)
    check_parm(print_info, bool)
    check_parm(format, bool)
    check_parm(full_frame, bool)

    datas = []
    for data in contents:
        datas.extend(["--", data])
    datas = datas[1:]
    if print_info:
        try:
            info = get_info(contents)
        except:
            info = False
        if info:
            if info["types"][tuple] == 1:
                del info["types"][tuple]
            else:
                info["types"][tuple] -= 1
            info["types"] = ["%s: %s" % (key.__name__, val) for key, val in info["types"].items()]
            info["types"] = ", ".join(info["types"])
            datas = [
                f"size: {info['size']}",
                f"total: {info['total'] - 1}",
                info["types"],
                "--",
                *datas
            ]
    if title == None:
        try:
            title = nameof(*contents, frame=2)
            if type(title) == tuple:
                title = " │ ".join(title)
            if title[:1] == "'":
                title = None
        except:
            title = None
    if format:
        _width = width - 2
        for index, data in enumerate(datas):
            try:
                if data != "--":
                    datas[index] = pformat(data, _width)
            except:
                pass
    print_frame(datas, title, width, full_frame)