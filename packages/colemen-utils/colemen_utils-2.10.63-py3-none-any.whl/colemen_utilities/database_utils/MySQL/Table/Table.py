
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
# import importlib
from dataclasses import dataclass
from posixpath import split
# from typing import List
from typing import Iterable, Union



# import colemen_utilities.database_utils.MySQL.Column.Column as _Column
from colemen_utilities.database_utils.MySQL.Column.Column import Column as _Column
import colemen_utilities.dict_utils as _obj
from colemen_utilities.database_utils.MySQL.Column import column_utils as _u
from colemen_config import _db_column_type,_db_mysql_database_type
from colemen_utilities.database_utils.MySQL import CacheFile as _CacheFile
# import colemen_utilities.database_utils.MySQL.CacheFile as _CacheFile
import colemen_utilities.random_utils as _rand
import colemen_utilities.console_utils as _con
_log = _con.log




@dataclass
class Table:
    database:_db_mysql_database_type = None
    _cache = None

    schema:str = None
    _name:str = None
    _has_deleted_column:bool = None
    _has_timestamp_column:bool = None
    _has_modified_timestamp_column:bool = None
    _has_hash_id:bool = None
    _hash_id_prefix:str = None
    _hash_id_column:_db_column_type = None
    table_catalog = None
    table_schema = None
    table_name = None
    table_type = None
    engine = None
    version = None
    row_format = None
    table_rows = None
    avg_row_length = None
    data_length = None
    max_data_length = None
    index_length = None
    data_free = None
    auto_increment = None
    # create_time = None
    # update_time = None
    # check_time = None
    table_collation = None
    checksum = None
    create_options = None
    table_comment = None
    _cerberus_validations = None



    _Columns = []
    _primary_id = None
    relationships = None
    '''A list of relationship instances that are associated to this table.'''

    def __init__(self,database:_db_mysql_database_type,table_name:str,data:dict = None) -> None:
        '''
            Create a table instance.

            ----------

            Arguments
            -------------------------
            `database` {MySQLDatabase}
                A reference to the Database that this table belongs to.

            `table_name` {str}
                The name of this table.

            `data` {dict}
                A dictionary of table data.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:38:23
            `memberOf`: Table
            `version`: 1.0
            `method_name`: Table
            * @TODO []: documentation for Table
        '''
        self.database:_db_mysql_database_type = database
        self.table_name = table_name
        self._columns = []
        self._has_deleted_column = None
        self._has_timestamp_column = None
        self._has_modified_timestamp_column = None
        self._has_hash_id = None
        self._hash_id_prefix = None
        self._hash_id_column = None

        if data is None:
            data = self.cache.load()
        # if data is None:
        #     data = self.database.get_table_meta_data(self.naem)
        if data is not None:
            populate_from_dict(data,self)

    @property
    def cache(self):
        '''
            Get this Table's cache

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:51:44
            `@memberOf`: Table
            `@property`: cache
        '''
        value = self._cache
        if value is None:
            print(f"table.cache - instantiating cache class")
            value = _CacheFile(self.database,self.database.database,self.table_name)
            value.name = f"{self.database.database}_{self.table_name}"
            self._cache = value
        return value

    def save_cache(self):
        '''Save this table's cache file'''
        self.summary
        self.cache.save()

    @property
    def summary(self):
        '''
            Get the summary property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:10:00
            `@memberOf`: __init__
            `@property`: summary
        '''
        print(f"table.summary - generating summary")
        value = {
            "schema":self.database.database,
            "name":self.table_name,
            "has_deleted_column":self.has_deleted_column,
            "has_timestamp_column":self.has_timestamp_column,
            "has_modified_timestamp_column":self.has_modified_timestamp_column,
            "has_hash_id":self.has_hash_id,
            "hash_id_prefix":self.hash_id_prefix,
            "table_catalog":self.table_catalog,
            "table_schema":self.table_schema,
            "table_name":self.table_name,
            "table_type":self.table_type,
            "engine":self.engine,
            "version":self.version,
            "row_format":self.row_format,
            "table_rows":self.table_rows,
            "avg_row_length":self.avg_row_length,
            "data_length":self.data_length,
            "max_data_length":self.max_data_length,
            "index_length":self.index_length,
            "data_free":self.data_free,
            "auto_increment":self.auto_increment,
            "table_collation":self.table_collation,
            "checksum":self.checksum,
            "table_comment":self.table_comment,
            # "create_options":self.create_options,
            # "create_roles":self.create_roles,
            # "read_roles":self.read_roles,
            # "update_roles":self.update_roles,
            # "delete_roles":self.delete_roles,
            # "blueprint_name":self.blueprint_name,
        }

        # value['relationships'] = [x.summary for x in self.relationships]
        self._cache.set_key("table_data",value)
        value['columns'] = [x.summary for x in self.columns]


        # self._cache.set_key("columns",value['columns'])
        # value['end_points'] = [x.summary for x in self._end_point_docs]
        self._cache.save()
        return value


    def add_column(self,column:Union[dict,_db_column_type]):
        '''
            Register a column instance with this table.

            This does NOT literally add a column to the table in the database.
            ----------

            Arguments
            -------------------------
            `column` {Column,dict}
                The column instance or dictionary of data to register.


            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:35:18
            `memberOf`: Table
            `version`: 1.0
            `method_name`: add_column
            * @xxx [12-13-2022 12:36:52]: documentation for add_column
        '''
        if isinstance(column,(dict)):
            column = _Column(self.database,self,column)
        self._columns.append(column)

    def gen_hash_id(self):
        '''
            Generate a hash_id specific for this table, if the table supports a hash_id column.
            ----------

            Return {str,None}
            ----------------------
            The hash_id if the table supports it, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 12:34:03
            `memberOf`: Table
            `version`: 1.0
            `method_name`: gen_hash_id
            * @xxx [12-13-2022 12:35:06]: documentation for gen_hash_id
        '''
        if self.has_hash_id:
            if self.hash_id_prefix is not None:
                return f"{self.hash_id_prefix}_{_rand.rand((self._hash_id_column.data.character_maximum_length - len(self.hash_id_prefix)))}"


    # ---------------------------------------------------------------------------- #
    #                            COLUMN SUPPORT METHODS                            #
    # ---------------------------------------------------------------------------- #


    @property
    def columns(self)->Iterable[_db_column_type]:
        '''
            Get the columns property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:27:28
            `@memberOf`: __init__
            `@property`: columns
        '''
        value = self._columns
        if len(value) == 0:
            # import traceback
            # traceback.print_stack()
            _log("table.columns - no columns associated to table, requesting data from server.","magenta")
            cols = self.database.get_column_data(self.table_name)
            if isinstance(cols,(list)):
                for col in cols:
                    self.add_column(col)
                    # self.add_column(_column.Column(self.database,self,col))
        return self._columns

    @columns.setter
    def columns(self,value):
        '''
            Set the columns property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-06-2022 12:17:29
            `@memberOf`: __init__
            `@property`: columns
        '''
        self._columns = value

    @property
    def primary_id(self):
        '''
            Get this Table's primary_id column instance

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-13-2022 11:52:51
            `@memberOf`: Table
            `@property`: primary_id
        '''
        value = self._primary_id
        if value is None:
            for col in self.columns:
                if col.data.is_primary:
                    value = col
                    self._primary_id = col
                    break

        return value


    @property
    def foreign_keys(self)->Iterable[_db_column_type]:
        output = []
        col:_db_column_type
        for col in self.columns:
            if col.sql_data.is_foreign_key:
                output.append(col)
        return output

    def get_column_by_name(self,name)->_db_column_type:
        for col in self.columns:
            
            if col.data.column_name == name:
                return col
        return None

    @property
    def name(self)->str:
        '''
            Get the name value.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:40:58
            `@memberOf`: PostArg
            `@property`: name
        '''
        value = self.table_name
        self._name = value

        return value

    @name.setter
    def name(self,value:str):
        '''
            Set the name value.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 09:40:58
            `@memberOf`: PostArg
            `@property`: name
        '''
        self._name = value

    def populate_from_dict(self,data:dict):
        '''Used internally to populate the instance from caches.'''
        populate_from_dict(data,self)

    @property
    def has_deleted_column(self)->bool:
        '''
            Check if this table has a column used for denoting that a row is "deleted".

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_deleted_column
        '''

        for col in self.columns:
            if col.data.is_deleted is True:
                self._has_deleted_column = True

        return self._has_deleted_column

    @has_deleted_column.setter
    def has_deleted_column(self,value):
        '''
            Set the Table's has_deleted_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:49:47
            `@memberOf`: Table
            `@property`: has_deleted_column
        '''
        self._has_deleted_column = value

    @property
    def has_hash_id(self)->bool:
        '''
            Check if this table has a column used storing a hash_id.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_hash_id
        '''
        value = self._has_hash_id
        if value is None:
            for col in self.columns:
                # print(f"col.data:{col.data.summary()}")
                if col.data.is_hash_id is True:
                    self._hash_id_column = col
                    self._has_hash_id = True
                    break
                # self._has_hash_id = value
        return self._has_hash_id

    @has_hash_id.setter
    def has_hash_id(self,value):
        '''
            Set the Table's has_hash_id property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:49:28
            `@memberOf`: Table
            `@property`: has_hash_id
        '''
        self._has_hash_id = value

    @property
    def hash_id_prefix(self):
        '''
            If this table supports a hash_id column this will contain the prefix used to denote the hash_id.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:44:30
            `@memberOf`: Table
            `@property`: hash_id_prefix
        '''

        if self.has_hash_id is False:
            return None

        value = self._hash_id_column.data.hash_id_prefix
        return value

    @hash_id_prefix.setter
    def hash_id_prefix(self,value):
        '''
            Set the Table's hash_id_prefix property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:02
            `@memberOf`: Table
            `@property`: hash_id_prefix
        '''
        self._hash_id_prefix = value

    @property
    def has_timestamp_column(self)->bool:
        '''
            Check if this table has a column used storing a timestamp_column.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_timestamp_column
        '''
        value = self._has_timestamp_column
        if value is None:
            for col in self.columns:
                if col.data.is_timestamp is True:
                    value = True
            self._has_timestamp_column = value
        return value

    @has_timestamp_column.setter
    def has_timestamp_column(self,value):
        '''
            Set the Table's has_timestamp_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:31
            `@memberOf`: Table
            `@property`: has_timestamp_column
        '''
        self._has_timestamp_column = value

    @property
    def has_modified_timestamp_column(self)->bool:
        '''
            Check if this table has a column used storing a modified_timestamp_column.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:36:20
            `@memberOf`: PostArg
            `@property`: has_modified_timestamp_column
        '''
        value = self._has_modified_timestamp_column
        if value is None:
            for col in self.columns:
                if col.data.is_modified_timestamp is True:
                    value = True
            self._has_modified_timestamp_column = value
        return value

    @has_modified_timestamp_column.setter
    def has_modified_timestamp_column(self,value):
        '''
            Set the Table's has_modified_timestamp_column property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 10:50:41
            `@memberOf`: Table
            `@property`: has_modified_timestamp_column
        '''
        self._has_modified_timestamp_column = value

    # def locate_special_columns(self):
    #     for col in self.columns:
    #         if col.data.is_hash_id:
    #             self.has_hash_id = True




    # ---------------------------------------------------------------------------- #
    #                             QUERY SUPPORT METHODS                            #
    # ---------------------------------------------------------------------------- #


    def insert(self,data:dict,**kwargs)->Union[int,dict,bool]:
        '''
            Insert a dictionary of data into this table
            ----------

            Arguments
            -------------------------
            `data` {dict}
                The data to be inserted into this table, where the keys correspond to columns.

            Keyword Arguments
            -------------------------
            [`return_row`=True] {bool}
                If True, the entire row will be retrieved after a successful insertion and returned as a dictionary.

            Return {int,dict,bool}
            ----------------------
            The integer id of the inserted row if successful, False otherwise.

            if return_row is True, the row dictionary is returned.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-13-2022 11:43:55
            `memberOf`: Table
            `version`: 1.0
            `method_name`: insert
            * @TODO []: documentation for insert
        '''
        
        from colemen_utilities.database_utils.MySQL.InsertQuery import InsertQuery
        
        InsertQuery(database=self.database,table=self)
        
        cerberus_validate = _obj.get_kwarg(['cerberus_validate'],False,(bool),**kwargs)
        return_row = _obj.get_kwarg(['return_row'],True,(bool),**kwargs)
        
        result = self.database.insert_to_table(self.table_name,data,cerberus_validate)
        if result:
            if return_row:
                s = self.select_query()
                s.add_where(self.primary_id.name,result,"=")
                result = s.execute()
        return result

    def insert_query(self):
        return self.database.insert_query(self)

    def select_query(self):
        '''Create a new select query instance for this table.'''
        return self.database.select_query(self)

    def update_query(self):
        '''Create a new update query instance for this table.'''
        return self.database.update_query(self)
        # return self.database.update_query(self.table_name)

    def delete_query(self):
        '''Create a new delete query instance for this table.'''
        return self.database.delete_query(self)
        # return self.database.delete_query(self.table_name)

    @property
    def cerberus_validation_schema(self):
        '''
            Get this Table's cerberus_validation_schema

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-12-2022 13:47:07
            `@memberOf`: Table
            `@property`: cerberus_validation_schema
        '''
        value = self._cerberus_validations
        if value is None:
            value = {
                "create":[],
                "read":[],
                "update":[],
                "delete":[],
            }
            col:_db_column_type
            cols = self.columns
            for col in cols:
                value['create'].append(col.validation.cerberus_schema("create"))
                value['read'].append(col.validation.cerberus_schema("read"))
                value['update'].append(col.validation.cerberus_schema("update"))
                value['delete'].append(col.validation.cerberus_schema("delete"))


            self._cerberus_validations = value
        return value


    def create_cerberus_validation_schema(self,**kwargs):
        _obj.get_kwarg(['post_arguments'],False,)

        



def populate_from_dict(data:dict,table:Table):
    columns = None
    table_data = data
    # print(f"table_data: {table_data}")
    if "table_data" in data:
        _log("table.populate.from_dict - table_data key located in data dictionary","info")
        table_data = data['table_data']
        if "columns" in table_data:
            _log("table.populate.from_dict -    columns key located in table_data dictionary","info")
            columns = table_data['columns']
            del table_data['columns']

    if columns is not None:
        _log("table.populate_from_dict - Loading Columns from cache","info")
        for col in columns:
            table.add_column(col)

    for k,v in table_data.items():
        # @Mstep [IF] if the key is for columns skip it
        if k == "columns" and columns is not None:
            _log("table.populate.from_dict -        skipping columns key from table_data dictionary","info")
            continue
        if k == "table_name":
            setattr(table,"name",v)
            # setattr(table,"name",_name.Name(v))
            continue
        if k == "table_schema":
            setattr(table,"schema",v)
            continue

        # @Mstep [IF] if the key is table_comment
        if k == "table_comment":
            # @Mstep [] parse the comment as YAML
            yd = _u.parse_comment_yaml(v)
            if isinstance(yd,(dict)):
                # print(yd)
                # @Mstep [LOOP] iterate the comments keys
                for ck,cv in yd.items():
                    # @Mstep [] assign the comment keys to the table
                    if hasattr(table,ck):
                        setattr(table,ck,cv)
            setattr(table,"table_comment",v)
            continue

        if hasattr(table,k):
            setattr(table,k,v)




