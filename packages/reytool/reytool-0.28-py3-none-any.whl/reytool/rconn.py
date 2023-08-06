# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
══════════════════════════════
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's database connect type
══════════════════════════════
"""


import re
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import LegacyCursorResult
from sqlalchemy.sql.elements import TextClause
from types import MethodType

from .rbasic import check_parm, get_first_notnull, is_iterable, error
from .rtext import rprint
from .rtime import now, time_to_str


class RConn(object):
    """
    Rey's database connect type.
    """

    # Values to be converted to None.
    none_values = ["", " ", b"", [], (), {}, set()]
    
    def __init__(
        self,
        user: "str"=None,
        password: "str"=None,
        host: "str"=None,
        port: "str"=None,
        database: "str"=None,
        charset: "str"=None,
        only_once: "bool"=True,
        conn: "Engine | Connection"=None
    ) -> "None":
        """
        Set database connect parameters.
        """

        check_parm(user, str, None)
        check_parm(password, str, None)
        check_parm(host, str, None)
        check_parm(port, str, int, None)
        check_parm(database, str, None)
        check_parm(charset, str, None)
        check_parm(only_once, bool)
        check_parm(conn, Engine, Connection, None)

        if type(conn) == Connection:
            conn = conn.engine
        if type(conn) == Engine:
            user = get_first_notnull(user, conn.url.username)
            password = get_first_notnull(password, conn.url.password)
            host = get_first_notnull(host, conn.url.host)
            port = get_first_notnull(port, conn.url.port)
            database = get_first_notnull(database, conn.url.database)
            charset = get_first_notnull(charset, conn.url.query.get("charset"))
            conn = conn.connect(close_with_result=only_once)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.charset = charset
        self.only_once = only_once
        self.conn = conn
    
    def create_conn(
        self,
        user: "str"=None,
        password: "str"=None,
        host: "str"=None,
        port: "str | int"=None,
        database: "str"=None,
        charset: "str"=None,
        only_once: "bool"=True
    ) -> "Connection":
        """
        Get database connect engine.
        """

        check_parm(user, str, None)
        check_parm(password, str, None)
        check_parm(host, str, None)
        check_parm(port, str, int, None)
        check_parm(database, str, None)
        check_parm(charset, str, None)

        user = get_first_notnull(user, self.user)
        password = get_first_notnull(password, self.password)
        host = get_first_notnull(host, self.host)
        port = get_first_notnull(port, self.port)
        database = get_first_notnull(database, self.database)
        charset = get_first_notnull(charset, self.charset, default="utf8")
        only_once = get_first_notnull(only_once, self.only_once, default="utf8")

        if self.conn and [user, password, host, port, database] == [None] * 5:
            return self.conn

        check_parm(user, str)
        check_parm(password, str)
        check_parm(host, str)
        check_parm(port, str, int)
        check_parm(database, str)
        check_parm(only_once, bool)
        
        try:
            url = f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        except ModuleNotFoundError:
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        conn = engine.connect(close_with_result=only_once)
        if not self.conn and not only_once:
            self.conn = conn
        return conn
    
    def fill_sql_none(
        self,
        sql: "str | TextClause",
        parms: "dict | list",
        fill_field: "bool"=True,
        none_values: "list"=none_values
    ) -> "dict | list":
        """
        Fill missing parameters according to contents of sqlClause object of sqlalchemy module.

        Parameters
        ----------
        sql : str or sqlalchemy.sql.elements.TextClause
            SQL in sqlalchemy.text format or return of sqlalchemy.text.
        parms : dict or list [dict, ...]
            Parameters set for filling sqlalchemy.text.
        fill_field : bool
            Whether fill missing fields.
        none_values : list [object, ...]
            Values to be converted to None.

        Returns
        -------
        dict or list [dict, ...]
            Filled parameters.

            - When parameter parms is dict, then return dict.
            - When parameter parms is list [dict, ...], then return list [dict, ...].
        """

        check_parm(sql, str, TextClause)
        check_parm(parms, dict, list)
        check_parm(fill_field, bool)
        check_parm(none_values, list)

        if type(sql) == TextClause:
            sql = sql.text
        pattern = "(?<!\\\):(\w+)"
        sql_keys = re.findall(pattern, sql)
        if type(parms) == dict:
            for key in sql_keys:
                if fill_field:
                    val = parms.get(key)
                else:
                    val = parms[key]
                if val in none_values:
                    val = None
                parms[key] = val
        else:
            for parm in parms:
                for key in sql_keys:
                    if fill_field:
                        val = parm.get(key)
                    else:
                        val = parm[key]
                    if val in none_values:
                        val = None
                    parm[key] = val
        return parms

    def fetch_table(self, data: "LegacyCursorResult | iter", fields: "iter"=None) -> "list[dict,]":
        """
        Fetch SQL result to list[dict{field: value,},] table format.
        """

        if type(data) == LegacyCursorResult:
            if fields == None:
                fields = data.keys()
            table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
        else:
            data_fields_len = max([len(row) for row in data])
            if fields == None:
                data = [list(row) + [None] * (data_fields_len - len(row)) for row in data]
                field_range = range(data_fields_len)
                table = [dict(zip(field_range, [time_to_str(val) for val in row])) for row in data]
            else:
                field_len = len(fields)
                if data_fields_len > field_len:
                    fields += list(range(data_fields_len - field_len))
                data = [list(row) + [None] * (field_len - len(row)) for row in data]
                table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
        return table

    def fetch_df(self, data: "LegacyCursorResult | iter", fields: "iter"=None) -> "DataFrame":
        """
        Fetch SQL result to DataFrame object.
        """

        if type(data) == LegacyCursorResult:
            if fields == None:
                fields = data.keys()
            else:
                fields_len = len(data.keys())
                fields = fields[:fields_len]
            df = DataFrame(data, columns=fields)
        else:
            if fields == None:
                df = DataFrame(data)
            else:
                data_fields_len = max([len(row) for row in data])
                field_len = len(fields)
                if data_fields_len > field_len:
                    fields += list(range(data_fields_len - field_len))
                data = [list(row) + [None] * (field_len - len(row)) for row in data]
                df = DataFrame(data, columns=fields)
        return df

    def fetch_sql(self, data: "LegacyCursorResult | iter", fields: "iter"=None) -> "str":
        """
        Fetch SQL result to SQL sentence.
        """

        if type(data) == LegacyCursorResult:
            if fields == None:
                fields = data.keys()
            sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] for row in data]
        else:
            if fields == None:
                data_fields_len = max([len(row) for row in data])
                fields = ["field_%d" % i for i in range(data_fields_len)]
            sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] + ["NULL"] * (data_fields_len - len(row)) for row in data]
        sqls[0] = "SELECT " + ",".join(["%s AS `%s`" % (val, fie) for val, fie in list(zip(sqls[0], fields))])
        sqls[1:] = ["SELECT " + ",".join(sql) for sql in sqls[1:]]
        sql = " UNION ALL ".join(sqls)
        return sql

    def execute(
        self,
        sql: "str",
        parms: "dict | list(dict,)"=None,
        fill_field: "bool"=True,
        none_values: "list"=none_values,
        only_once: "bool"=True,
        **kw_parms: "object"
    ) -> LegacyCursorResult:
        """
        Execute SQL and add methods fetch_table and fetch_df.

        Parameters
        ----------
        sql : str
            SQL in sqlalchemy.text format.
        parms : dict or list(dict,)
            Parameters set for filling sqlalchemy.text.
        fill_field : bool
            Whether fill missing fields.
        none_values : list(object,)
            Values to be converted to None.
        only_once : bool
            Whether the database connect engine is one-time (i.e. real time creation).
        **kw_parms : object
            Keyword parameters for filling sqlalchemy.text.

        Returns
        -------
        LegacyCursorResult object
            Object of alsqlchemy package.
        """

        check_parm(sql, str)
        check_parm(parms, dict, list, None)
        check_parm(fill_field, bool)
        check_parm(none_values, list)
        check_parm(only_once, bool)

        only_once = get_first_notnull(only_once, self.only_once)

        if self.conn:
            conn = self.conn
        else:
            conn = self.create_conn(only_once=only_once)
        if parms != None or kw_parms != {}:
            if parms != None and kw_parms != {}:
                if type(parms) == list:
                    for parm in parms:
                        parm.update(kw_parms)
                else:
                    parms.update(kw_parms)
            elif kw_parms != {}:
                parms = kw_parms
            parms = self.fill_sql_none(sql, parms, fill_field, none_values)
            sql = text(sql)
            result = conn.execute(sql, parms)
        else:
            result = conn.execute(sql)
        fetch_table = lambda _self, fileds=None: self.fetch_table(_self, fileds)
        fetch_df = lambda _self, fileds=None: self.fetch_df(_self, fileds)
        fetch_sql = lambda _self, fileds=None: self.fetch_sql(_self, fileds)
        result.fetch_table = MethodType(fetch_table, result)
        result.fetch_df = MethodType(fetch_df, result)
        result.fetch_sql = MethodType(fetch_sql, result)
        if self.only_once:
            self.conn.close()
            del self.conn
            self.conn = None
        return result

    def execute_select(
            self,
            table: "str",
            database: "str"=None,
            fields: "str | iter"=None,
            where: "str"=None,
            order: "str"=None,
            limit: "int | str | iter"=None,
            print_sql: "bool"=False
        ) -> "LegacyCursorResult":
        """
        Execute select SQL.

        Parameters
        ----------
        table : str
            Table name.
        database : str
            Database name.
        fields : None or str or iterator
            Select syntax content.

            - None : Is 'SELECT *'.
            - str : Join as 'SELECT str'.
            - iterator(str,) : Join as 'SELECT \`str\`, ...'.

        where : str
            Where syntax content.
            Join as 'WHERE str'.
        order : str
            Order by syntax content.
            Join as 'ORDER BY str'.
        limit : int or str or iterator(str/int, str/int)
            Limit syntax content.

            - int | str : Join as 'LIMIT int/str'.
            - iterator(int/str, ...) with length of 1 or 2 : Join as 'LIMIT int/str, ...'.

        print_sql : bool
            Whether print SQL.

        Returns
        -------
        LegacyCursorResult object
            Object of alsqlchemy package.
        """

        check_parm(table, str)
        check_parm(database, str, None)
        check_parm(where, str, None)
        check_parm(order, str, None)

        database = get_first_notnull(database, self.database)

        check_parm(database, str)

        sqls = []
        if fields == None:
            fields = "*"
        elif is_iterable(fields):
                fields = ",".join(["`%s`" % field for field in fields])
        select_sql = (
            f"SELECT {fields}\n"
            f"FROM `{database}`.`{table}`"
        )
        sqls.append(select_sql)
        if where != None:
            where_sql = "WHERE %s" % where
            sqls.append(where_sql)
        if order != None:
            order_sql = "ORDER BY %s" % order
            sqls.append(order_sql)
        if limit != None:
            list_type = type(limit)
            if list_type in [str, int]:
                limit_sql = f"LIMIT {limit}"
            else:
                if len(limit) in [1, 2]:
                    limit_content = ",".join([str(val) for val in limit])
                    limit_sql = "LIMIT %s" % limit_content
                else:
                    error("The length of the limit parameter value must be 1 or 2", ValueError)
            sqls.append(limit_sql)
        sql = "\n".join(sqls)
        if print_sql:
            rprint(sql, title="SQL", format=None, full_frame=False)
        result = self.execute(sql)
        return result


    def execute_update(
        self,
        data: "LegacyCursorResult | list(dict,) | dict",
        table: "str",
        database: "str"=None,
        primary_key: "str"=None,
        print_sql: "bool"=False
    ) -> "None":
        """
        Update the data of table in the datebase.
    
        Parameters
        ----------
        data : LegacyCursorResult or list(dict,) or dict
            Updated data.
        table : str
            Table name.
        database : str
            Database name.
        primary_key : str or None
            Where syntax content.

            - str : Is f'WHERE `{str}` = :{str}'.
            - None : Is 'WHERE `%s` = :%s' % (first field name and value of each item).

        print_sql : bool
            Whether print SQL.

        Returns
        -------
        LegacyCursorResult object
            Object of alsqlchemy package.
        """

        check_parm(table, str)
        check_parm(data, LegacyCursorResult, list, dict)
        check_parm(database, str, None)
        check_parm(primary_key, str, None)

        database = get_first_notnull(database, self.database)

        check_parm(database, str)

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.fetch_table(data)
        elif data_type == dict:
            data = [data]
        for row in data:
            if primary_key == None:
                primary_key = list(row.keys())[0]
            set_content = ",".join(["`%s` = :%s" % (key, key)for key in row if key != primary_key])
            sql = (
                f"UPDATE `{database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE `{primary_key}` = :{primary_key}"
            )
            if print_sql:
                rprint(sql, title="SQL", format=None, full_frame=False)
            self.execute(sql, row, only_once=False)
        if self.only_once:
            self.conn == None

    def execute_insert(
        self,
        data: "LegacyCursorResult | list(dict,) | dict",
        table: "str",
        database: "str"=None,
        duplicate_method: "str"=None,
        print_sql: "bool"=False
    ) -> "None":
        """
        Insert the data of table in the datebase.

        Parameters
        ----------
        data : LegacyCursorResult or list(dict,) or dict
            Updated data.
        table : str
            Table name.
        database : str
            Database name.
        duplicate_method : str {'ignore', 'update'}
            Syntax method when constraint error.

            - None : Then no syntax.
            - 'ignore' : Is 'UPDATE IGNORE INTO'.
            - 'update' : Is 'ON DUPLICATE KEY UPDATE'.

        print_sql : bool
            Whether print SQL.

        Returns
        -------
        LegacyCursorResult object
            Object of alsqlchemy package.
        """
        
        check_parm(table, str)
        check_parm(data, LegacyCursorResult, list, dict)
        check_parm(database, str, None)

        database = get_first_notnull(database, self.database)

        check_parm(database, str)

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.fetch_table(data)
        elif data_type == dict:
            data = [data]
        fields = list({key for row in data for key in row})
        fields_str = ",".join(["`%s`" % field for field in fields])
        fields_str_position = ",".join([":" + field for field in fields])
        if duplicate_method == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate_method == "update":
            update_content = ",".join(["`%s` = VALUES(`%s`)" % (field, field) for field in fields])
            sql = (
                f"INSERT INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        if print_sql:
            rprint(sql, title="SQL", format=None, full_frame=False)
        self.execute(sql, data)