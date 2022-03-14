import re
from io import TextIOWrapper
from typing import Dict, List, Tuple, Union

import pandas as pd


def get_msgType_dict(
    buffer: TextIOWrapper
) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    get_msgType_dict generates a dictionary using the msgType as key, and
    populating a list with all the messages of such type.
    It also returns a list with all messages not parsed as specific type
    (in this example mostly timestamps)

    Parameters:

        - buffer: file buffer generated as with open() construct
    """

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
    """
    Provided an Id for the type of messages required, this functions
    returns a DataFrame with the relevant columns.

    Parameters:

        - type_id: the id to use
        - input_table: the table of messages generated with `get_msgType_dict`
    """

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
    """
    Utility function which return useful entities to parse in the messages.
    This functions is generated by analysing by hand the messages of type = 8 and = 12.
    Since the regex expression are very restrictive any changes in the messages may render this function
    worthless. BE AWARE.

    Parameters:

        - type_id: the id to use
    """
    if str(type_id) == '8':
        parse_key = [
            'securityId', 'umtf', 'isin', 'currency', 'mic', 'tickTableId'
        ]
        parse_string = (
            '\"securityId_\"\\:(\\d+),'  # 1st group
            '\"umtf_\"\\:\"(\\w+)\",'  # 2nd
            '\"isin_\"\\:\"(\\w+)\",'  # 3rd
            '\"currency_\"\\:\"(\\w+)\",'  # 4th
            '\"mic_\"\\:\"(\\w+)\",'  # 5th
            '\"tickTableId_\"\\:(\\d+),'  # 6th
        )

    elif str(type_id) == '12':
        parse_key = [
            'securityId', 'side', 'quantity', 'price', 'orderId'
        ]
        parse_string = (
            '\"securityId_\"\\:(\\d+),'  # 1st
            '\"side_\"\\:(\\w+),'  # 2nd
            '\"quantity_\"\\:(\\d+),'  # 3rd
            '\"price_\"\\:(\\d+),'  # 4th
            '\"orderId_\"\\:(\\d+)'  # 5th
        )
    else:
        parse_string = ''
        parse_key = []
    return parse_string, parse_key
