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
import re
from typing import Union
import colemen_utilities.dict_utils as _obj

def is_email(value:str)->bool:
    if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',value) is None:
        return False
    return True

def alpha_only(value:str)->bool:
    return False if re.match(r'^[a-zA-Z]*$',value) is None else True


def alphanumeric_only(value:str)->bool:
    return False if re.match(r'^[a-zA-Z0-9]*$',value) is None else True

def numeric_only(value:str)->bool:
    return False if re.match(r'^[0-9]*$',value) is None else True

def phone_number(value:str)->bool:
    return False if re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',value) is None else True

# def alpha_only(value:str)->bool:
# def alpha_only(value:str)->bool:

def ip_address(value:Union[str,int])->bool:
    import ipaddress
    try:
        ipaddress.ip_address(value)
        # print("Valid IP Address")
        return True
    except ValueError:
        pass
        # print("Invalid IP Address")
    return False

def future_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the future.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: future_unix
        * @TODO []: documentation for future_unix
    '''
    import time
    return False if value <= time.time() else True

def past_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the past.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: past_unix
        * @TODO []: documentation for past_unix
    '''
    import time
    return False if value >= time.time() else True

def to_hash_id(value:str,prefix:str):
    if prefix not in value:
        value= f"{prefix}_{value}"

def crud_type(value:str):
    valids = ["create","read","update","delete"]
    if value.lower() not in valids:
        return False
    return True


