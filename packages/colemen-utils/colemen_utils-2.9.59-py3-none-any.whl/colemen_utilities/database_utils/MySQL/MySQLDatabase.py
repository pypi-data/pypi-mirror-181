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


import datetime
from dataclasses import dataclass
import json
import re as re
import os as _os
from re import L
import sys
import time
from typing import Iterable, Union as _Union
from typing import Iterable as _Iterable

import mysql.connector as _mysqlConnector
import traceback as _traceback
from mysql.connector import Error
from colorama import Fore as _Fore
from colorama import Style as _Style
from colemen_config import _db_column_type,_db_table_type,_db_mysql_delete_query_type,_db_mysql_select_query_type,_db_mysql_update_query_type
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _cfu
import colemen_utilities.directory_utils as _dirs
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _lu
from colemen_utilities.database_utils.MySQL.SelectQuery import SelectQuery
from colemen_utilities.database_utils.MySQL.UpdateQuery import UpdateQuery
from colemen_utilities.database_utils.MySQL.DeleteQuery import DeleteQuery
from colemen_utilities.database_utils.MySQL.Table import Table


# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils.TableManager as _table_manager

# import colemen_utilities.database_utils as _cdb
# _TableManager = _cdb.TableManager
import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class MySQLDatabase:
    database:str = None
    user:str = None
    password:str = None
    host:str = None
    _tables = None
    cache_path:str = None
    get_limit:int = 100


    def __init__(self,**kwargs):
        self._dbm = None
        '''The Database manager instance.'''

        self.database:str = _obj.get_kwarg(['database','name'],None,(str),**kwargs)
        '''The name of the database/schema this instance represents.'''

        self.user:str = _obj.get_kwarg(['user'],None,(str),**kwargs)
        '''The user name used to connect to the database.'''

        self.password:str = _obj.get_kwarg(['password'],None,(str),**kwargs)
        '''The password used to connect to the database.'''

        self.host:str = _obj.get_kwarg(['host'],None,(str),**kwargs)
        '''The host address used to connect to the database'''

        self._credentials:bool = None
        '''True if the credentials dictionary can be successfully compiled.'''


        self.data = {}
        self.settings = {}
        self.con = None
        self.cur = None
        self._tables = {}


        self.connect()


    @property
    def summary(self):
        '''
            Get this MySQLDatabase's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: MySQLDatabase
            `@property`: summary
        '''
        value = {
            "schema":self.database,
        }
        # print(f"self._tables:{self._tables}")
        value['tables'] = { k:v.summary for (k,v) in self._tables.items()}
        # value['tables'] = [x.summary for x in self._tables]

        return value

    # def save(self):
    #     table:_db_table_type
    #     for _,table in self._tables.items():
    #         table.cache.save()
        # _cfu.writer.to_json(f"{self.cache_path}/db_summary.json",self.summary)

    @property
    def __credentials(self):
        '''
            Verify that all credentials were provided and compile the credential dictionary.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-28-2022 09:05:14
            `@memberOf`: __init__
            `@property`: credentials
        '''
        missing_keys = []
        if self.user is None:
            missing_keys.append('user')
        if self.password is None:
            missing_keys.append('password')
        if self.host is None:
            missing_keys.append('host')
        if self.database is None:
            missing_keys.append('database')
        if len(missing_keys) > 0:
            _log(f"MISSING CREDENTIALS: {missing_keys}","warning")
            self._credentials = False
            return False
        creds = {
            "user":self.user,
            "password":self.password,
            "host":self.host,
            "database":self.database,
        }
        self._credentials = True
        return creds

    def connect(self)->bool:
        '''
            Attempts to connect to the database.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 10:03:16
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __connect_to_my_sqldb
        '''
        connect_success = False
        if self.con is not None:
            return True
        creds = self.__credentials
        if self._credentials:
            self.con = None
            try:
                self.con = _mysqlConnector.connect(
                    database =self.database,
                    user =self.user,
                    password =self.password,
                    host =self.host,
                )

                self.cur = self.con.cursor(
                    buffered=True,
                    dictionary=True
                )

                if self.con.is_connected():
                    # print("Successfully connected to mysql database")
                    _log("Successfully connected to database.","success")
                    connect_success = True

            except Error as error:
                print(error)

        if connect_success is False:
            _log("Failed to connect to database.","warning")

        return connect_success

    def list_schemas(self)->list:
        '''
            List all schemas in this database.

            ----------

            Return {list}
            ----------------------
            The list of schemas in this database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 19:17:41
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: list_schemas
            * @xxx [06-05-2022 19:19:02]: documentation for list_schemas
        '''

        schemas = []
        if self.settings['setup_complete'] is False:
            return False
        # master = _cfu.read.as_json(f"{_os.getcwd()}{_os_divider}modules{_os_divider}equari{_os_divider}parse_master_sql.json")
        print(f"\n{_csu.gen.title_divider('Equari Database Schemas')}\n\n")
        total_tables = 0
        for schema in self.data['schemas']:
            print(f"    {schema['name']}")
            schemas.append(schema['name'])
            total_tables += len(schema['tables'])

        print(f"Total Schemas: {len(self.data['schemas'])}")
        print(f"Total Tables: {total_tables}")
        print(f"\n\n{_csu.gen.title_divider('Equari Database Schemas')}\n\n")
        return schemas


    @property
    def is_connected(self):
        if self.con is not None:
            if self.con.is_connected() is True:
                return True
            # return True
        return False

    def run(self, sql:str, args:_Union[list,dict]=False):
        '''
            Executes a query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The sql query to execute.

            `args` {list,dict}
                A list of arguments to apply to the sql query

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            if multiple statements are provided it will return True if ALL statements execute successfully.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:07:54
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: run
        '''

        statements = sql
        # if the sql is a string, split it into a list of statements
        if isinstance(sql, (str)):
            statements = _to_statement_list(sql)



        if len(statements) > 1:
            # print(f"Multiple statements [{len(statements)}] found in sql.")
            success = True
            for statement in statements:
                # print(f"statement: {statement}")
                res = self.execute_single_statement(statement, args)
                if res is False:
                    success = False
            return success

        if len(statements) == 1:
            return self.execute_single_statement(sql, args)

    def run_select(self,sql:str,args=False,**kwargs):
        '''
            Execute a select query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {str}
                The Select query to execute.

            `args` {list,dict}
                The arguments to use in parameterized placeholders

            Keyword Arguments
            -------------------------
            [`default`=None] {any}
                The default value to return in the event of an error.

            [`limit`=None] {int}
                The maximum number of results to return

            [`offset`=None] {int}
                The index offset to apply to the query.

            Return {any}
            ----------------------
            The results of the query if successful, the default value otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:12:16
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: run_select
            * @xxx [12-09-2022 11:15:35]: documentation for run_select
        '''
        default = _obj.get_kwarg(['default'],None,None,**kwargs)
        limit = _obj.get_kwarg(['limit'],None,(int),**kwargs)
        offset = _obj.get_kwarg(['offset'],None,(int),**kwargs)

        sql = _paginate_select_query(sql,limit,offset)
        if isinstance(args,(dict)):
            sql = _format_query_params(sql,args)
        # print(f"sql:{sql}")
        if self.connect() is False:
            return default
        _log(f"sql:{sql}","cyan")
        _log(f"args:{args}","cyan")

        if self.run(sql,args):
            return self.fetchall()
        return default



    def insert_to_table(self,table_name:str,data:dict):
        data = self.correlate_to_table(table_name,data,crud="create",cerberus_validate=True)
        from colemen_utilities.sql_utils import insert_from_dict
        if len(data.keys()) == 0:
            return False
        sql,args = insert_from_dict(data,table_name,self.database)
        print(f"sql: {sql}")
        print(f"args: {args}")
        result = self.run(sql,args)
        if result is True:
            return self.last_id()

    def select_query(self,table_name:str)->_db_mysql_select_query_type:
        '''Create a new select query instance'''
        return SelectQuery(database=self,table_name=table_name)

    def update_query(self,table_name:str)->_db_mysql_update_query_type:
        '''Create a new update query instance'''
        return UpdateQuery(database=self,table_name=table_name)

    def delete_query(self,table_name:str)->_db_mysql_delete_query_type:
        '''Create a new delete query instance'''
        return DeleteQuery(database=self,table_name=table_name)

    # def get_from_table(self,table_name:str,data:dict,**kwargs):
    #     limit = _obj.get_kwarg(['limit'],self.get_limit,(int),**kwargs)
    #     offset = _obj.get_kwarg(['offset'],None,(int),**kwargs)
    #     select = _obj.get_kwarg(['select'],None,(list,dict),**kwargs)
    #     data = self.correlate_to_table(table_name,data,crud="read",cerberus_validate=True)
    #     from colemen_utilities.sql_utils import select_from_dict
    #     if len(data.keys()) == 0:
    #         return False

    #     sql,args = select_from_dict(
    #         data,
    #         table_name,
    #         schema_name=self.database,
    #         select = select,
    #     )

    #     sql = _paginate_select_query(sql,limit,offset)
    #     sql = _format_query_params(sql,data)

    #     # TODO []: COMMENTED FOR TESTING
    #     # result = self.run_select(sql,args)
    #     # TODO []: COMMENTED FOR TESTING
    #     print(f"result:{(sql,args)}")

    def close(self):
        '''
            Close the connection to the mySQL database.

            ----------

            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 19:19:32
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: close
            * @xxx [06-05-2022 19:20:10]: documentation for close
        '''

        self.con.close()
        self.con = None
        self.cur = None

    def execute_single_statement(self, sql:str, args=False,isTimeoutRetry=False):
        '''
            Executes a single SQL query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The SQL to be executed.

            `args` {list}
                A list of arguments for parameter substitution.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2021 09:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: execute_single_statement
        '''
        success = False
        if self.cur is None or self.con is None:
            print("Not connected to a database, aborting query.")
            if self.data['credentials'] is not None:
                self.connect()
        try:
            if args is False:
                # print(f"executing sql: ",sql)
                self.cur.execute(sql)
            else:
                # args = _csu.sql.sanitize_quotes(args)
                args = _sanitize_args(args)
                if isinstance(args,(dict)):
                    sql = _format_query_params(sql,args)
                # print(f"args:{args}")
                self.cur.execute(sql, args)

                # print(f"result: ",result)

            self.con.commit()
            success = True


        except _mysqlConnector.errors.IntegrityError:
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        except _mysqlConnector.errors.InterfaceError:
            if isTimeoutRetry is True:
                _log(f"{_traceback.format_exc()}","error")
                _log(f"SQL: {sql}","error")
            if isTimeoutRetry is False:
                # _log(f"CONNECTION TIMED OUT")
                self.cur = None
                self.con = None
                self.connect()
                return self.execute_single_statement(sql,args,True)

        except _mysqlConnector.errors.DatabaseError:
            # print(f"ERROR: {err}", PRESET="FATAL_ERROR_INVERT")
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        except AttributeError:
            _log(f"{_traceback.format_exc()}\n","error")
            _log(f"{print(sys.exc_info()[2])}\n\n","error")
            _log(f"SQL: \033[38;2;(235);(64);(52)m{sql}")
        return success

    def run_from_list(self, query_list,**kwargs):
        '''
            Execute SQL statements from a list.

            ----------

            Arguments
            -------------------------
            `query_list` {list}
                A list of query statements to execute.

            Keyword Arguments
            -------------------------
            [`disable_restraints`=True] {bool}
                If True, temporarily disable foreign_key_checks while executing the queries

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 16:32:58
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: run_from_list
            * @xxx [06-05-2022 16:36:56]: documentation for run_from_list
        '''

        disable_foreign_key_restraints = _obj.get_kwarg(['disable key restraints','disable restraints'],True,(bool),**kwargs)
        # disable_foreign_key_restraints = True
        # if 'DISABLE_KEY_RESTRAINTS' in kwargs:
        #     if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
        #         disable_foreign_key_restraints = False
        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 0;")

        success = True
        for idx,que in enumerate(query_list):
            print(f"{idx}/{len(query_list)}",end="\r",flush=True)
            success = self.run(que)
            if success is False:
                break

        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 1;")
        return success

    def run_multi(self, sql:str, args):
        sql = sql.replace(";", ";STATEMENT_END")
        statements = sql.split('STATEMENT_END')
        for s in statements:
            if len(s) > 0:
                # print(f"query: {s}")
                self.run(s, args)

    def fetchall(self):
        '''
            Executes the fetchall method on the database and converts the result to a dictionary.

            ----------


            Return {dict|list}
            ----------------------
            If there is more than one result, it returns a list of dicts.
            If there is only one result, it returns a single dictionary.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 13:58:55
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: fetchall
            * @xxx [06-02-2022 13:59:37]: documentation for fetchall
        '''
        return self._to_dict(self.cur.fetchall())

    def fetchone(self):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"fetchone",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes the fetchone method on the database.",
                "returns":{
                    "type":"dict",
                    "description":"The result of the fetchone command"
                }
            }"""
        r = self.cur.fetchone()
        return r

    def execute_sql_from_file(self, filePath:str, **kwargs):
        '''
            Executes queries stored in a file.

            ----------

            Arguments
            -------------------------
            `file_path` {str}
                The filePath to the sql file

            Keyword Arguments
            -------------------------
            `DISABLE_KEY_RESTRAINTS` {bool}
                If True, temporarily disable foreign_key_checks while executing the queries

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 16:29:39
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: execute_sql_from_file
            * @xxx [06-05-2022 16:41:53]: documentation for execute_sql_from_file
        '''

        with open(filePath, 'r', encoding='utf-8') as file:
            sql = file.read()
            # print(f"filePath:{filePath}")
            statements = [str(x) for x in _csu.sql.get_statements(sql)]
            # sql = _csu.strip_sql_comments(sql)
            # _re.sub(r";")
            # sql = sql.replace(";", ";STATEMENT_END")
            # statements = sql.split('STATEMENT_END')

        # self.run("SET foreign_key_checks=0;")
        # "SOURCE /backups/mydump.sql;" -- restore your backup within THIS session
        # statements = getSQLStatementsFromFile(filePath)
        # print(f"total statements: {len(statements)}")
        disable_foreign_key_restraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disable_foreign_key_restraints = False
        return self.run_from_list(statements, DISABLE_KEY_RESTRAINTS=disable_foreign_key_restraints)
        # self.run("SET foreign_key_checks=1;")

    def _to_dict(self, result):
        # print(f"_to_dict: resultType: {type(result)}")
        if isinstance(result, list):
            new_data = []
            for row in result:
                tmp = {}
                for col in row.keys():
                    tmp[col] = row[col]
                new_data.append(tmp)
            return new_data
        if isinstance(result, sqlite3.Row):
            new_data = {}
            for col in result.keys():
                new_data[col] = result[col]
            return new_data

    def last_id(self):
        sql = 'SELECT LAST_INSERT_ID();'
        result = self.run_select(sql)
        if isinstance(result,(list)):
            result = result[0]['LAST_INSERT_ID()']
        return result


    def get_column_data(self,table_name:str,default=None)->Iterable[_db_column_type]:
        '''
            Retrieve the column meta data for all columns in the table provided.

            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to retrieve column data about.

            [`default`=None] {any}
                The value to return if no columns are found.


            Return {list}
            ----------------------
            A list of column instances if successful, the default otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:18:41
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_column_data
            * @xxx [12-09-2022 11:19:52]: documentation for get_column_data
        '''
        # if table_name in self._tables:
        #     return self._tables[table_name]['columns']

        if self.connect() is False:
            return False
        # @Mstep [] get the INFORMATION_SCHEMA.COLUMNS data from the database.
        sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=$schema_name AND TABLE_NAME=$table_name"
        args = {
            "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql, args)

        if isinstance(result,(list)) is False:
            return default

        keys = self.get_foreign_keys(table_name)


        columns = []
        for col in result:
            for key in keys:
                if col['COLUMN_NAME'] == key['COLUMN_NAME']:
                    col['constraint'] = key
            columns.append(col)


        # import colemen_utilities.database_utils.MySQL.Column.Column as _col
        output = columns
        # output = []
        # for col in columns:
            # output.append(_col.Column(col))
            # output.append(_col.Column(col))
        if len(columns) == 0:
            output = default
        return output

    # def get_column_data(self,table_name:str,default=None)->Iterable[_db_column_type]:
    #     '''
    #         Retrieve the column meta data for all columns in the table provided.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `table_name` {str}
    #             The name of the table to retrieve column data about.

    #         [`default`=None] {any}
    #             The value to return if no columns are found.


    #         Return {list}
    #         ----------------------
    #         A list of column instances if successful, the default otherwise.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-09-2022 11:18:41
    #         `memberOf`: MySQLDatabase
    #         `version`: 1.0
    #         `method_name`: get_column_data
    #         * @xxx [12-09-2022 11:19:52]: documentation for get_column_data
    #     '''
    #     # if table_name in self._tables:
    #     #     return self._tables[table_name]['columns']

    #     if self.connect() is False:
    #         return False
    #     # @Mstep [] get the INFORMATION_SCHEMA.COLUMNS data from the database.
    #     sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=$schema_name AND TABLE_NAME=$table_name"
    #     args = {
    #         "schema_name":self.database,
    #         "table_name":table_name,
    #     }
    #     result = self.run_select(sql, args)
    #     # _cfu.writer.to_json("tmp.json",result)
    #     if isinstance(result,(list)) is False:
    #         result = []
    #     import colemen_utilities.database_utils.MySQL.Column.Column as _col
    #     output = []
    #     for col in result:
    #         output.append(_col.Column(col))
    #     if len(output) == 0:
    #         output = default
    #     return output

    def get_cerberus_schema(self,table_name,crud_type=None,to_json=False):
        tb = self.get_table(table_name)
        result = []
        if tb is not None:
            result = tb.columns
        # result = self.get_column_data(table_name)

        # col:colemen_config._db_column_type = result[0]


        cerb = {}
        for x in result:
            valid = x.validation.cerberus_schema(crud_type)
            if valid is not None:
                data = {}
                for k,v in valid.items():
                    if to_json is True:
                        if k in ["check_with",'coerce']:
                            v = v.__name__
                    data[k] = v
                cerb[x.name] = data
        if to_json is True:
            return json.dumps(cerb,indent=4)
        return cerb

    def get_foreign_keys(self,table_name:str):
        '''
            Retrieve a list of columns that are foreign keys in the table provided.
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to query.


            Return {list}
            ----------------------
            A list of foreign key columns, the list is empty if there are None.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:24:42
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_foreign_keys
            * @xxx [12-09-2022 11:26:26]: documentation for get_foreign_keys
        '''
        # if table_name in self._tables:
        #     return self._tables[[table_name]]['foreign_keys']
        if self.connect() is False:
            return False
        sql = f'''
            SELECT
                TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME,REFERENCED_TABLE_SCHEMA
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                TABLE_NAME = $table_name AND
                TABLE_SCHEMA = $schema_name AND
                REFERENCED_TABLE_NAME IS NOT NULL;
        '''
        args = {
            "schema_name":self.database,
            "table_name":table_name,
        }
        result = self.run_select(sql,args)
        if isinstance(result,(list)) is False:
            result = []
        # self._tables[table_name]
        # self._tables[table_name]['foreign_keys'] = result
        return result

    def get_table_data(self,table_name:str):
        '''
            Retrieve the Table's meta data and
            ----------

            Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                arg_description

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-12-2022 09:02:38
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: get_table_data
            * @TODO []: documentation for get_table_data
        '''
        # if table_name in self._tables:
        #     return self._tables[table_name]
        keys = self.get_foreign_keys(table_name)
        columns = self.get_column_data(table_name)
        output = []
        # TODO []: modify this method to use the Column class
        for col in columns:
            for key in keys:
                if col['COLUMN_NAME'] == key['COLUMN_NAME']:
                    col['constraint'] = key
            output.append(col)
        # self._tables[table_name] = output
        return output

    def get_table(self,table_name:str)->_db_table_type:
        # @Mstep [IF] if the table already exists in the _tables dictionary.
        if table_name in self._tables:
            # @Mstep [RETURN] return table
            return self._tables[table_name]
        # @Mstep [IF] if we fail to connect to the database
        if self.connect() is False:
            # @Mstep [RETURN] return False
            return False

        output = None
        # @Mstep [] instantiate the table
        tb = Table.Table(self,table_name)
        # @Mstep [IF] if the table cannot be loaded from a cache file.
        if tb.cache.exists is False:
            _log("database.get_table - Failed to get table from cache.","warning")
            # @Mstep [] retrieve the tables data from the database.
            result = self.get_table_meta_data(table_name)
            # @Mstep [IF] if the data is successfully retrieved
            if isinstance(result,(list)):
                # @Mstep [LOOP] iterate the results (there should only ever be ONE)
                for table_data in result:
                    # cols = self.get_column_data(table_name)
                    # if isinstance(cols,(list)):
                    #     for col in cols:
                    #         tb.add_column(col)
                    # @Mstep [] have the table populate using the result data.
                    tb.populate_from_dict(table_data)
                    # tb = Table.Table(self,table_name,table_data)
                    # @Mstep [] add the table to self._tables[table_name]
                    self._tables[table_name] = tb
                    tb.save_cache()
                    output = tb
        # @Mstep [ELSE] if the table was loaded from the cache file.
        else:
            self._tables[table_name] = tb
            output = tb
        return output

    def get_table_meta_data(self,table_name:str,default=None):
        sql = f"""select *
            from INFORMATION_SCHEMA.TABLES
            where table_type = 'BASE TABLE'
                    and table_schema = '{self.database}'
                    and table_name = '{table_name}'"""
        result = self.run_select(sql)
        output = []
        for table in result:
            if isinstance(table,(dict)):
                table = _obj.keys_to_snake_case(table)


                output.append(table)
        if len(output) == 0:
            output = default
        return output


    # def get_table_meta_data(self):


    #     sql = f"""select *
    #         from INFORMATION_SCHEMA.TABLES
    #         where table_type = 'BASE TABLE'
    #                 and table_schema = '{self.database}'"""
    #     result = self.run_select(sql)
    #     output = []
    #     for table in result:
    #         if isinstance(table,(dict)):
    #             table = _obj.keys_to_snake_case(table)
    #             tb = Table.Table(self,table['table_name'],table)
    #             cols:Iterable[_db_column_type] = self.get_column_data(table['table_name'])
    #             for col in cols:
    #                 tb.add_column(col)
    #         # if isinstance(table,(dict)):
    #             # table['create_time'] = table['create_time'].timestamp()
    #             output.append(table)
    #     return output

    # def validate_to_table(self,table_name:str,data:dict):
    #     cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
    #     crud_type = _obj.get_kwarg(['crud','crud_type'],None,(str),**kwargs)
    #     default_on_fail = _obj.get_kwarg(['default_on_failure'],False,(bool),**kwargs)

    def __assign_default_meta_cols(self,tb:_db_table_type,crud_type):
        output = {}
        if crud_type in ['create']:
            if tb.has_timestamp_column:
                output['timestamp'] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

            if tb.has_hash_id:
                output['hash_id'] = tb.gen_hash_id()

        if crud_type in ['update']:
            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

        if crud_type in ['delete']:
            if tb.has_modified_timestamp_column:
                output['modified_timestamp'] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

            if tb.has_deleted_column:
                output['deleted'] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()


        return output




    def correlate_to_table(self,table_name:str,data:dict,**kwargs):
        cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
        crud_type = _obj.get_kwarg(['crud','crud_type'],None,(str),**kwargs)
        default_on_fail = _obj.get_kwarg(['default_on_failure'],False,(bool),**kwargs)

        tb = self.get_table(table_name)
        cols = tb.columns
        # cols = self.get_column_data(table_name)
        col:_db_column_type
        output = self.__assign_default_meta_cols(tb,crud_type)


        for col in cols:
            name = col.data.column_name
            if name in data:
                value = data[name]
                value_type = type(value).__name__

                # if col.data.is_timestamp:
                #     value = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
                #     output[name] = value
                #     continue
                # if col.data.is_hash_id:
                #     value = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
                #     output[name] = value
                #     continue

                if cerberus_validate:
                    validation_schema = col.validation.cerberus_schema(crud_type)
                    if validation_schema is None:
                        a = "a"
                        if crud_type == "update":
                            a= "an"
                        _log(f"{name} is not an allowed column in {a} {crud_type} operation","warning")
                        continue

                    from colemen_utilities.validate_utils.cerberus import single_value
                    success,errors,output_data = single_value(name,validation_schema,value)
                    if success is False:
                        for k,v in errors.items():
                            _log(f"Value for {k} failed validation: {v}","warning")
                        continue
                    else:
                        _log(f"Successfully validated {name}","success")
                        output[name] = output_data[name]
                        # continue


                if value_type in col.data.py_data_type:
                    output[name] = value
                else:
                    if col.validation.is_boolean is True and value_type in ['string','int']:
                        from colemen_utilities.type_utils import to_bool
                        output[name] = to_bool(to_bool)
                        continue
                    if value is None and col.data.is_nullable is True:
                        output[name] = value
                    else:
                        if default_on_fail is True:
                            output[name] = col.data.default
                        else:
                            _log(f"Value for {name} expected: {col.validation.py_data_type} --- found: {value_type}","warning")

        return output


def _to_statement_list(sql):
    sql = sql.replace(";", ";STATEMENT_END")
    statements = sql.split('STATEMENT_END')
    output = [x.strip() for x in statements if len(x.strip()) > 0]
    return output

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

def _sanitize_args(args):
    if isinstance(args,(dict)):
        output = {}
        for k,v in args.items():
            output[k] = _csu.sanitize_quotes(v)
        return output
    if isinstance(args,(list)):
        output = []
        for v in args:
            output.append(_csu.sanitize_quotes(v))
        return output


def new(**kwargs)->MySQLDatabase:
    return MySQLDatabase(**kwargs)









