# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
══════════════════════════════
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's parameters directory type
══════════════════════════════
"""


from .rbasic import check_parm, is_iterable


class RParm(object):
    """
    Rey's parameters directory type.

    Methods
    -------
    attribute : parms, default
    syntax : [index/ slice], for, in/ not in
    enter parameter : len
    symbol : +(l/ r), -(l/ r), &(l/ r), +=, -=, &=
    function : items, keys, values, get, pop
    """
    
    def __init__(self, *parms: "dict", default: "object | str"="error") -> "None":
        """
        Set parameters directory attribute.

        Parameters
        ----------
        *parms : dict
            Parameters
        default : object or str {'error'}
            Default method when index fails.

            - object : Return this value.
            - 'error' : Throw error.
        """

        check_parm(parms, dict, check_array=True)

        parms = {}
        for parm in parms:
            parms.update(parm)
        self.parms = parms
        self.default = default
    
    def __call__(self, *keys: "object") -> "object":
        """
        Indexes key value pair.
        """

        if keys == ():
            ret = self.parms
        else:
            ret = {key: self.parms[key] for key in keys}
        return ret

    def __getattr__(self, key: "object") -> "object":
        """
        Index value.
        """

        value = self.parms[key]
        return value

    def __getitem__(self, indexes: "object | tuple") -> object:
        """
        Batch indexing directory values.
        """

        if type(indexes) == tuple:
            if self.default == "error":
                vals = [self.parms[key] for key in indexes]
            else:
                vals = [self.parms.get(key, self.default) for key in indexes]
        else:
            if self.default == "error":
                vals = self.parms[indexes]
            else:
                vals = self.parms.get(indexes, self.default)
        return vals

    def __setitem__(self, key: "object", value: "object") -> "None":
        """
        Create or modify key value pair.
        """

        self.parms[key] = value
    
    def __iter__(self) -> iter:
        """
        Return iterable directory keys.
        """

        return self.keys

    def __contains__(self, key: "object") -> "bool":
        """
        Judge contain.
        """

        judge = key in self.parms
        return judge

    def __len__(self) -> "int":
        """
        Return parameters directory length.
        """
        return self.len

    def __add__(self, parms: "dict") -> "dict":
        """
        Union directory.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.parms, **parms}
        return parms
    
    def __radd__(self, parms: "dict") -> "dict":
        """
        Union directory right.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**parms, **self.parms}
        return parms

    def __iadd__(self, parms: "dict") -> object:
        """
        Union directory and definition.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.parms, **parms}
        self.parms = parms
        return self

    def __sub__(self, parms: "iter") -> "dict":
        """
        Difference directory.
        """

        main_set = set(self.parms)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.parms[key] for key in diff_set}
        return parms

    def __rsub__(self, parms: "dict") -> "dict":
        """
        Difference directory right.
        """

        check_parm(parms, dict)

        main_set = set(parms)
        sub_set = set(self.parms)
        diff_set = main_set - sub_set
        parms = {key: parms[key] for key in diff_set}
        return parms

    def __isub__(self, parms: "dict") -> object:
        """
        Difference directory and definition.
        """

        main_set = set(self.parms)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.parms[key] for key in diff_set}
        self.parms = parms
        return self

    def __and__(self, parms: "dict") -> "dict":
        """
        Intersection directory.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.parms)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.parms[key] for key in inte_set}
        return parms

    def __rand__(self, parms: "dict") -> "dict":
        """
        Intersection directory right.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(parms)
        sub_set = set(self.parms)
        inte_set = main_set & sub_set
        parms = {key: parms[key] for key in inte_set}
        return parms

    def __iand__(self, parms: "dict") -> "dict":
        """
        Intersection directory and definition.
        """

        check_parm(parms, dict)

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.parms)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.parms[key] for key in inte_set}
        self.parms = parms
        return self

    def items(self) -> iter:
        """
        Get directory all keys and values.
        """

        items = self.parms.items()
        return items

    def keys(self) -> iter:
        """
        Get directory all keys.
        """

        keys = self.parms.keys()
        return keys

    def values(self) -> iter:
        """
        Get directory all values.
        """

        values = self.parms.values()
        return values

    def get(self, keys: "object | iter", default: "object"=None) -> "dict":
        """
        Batch get directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.parms.get(key, default) for key in keys]
        else:
            vals = self.parms.get(keys, default)
        return vals

    def pop(self, keys: "object | iter", default: "object"=None) -> "dict":
        """
        Batch pop directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.parms.pop(key, default) for key in keys]
        else:
            vals = self.parms.pop(keys, default)
        return vals