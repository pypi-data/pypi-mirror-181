# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for parsing and converting python types.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: type_utils
'''



from dataclasses import dataclass
import re as re
import os as _os
from re import L
import sys
import time
from typing import Union as _Union
from typing import Iterable as _Iterable

import mysql.connector
import traceback as _traceback
from mysql.connector import Error
from colorama import Fore as _Fore
from colorama import Style as _Style
from colemen_config import _db_mysql_database_type
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _cfu
import colemen_utilities.directory_utils as _dirs
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu


# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils as _cdb
# _TableManager = _cdb.TableManager
import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class UpdateQuery:
    table_name:str = None
    schema_name:str = None
    limit:int = None
    offset:int = None
    statement:str = None
    args = None
    database:_db_mysql_database_type = None
    _count:bool = False
    '''True if this query should return the count of rows selected'''

    _average:bool = False
    '''True if this query should return the average of rows selected'''

    _sum_:bool = False
    '''True if this query should return the sum of rows selected'''

    _wheres = None
    _updates = None
    _params = None



    def __init__(self,**kwargs):
        self._wheres = []
        self._updates = []
        self._params = {}
        # self._count = False
        # self._average = False
        # self._sum_ = False
        for k,v in kwargs.items():
            if hasattr(self,k):
                setattr(self,k,v)

        if self.database is not None:
            self.schema_name = self.database.database
            self.limit = self.database.get_limit

    def execute(self):
        if self.database is None:
            raise Exception("Select Query does not have a database to execute the query on")
        # self.__correlate_updates_to_table()
        sql,args= self.query
        

        # print(f"sql: {sql}")
        # print(f"args: {args}")
        return self.database.run(sql,args)

    # def __correlate_updates_to_table(self):
    #     data = {}
    #     for up in self._updates:
    #         data[up['column_name']] = up['value']
    #     new_updates = []
    #     data = self.database.correlate_to_table(self.table_name,data,crud="update",cerberus_validate=True)
    #     self._updates = []
    #     for k,v in data.items():
    #         self.add_column(k,v)
    #     self._updates = new_updates
        
    @property
    def schema_table_string(self):
        '''
            Get this Query's schema_table_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 10:47:15
            `@memberOf`: Query
            `@property`: schema_table_string
        '''
        value = f"`{self.table_name}`"
        if self.schema_name is not None:
            value = f"`{self.schema_name}`.{value}"
        return value


    @property
    def query(self):
        '''
            Get this UpdateQuery's query

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:44:59
            `@memberOf`: UpdateQuery
            `@property`: query
        '''
        value = f"UPDATE {self.schema_table_string} SET {self.update_string}{self.where_string}"

        value = _paginate_select_query(value,self.limit,self.offset)
        value = _format_query_params(value,self._params)
        return value,self._params

    @property
    def where_string(self):
        '''
            Get this UpdateQuery's where_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:45:29
            `@memberOf`: UpdateQuery
            `@property`: where_string
        '''
        value = self._wheres
        # self._params = {}
        if len(self._wheres) > 0:
            wheres = []
            for where in self._wheres:
                if where['comparison'] in ["between"]:
                    min_key =f"{where['column_name']}_minimum"
                    max_key =f"{where['column_name']}_maximum"

                    single_where = f"{where['column_name']} {where['comparison'].upper()} :{min_key} AND :{max_key}"
                    self._params[min_key] = where['value']
                    self._params[max_key] = where['max_value']


                elif where['comparison'] in ["in"]:
                    in_list = []
                    for idx,val in enumerate(where['value']):
                        key = f"{where['column_name']}_{idx}"
                        self._params[key] = val
                        in_list.append(f":{key}")
                    in_list_string = ', '.join(in_list)
                    single_where = f"{where['column_name']} {where['comparison'].upper()} ({in_list_string})"



                elif where['comparison'] in ["is","is not"]:
                    single_where = f"{where['column_name']} {where['comparison'].upper()} {str(where['value'])}"
                    # params[where['column_name']] = where['value']
                else:
                    single_where = f"{where['column_name']} {where['comparison']} :{where['column_name']}"
                    self._params[where['column_name']] = where['value']
                wheres.append(single_where)
            wheres = ' AND '.join(wheres)
            value = f" WHERE {wheres}"
        else:
            value = ""
        return value

    @property
    def update_string(self):
        '''
            Get this UpdateQuery's update_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: UpdateQuery
            `@property`: update_string
        '''
        if len(self._updates) == 0:
            return None
        else:
            selects = []
            for sel in self._updates:
                value = None
                value = f"{sel['column_name']}=:{sel['column_name']}"
                self._params[sel['column_name']] = sel['value']
                selects.append(value)
            value = ', '.join(selects)

        return value


    def add_where(self,column_name,value,comparison="="):
        if value is None:
            value = "NULL"

        if _csu.to_snake_case(comparison) in ["!","!=","isnt","isnot","is_not","<>"]:
            comparison = "is not"

        data = {
            "column_name":column_name,
            "comparison":comparison,
            "value":value,
            "max_value":None,
        }
        if _csu.to_snake_case(comparison) in ["between"]:
            if isinstance(value,(list,tuple)):
                data['value'] = value[0]
                data['max_value'] = value[1]
            else:
                data['value'] = 0
                data['max_value'] = value

        if _csu.to_snake_case(comparison) in ["in"]:
            value = _lu.force_list(value)
            if isinstance(value,(list,tuple)):
                items = []
                for idx,x in enumerate(value):
                    if isinstance(x,(str)):
                        # key = f"{column_name}_{idx}"
                        # items[key] = f"'{x}'"
                        items.append(x)


                    if isinstance(x,(int,float)):
                        # key = f"{column_name}_{idx}"
                        items.append(f"{x}")
                        # items[key] = f"{x}"

                # str_list = ', '.join(items)

                data['value'] = items

        self._wheres.append(data)

    def add_column(self,column_name,value):
        data = {
            "column_name":column_name,
            "value":value,
        }
        self._updates.append(data)
        self.validate()

    def validate(self):
        if self.database is None:
            return
        new_updates = []
        for up in self._updates:
            column_name = up['column_name']
            value = up['value']
            if self.database is not None:
                result = self.database.correlate_to_table(self.table_name,{column_name:value},crud_type="update",cerberus_validate=True)
                for k,v in result.items():
                    data = {
                        "column_name":k,
                        "value":v,
                    }
                    new_updates.append(data)
                # print(f"result:{result}")
        self._updates = new_updates

def _paginate_select_query(sql:str,limit:int=None,offset:int=None)->str:
    '''
        Apply a limit and offset value to a select query statement.
        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql statement to modify

        [`limit`=None] {int}
            The limit to apply to the results.

        [`offset`=None] {int}
            The offset to apply to the results.


        Return {str}
        ----------------------
        The sql statement with a limit and offset value applied.

        If the limit/offset if invalid no pagination is added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 11:09:53
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _paginate_select_query
        * @xxx [12-09-2022 11:11:52]: documentation for _paginate_select_query
    '''
    if limit is None and offset is None:
        return sql
    if isinstance(limit,(str)):
        limit = re.sub(r'[^0-9]',"",limit)
        if len(limit) == 0:
            return sql
        limit = int(limit)

    if isinstance(offset,(str)):
        offset = re.sub(r'[^0-9]',"",offset)
        if len(offset) == 0:
            offset = None
        else:
            offset = int(offset)

    if limit == 0:
        limit = 1

    if offset is not None:
        if offset < 1:
            offset = None

    sql = _csu.strip(sql,[";"],"right")
    sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

    limit_string = f"LIMIT {limit}"
    offset_string = ""
    if offset is not None:
        offset_string = f"OFFSET {offset}"
    paginate = f"{limit_string} {offset_string}"
    sql = f"{sql} {paginate}"
    return sql


def _format_query_params(sql:str,args:dict)->str:
    '''
        Format an SQL query's parameters to use the python named template format.

        This will only replace matches that have a corresponding key in the args dictionary.

        Parameters can begin with a dollar sign or colon.


        SELECT * from blackholes WHERE hash_id=$hash_id

        SELECT * from blackholes WHERE hash_id=%(hash_id)s

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql string to format.

        `args` {dict}
            The dictionary of parameter values.


        Return {str}
        ----------------------
        The sql statement with parameters replaced.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 10:39:24
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _format_query_params
        * @xxx [12-09-2022 10:43:23]: documentation for _format_query_params
    '''
    if isinstance(args,(dict)) is False:
        return sql
    # args = sorted(args.items(), key=lambda x: x[1], reverse=True)
    arg_keys = list(args.keys())
    arg_keys.sort(key=len, reverse=True)
    for k in arg_keys:
    # for k,v in args.items():
        sql = re.sub(fr'[$:]{k}',f"%({k})s",sql)

    # matches = re.findall(r'[$:]([a-z_0-9]*)',sql,re.IGNORECASE)
    # if isinstance(matches,(list)):
    #     for match in matches:
    #         if match in args:
    #             sql = sql.replace(f"${match}",f"%({match})s")

    return sql


if __name__ == '__main__':
    import time
    q = UpdateQuery(
        table_name="blackholes",
        schema_name="boobs",
    )
    # q.add_where("expiration",(0,time.time()),"between")
    q.add_where("hash_id","blackhole_RgH1OzdPnkGbj9dES593UlXc","=")
    q.add_column("reason","someShit")
    q.add_column("message","boobies")
    # q.add_select("hash_id")
    sql,args = q.query
    print(sql)
    print(args)

