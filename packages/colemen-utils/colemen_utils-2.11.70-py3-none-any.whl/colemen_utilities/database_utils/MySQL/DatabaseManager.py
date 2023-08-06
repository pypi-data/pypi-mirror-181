
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import


'''
    Module containing the DatabaseManager class declaration.

    This is used to connect to a remote MySQL database and allows slightly abstracted
    methods for manipulating it.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-13-2022 12:42:25
    `memberOf`: MySQL
'''


import datetime
from dataclasses import dataclass
import json
import re as re
import os

import sys

from typing import Iterable, Union


import mysql.connector as _mysqlConnector
import traceback as _traceback
from mysql.connector import Error
from colemen_config import _db_column_type,_db_table_type,_db_mysql_database_type,_db_relationship_type

# import colemen_utilities.file_utils as _cfu
# import colemen_utilities.directory_utils as _dirs
# import colemen_utilities.list_utils as _lu
import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj


import colemen_utilities.database_utils.MySQL.MySQLDatabase as _mySQLDatabase


import colemen_utilities.console_utils as _con
_log = _con.log


@dataclass
class DatabaseManager:
    
    database:str = None
    '''The name of the database/schema this instance represents.'''

    user:str = None
    '''The user name used to connect to the database.'''

    password:str = None
    '''The password used to connect to the database.'''

    host:str = None
    '''The host address used to connect to the database'''

    _tables = None
    '''A dictionary of table instances the keys correspond to the table's name for quick lookups.'''

    _relationship = None
    '''A list of relationship instances'''

    no_caching:bool = False
    '''If True, no cache files will be created, this really slows shit down..'''

    cache_path:str = None
    '''File path to the directory where table cache files are stored.

    Defaults to: {cwd}/db_cache
    '''

    get_limit:int = 100
    '''The default LIMIT applied to select queries'''



    def __init__(self,**kwargs):
        '''
            Create a new MySQL database connection.
            ----------


            Keyword Arguments
            -------------------------
            `database` {str}
                The name of the database/schema this instance represents.

            `user` {str}
                The user name used to connect to the database.

            `password` {str}
                The password used to connect to the database.

            `host` {str}
                The host address used to connect to the database

            `cache_path` {str}
                The path to the directory where the table cache files can be saved.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:30:55
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: DatabaseManager
            * @xxx [12-13-2022 12:31:27]: documentation for DatabaseManager
        '''

        self._schemas = {}


        # initialize these attributes for later use.
        self._tables = {}
        self._relationships = []
        self._columns = []


    @property
    def summary(self):
        '''
            Get the summary dictionary for all databases associated to this .

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:21:04
            `@memberOf`: DatabaseManager
            `@property`: summary
        '''
        value = {
            "schemas":{},
        }
        for name,s in self._schemas.items():
            value['schemas'][name] = s.summary
        # print(f"self._tables:{self._tables}")
        # value['tables'] = { k:v.summary for (k,v) in self._tables.items()}
        # value['tables'] = [x.summary for x in self._tables]

        return value


    def add_schema(self,**credentials):
        if 'name' in credentials:
            credentials['database'] = credentials['name']
        credentials['database_manager'] = self
        schema = _mySQLDatabase.new(**credentials)
        schema.no_caching = self.no_caching
        schema.cache_path = self.cache_path
        self._schemas[credentials['database']] = schema

    def master_index(self):
        '''
            All schemas will retrieve their associated tables, columns and relationships.

            This typically only needs to be called after all schemas are added.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:34:20
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_index
            * @TODO []: documentation for master_index
        '''
        # @Mstep [LOOP] iterate all schemas
        schema:_db_mysql_database_type
        for name,schema in self._schemas.items():
            print(f"\n")
            _log(f"Indexing all tables in schema {name} {' '*150}","info invert")
            # @Mstep [] get all tables from the schema
            schema.get_all_tables()



    def register(self,entity):
        '''
            Used INTERNALLY to register database entities with this manager.

            ----------

            Arguments
            -------------------------
            `entity` {any}
                The entity to register with this manager.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:01:12
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: register
            * @xxx [12-16-2022 10:43:14]: documentation for register
        '''
        from colemen_utilities.database_utils.MySQL.Table import Table
        from colemen_utilities.database_utils.MySQL.Relationship import Relationship
        from colemen_utilities.database_utils.MySQL.Column import Column
        
        if isinstance(entity,_mySQLDatabase.MySQLDatabase):
            db:_db_mysql_database_type = entity
            self._schemas[db.name] = db

        if isinstance(entity,Table.Table):
            table:_db_table_type = entity
            self._tables[table.name] = table

        if isinstance(entity,Relationship.Relationship):
            rel:_db_relationship_type = entity
            self._relationships.append(rel)

        if isinstance(entity,Column):
            col:_db_column_type = entity
            self._columns.append(col)

    def get_schema(self,schema_name:str)->_db_mysql_database_type:
        '''Retrieve a schema[database] instance by its name'''
        if schema_name in self._schemas:
            return self._schemas[schema_name]
        return None

    def get_table(self,table_name:str,schema_name:str=None)->_db_table_type:
        '''
            Get a table instance from the databases
            ----------

            Arguments
            -------------------------
            `table_name` {str}
                The name of the table to search for

            [`schema_name`=None] {str}
                The name of the schema the table must belong to.

            Return {_db_table_type,None}
            ----------------------
            The table instance, if it can be found, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 10:43:22
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table
            * @xxx [12-16-2022 10:44:51]: documentation for get_table
        '''
        if table_name in self._tables:
            return self._tables[table_name]

        if schema_name is not None:
            schema = self.get_schema(schema_name)
            from colemen_utilities.database_utils.MySQL.Table import Table
            if isinstance(schema,Table.Table):
                return schema.get_table(table_name)

        _log(f"Failed to locate table {table_name}, have all the schemas been indexed? call master_index","warning")

    @property
    def tables(self)->Iterable[_db_table_type]:
        '''
            Get all tables being managed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 15:36:52
            `@memberOf`: DatabaseManager
            `@property`: tables
        '''
        value = self._tables.values()
        return value

    @property
    def table_names(self):
        '''
            Get a list of all table names associated to this manager.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 10:54:20
            `@memberOf`: DatabaseManager
            `@property`: table_names
        '''
        
        return self._tables.keys()


    # ---------------------------------------------------------------------------- #
    #                                 RELATIONSHIPS                                #
    # ---------------------------------------------------------------------------- #

    @property
    def relationships(self):
        '''
            Get this DatabaseManager's relationships

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-16-2022 11:01:56
            `@memberOf`: DatabaseManager
            `@property`: relationships
        '''
        value = self._relationships
        return value

    def get_table_children(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that have a foreign key constraint referencing the table provided.

            ----------

            Arguments
            -------------------------
            `table` {str,Table}
                The name of the parent table or the Table instance.


            Return {list}
            ----------------------
            A list of tables associated as children to the table provided.
            
            If None are found, the list is empty.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:56:16
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table_children
            * @xxx [12-16-2022 12:01:52]: documentation for get_table_children
        '''
        table_name = _table_to_name(table)
        tables = []
        rel:_db_relationship_type
        for rel in self._relationships:
            if rel.is_parent(table_name):
                if rel.parent_table_found:
                    tables.append(rel.parent_table)
        return tables

    def get_table_parents(self,table:Union[str,_db_table_type])->Iterable[_db_table_type]:
        '''
            Retrieve a list of tables that the table provided is a child of.

            This means that it has a foreign key constraint referencing the tables returned.

            ----------

            Arguments
            -------------------------
            `table` {str,Table}
                The name of the parent table or the Table instance.


            Return {list}
            ----------------------
            A list of tables associated as parents to the table provided.

            If None are found, the list is empty.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 11:56:16
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: get_table_children
            * @xxx [12-16-2022 12:01:52]: documentation for get_table_children
        '''
        table_name = _table_to_name(table)
        tables = []
        rel:_db_relationship_type
        for rel in self._relationships:
            if rel.is_child(table_name):
                tables.append(rel.table)
        return tables



def _table_to_name(table:Union[str,_db_table_type]):
    '''returns a table name if the table instance is provided.'''
    from colemen_utilities.database_utils.MySQL.Table import Table
    if isinstance(table,Table.Table):
        table = table.name
    return table


def new(**kwargs)->DatabaseManager:
    '''
        Create a new MySQL database connection.

        ----------


        Keyword Arguments
        -------------------------
        `database` {str}
            The name of the database/schema this instance represents.

        `user` {str}
            The user name used to connect to the database.

        `password` {str}
            The password used to connect to the database.

        `host` {str}
            The host address used to connect to the database

        `cache_path` {str}
            The path to the directory where the table cache files can be saved.

        Return {DatabaseManager}
        ----------------------
        The DatabaseManager instance.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-13-2022 12:27:05
        `memberOf`: DatabaseManager
        `version`: 1.0
        `method_name`: new
        * @xxx [12-13-2022 12:29:29]: documentation for new
    '''
    return DatabaseManager(**kwargs)









