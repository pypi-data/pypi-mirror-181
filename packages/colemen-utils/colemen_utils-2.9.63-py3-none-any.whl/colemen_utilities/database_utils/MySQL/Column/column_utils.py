# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import re

import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import yaml












def parse_comment_yaml(contents:str):

    # contents = contents.replace("\n","   ")
    contents = contents.replace("desc:","description:")
    contents = contents.replace("opts:","options:")
    contents = contents.replace("o:","options:")

    # contents = contents.replace("options:","options:\n")



    if len(contents) > 0:
        if contents.startswith("description:") is False:
            contents = f"description: {contents}"

        if "description:" not in contents:
            contents = f"description: {contents}"
    else:
        return None

    # @Mstep [] force a space between a dash and alphanum characters.
    contents = re.sub(r"\n-([a-zA-Z0-9])",r"\n- \1",contents)

    # c.con.log(f"contents: {contents}","red")
    contents = contents.replace("__%0A__","\r\n")
    data = yaml.safe_load(contents)
    output = {}
    if "description" in data:
        output['description'] = data['description']

    if "options" in data:
        # output['options'] = data['options']
        if isinstance(data['options'],(dict)):
            flattend = _obj.flatten(data['options'],'','_')
            flattend = _obj.keys_to_snake_case(flattend)
            # print("\n\n\n")
            # print(flattend)
            # print("\n\n\n")
            output = {**output,**flattend}
            return output
        if data['options'] is not None:
            for o in data['options']:
                if isinstance(o,(str)):
                    output[_csu.to_snake_case(o)] = True
                if isinstance(o,(dict)):
                    for k,v in o.items():
                        # k = _csu.to_snake_case(k)
                        output[_csu.to_snake_case(k)] = v
    # print(output)
    return output


def sql_type_to_python_type(value:str)->str:
    '''
        Convert an SQL type to its PHP equivalent.
        ----------

        Arguments
        -------------------------
        `value` {str}
            The SQL type to convert.


        Return {str}
        ----------------------
        The converted type string, or the original string if no conversion occurred.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 11-27-2022 19:23:42
        `memberOf`: __init__
        `version`: 1.0
        `method_name`: sql_type_to_python_type
        * @xxx [11-27-2022 19:24:14]: documentation for sql_type_to_python_type
    '''
    if value in ["decimal","float"]:
        return "float"
    elif value in ["bigint","int","integer"]:
        return "integer"
    elif value in ["tinyint"]:
        return "boolean"
    elif value in ["varchar"]:
        return "string"
    elif value in ["timestamp"]:
        return "string"
    else:
        return value










