import re
from io import TextIOWrapper
from typing import Dict, List, Tuple, Union

import pandas as pd


def get_msgType_dict(
    buffer: TextIOWrapper
) -> Tuple[Dict[str, List[str]], List[str]]:

    type_parser = re.compile('"msgType_":(\\d+)')
    msgType = {}
    not_parsed = []
    for line in buffer:
        type_match = type_parser.search(line)
        if type_match:
            type_id = type_match.group(1)

            if type_id not in msgType.keys():
                msgType[type_id] = []

            msgType[type_id].append(type_match.string)
        else:
            not_parsed.append(line)

    return (msgType, not_parsed)


def generate_DataFrame_by_type_id(
    type_id: Union[str, int], input_table: dict[str, List[str]]
) -> pd.DataFrame:
    tmp_output = []
    parse_string, parse_key = generate_parse_key_string(type_id)
    parser = re.compile(parse_string)

    for elements in input_table.get(str(type_id), []):
        match = parser.search(elements)

        if match:
            tmp_dict = {
                key: value for key, value in zip(parse_key, match.groups())
            }
            tmp_output.append(tmp_dict)

    return pd.DataFrame(tmp_output)


def generate_parse_key_string(
    type_id: Union[str, int]
) -> Tuple[str, List[str]]:
    if str(type_id) == '8':
        parse_key = [
            'securityId', 'umtf', 'isin', 'currency', 'mic', 'tickTableId'
        ]
        parse_string = (
            '\"securityId_\"\\:(\\d+),'  # 1
            '\"umtf_\"\\:\"(\\w+)\",'  # 2
            '\"isin_\"\\:\"(\\w+)\",'  # 3
            '\"currency_\"\\:\"(\\w+)\",'  # 4
            '\"mic_\"\\:\"(\\w+)\",'  # 5
            '\"tickTableId_\"\\:(\\d+),'  # 6
        )

    elif str(type_id) == '12':
        parse_key = [
            'securityId', 'side', 'quantity', 'price', 'orderId'
        ]
        parse_string = (
            '\"securityId_\"\\:(\\d+),'  # 1
            '\"side_\"\\:(\\w+),'  # 2
            '\"quantity_\"\\:(\\d+),'  # 3
            '\"price_\"\\:(\\d+),'  # 4
            '\"orderId_\"\\:(\\d+)'  # 5
        )
    else:
        parse_string = ''
        parse_key = []
    return parse_string, parse_key
