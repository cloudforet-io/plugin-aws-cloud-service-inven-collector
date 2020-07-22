import re
from dataclasses import dataclass
from functools import partial
from typing import List


def make_snake_name(str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def make_simple_type(type_name, match):
    field = match.group(1)
    snake_field = make_snake_name(field)
    return f"""\n'{field}':'{snake_field} = {type_name}(deserialize_from="{field}")'"""


def make_choice_string_type(match):
    field = match.group(1)
    snake_field = make_snake_name(field)
    raw_choices = match.group(2).split('|')
    chocies = ",".join([c.replace("'", '"') for c in raw_choices])
    return f"""\n'{field}':'{snake_field} = StringType(deserialize_from="{field}",choices=[{chocies}])'"""


prefix_re = "\s*'(\w+)'\s?:\s?"
boolean_re = re.compile(f"{prefix_re}True\s?\|\s?False")
int_re = re.compile(f"{prefix_re}123")
float_re = re.compile(f"{prefix_re}123.0")
datetime_re = re.compile(f"{prefix_re}datetime\(.*\)")
string_re = re.compile(f"{prefix_re}'string'")
choice_string_re = re.compile(f"{prefix_re}(('[\w\d\.\-\_]+'\|?)+)")


def make_list_type(type_name, match):
    field = match.group(1)
    snake_field = make_snake_name(field)
    return f"""\n'{field}':'{snake_field} = ListType({type_name},deserialize_from="{field}")'"""


list_string_re = re.compile(f"{prefix_re}(\[\n\s*(('string')|(('[\w\d\.]+')\|?)+),\n\s*\])")
list_int_re = re.compile(f"{prefix_re}(\[\n\s*123,\n\s*\])")
list_float_re = re.compile(f"{prefix_re}(\[\n\s*123.0,\n\s*\])")


@dataclass
class Model:
    raw: str
    class_name: str


model_intro_re = re.compile("\s*'(\w+)'\s?:\s?\{")
model_in = re.compile("((\s*\{)|(\s*'(\w+)'\s?:\s?\{))")
model_end = re.compile('\s*\},?\s*')
list_in = re.compile("((\s*\[)|(\s*'(\w+)'\s?:\s?\[))")
list_end = re.compile('\s*\],?\s*')


def make_choice_string_type(match):
    field = match.group(1)
    snake_field = make_snake_name(field)
    raw_choices = match.group(2).split('|')
    chocies = ",".join([c.replace("'", '"') for c in raw_choices])
    return f"""\n'{field}':'{snake_field} = StringType(deserialize_from="{field}",choices=({chocies}))'"""


def find_model(text):
    result = []
    models = []

    is_in_model = False
    model_buffer = []
    nested_count = 0
    model_name = ''

    raw = text.split('\n')
    for l in raw:
        if is_in_model:
            if model_in.match(l):
                nested_count += 1
            elif (nested_count >= 1) & (model_end.match(l) is not None):
                nested_count -= 1
            elif model_end.match(l):
                model_buffer.append(l)
                models.append(Model('\n'.join(model_buffer), model_name))
                snake_field = make_snake_name(model_name)
                result.append(
                    f"""'{model_name}':'{snake_field} = ModelType({model_name},deserialize_from="{model_name}")',""")

                # reset temp model
                is_in_model = False
                continue
            model_buffer.append(l)
        else:
            if match := model_intro_re.match(l):
                is_in_model = True
                model_name = match.group(1)
                model_buffer = ['{']
            else:
                result.append(l)
    result = '\n'.join(result)

    return result, models


list_model_re = re.compile("'\w+'\s?:\s?\[\n\s*\{\s*(?:\n\s*.*)+?\s*\n\s*\},\s*\n\s*?\]")
list_model_parse_re = re.compile("""'(\w+)'\s?:\s?\[\n\s*(\{\s*(?:\n\s*.*)+\s*\n\s*\}),\s*\n\s*?\]""")


def normalize(class_name, text, _models: list = None):
    models = _models or []
    result, __models = find_model(text)
    models += __models

    pre_models = []
    for m_text in list_model_re.findall(result):
        origin = m_text
        match = list_model_parse_re.match(m_text)
        field = match.group(1)
        _klass_name = class_name + field
        snake_field = make_snake_name(field)
        _klass, __models = normalize(_klass_name, match.group(2))
        pre_models.append(_klass)
        models += __models
        result = result.replace(origin,
                                f"""'{field}':'{snake_field} = ListType(ModelType({_klass_name},deserialize_from="{field}"))'""")

    pre_models = '\n\n'.join(pre_models)

    result = boolean_re.sub(partial(make_simple_type, 'BooleanType'), result)
    result = float_re.sub(partial(make_simple_type, 'FloatType'), result)
    result = int_re.sub(partial(make_simple_type, 'IntType'), result)
    result = string_re.sub(partial(make_simple_type, 'StringType'), result)
    result = choice_string_re.sub(make_choice_string_type, result)
    result = datetime_re.sub(partial(make_simple_type, 'DateTimeType'), result)

    result = list_int_re.sub(partial(make_list_type, 'FloatType'), result)
    result = list_int_re.sub(partial(make_list_type, 'IntType'), result)
    result = list_string_re.sub(partial(make_list_type, 'StringType'), result)

    if result[-1] == ',':
        result = result[:-1]
    print(result)
    parse: dict = eval(result.strip())
    fields = '\n    '.join([x for x in parse.values()])
    klass = f"{pre_models}\n\nclass {class_name}(Model):\n    {fields}"

    return klass, models


def make_models(models: List[Model]):
    result = ''
    for model in models:
        _klass, _models = normalize(model.class_name, model.raw)
        result = f"{result}\n{make_models(_models)}\n{_klass}"

    return result


sample_simple = '''
{
    'ErrorCode': 123,
    'ResponsePagePath': string,
    'ResponseCode': string,
    'ErrorCachingMinTTL': 123,
    'Enabled': True|False,
    'Forward': 'none'|'whitelist'|'all',
    'AAtACXDest': True|False
}'''

sample_list = '''
{
    'ErrorCode': 123,
    'ResponsePagePath': 'string',
    'ResponseCode': 'string',
    'ErrorCachingMinTTL': 123,
    'Enabled': True|False,
    'Forward': 'none'|'whitelist'|'all',
    'AAtACXDest': True|False,
    'Items': [
        'string',
    ],
    'NumList': [
        123,
    ],
}'''
sample_nest_model = '''
{
    'Headers': {
                 'Quantity': 123,
                 'Items': [
                     'string',
                 ]
             },
    'Arc': string,
}
'''

sample_list_model = '''
{
    'Distribution': {
        'ActiveTrustedSigners': {
            'Enabled': True|False,
            'Quantity': 123,
            'Items': [
                {
                    'AwsAccountNumber': 'string',
                    'KeyPairIds': {
                        'Quantity': 123,
                        'Items': [
                            'string',
                        ]
                    }
                },
            ]
        },
        'InProgressInvalidationBatches': 123,
    }
}
 '''

list_model_in_list_model = '''
{
    'NodeGroups': [
        {
            'NodeGroupId': 'string',
            'Status': 'string',
            'PrimaryEndpoint': {
                'Address': 'string',
                'Port': 123
            },
            'ReaderEndpoint': {
                'Address': 'string',
                'Port': 123
            },
            'Slots': 'string',
            'NodeGroupMembers': [
                {
                    'CacheClusterId': 'string',
                    'CacheNodeId': 'string',
                    'ReadEndpoint': {
                        'Address': 'string',
                        'Port': 123
                    },
                    'PreferredAvailabilityZone': 'string',
                    'CurrentRole': 'string'
                },
            ]
        },
    ],
}
 '''

first = '''
import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)
'''

last = '''
    reference = ModelType(ReferenceModel, serialize_when_none=False)

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/"
        }'''
if __name__ == '__main__':
    # klass, models = normalize('SampleData', sample_simple)
    #
    # print(klass)
    #
    # klass, models = normalize('ListData', sample_list)
    # print(klass)
    # print('origin')
    # print(sample_nest_model)
    # klass, models = normalize('ModelData', sample_nest_model)
    # print('to class')
    # print(f"{make_models(models)}\n\n{klass}")

    # print('origin')
    # print(sample_list_model)
    # klass, models = normalize('ListModelData', sample_list_model)
    # print('to class')
    # print(f"{make_models(models)}\n\n{klass}")

    # print('origin')
    # print('NOT SUPPORT LIST>Model>List> Model')
    # print(list_model_in_list_model)
    # klass, models = normalize('ListModelListModelData', list_model_in_list_model)
    # print('to class')
    # print(f"{make_models(models)}\n\n{klass}")

    data ='''{
            'Path': 'string',
            'UserName': 'string',
            'UserId': 'string',
            'Arn': 'string',
            'CreateDate': datetime(2015, 1, 1),
            'PasswordLastUsed': datetime(2015, 1, 1),
            'PermissionsBoundary': {
                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                'PermissionsBoundaryArn': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },'''
    print('origin')
    print(data)
    klass, models = normalize('User', data)
    print('to class')
    print(f"{first}{make_models(models)}{klass}{last}")
