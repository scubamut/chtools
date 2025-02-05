# def explore_nested_json(data, prefix=None, sep='.'):
#     """
#     Recursively explore nested JSON and return flattened key-value pairs
#     with hierarchical keys that can be used as multi-index
#     """
#     items = {}

#     if isinstance(data, dict):
#         for key, value in data.items():
#             new_key = f"{prefix}{sep}{key}" if prefix else key
#             if isinstance(value, (dict, list)):
#                 items.update(explore_nested_json(value, new_key, sep))
#             else:
#                 items[new_key] = value

#     elif isinstance(data, list):
#         for i, value in enumerate(data):
#             new_key = f"{prefix}{sep}{i}" if prefix else str(i)
#             if isinstance(value, (dict, list)):
#                 items.update(explore_nested_json(value, new_key, sep))
#             else:
#                 items[new_key] = value

#     return items

# chtools/ch_utils/explore_nested_json.py
from typing import Dict, Any, List
import logging
import json


def explore_nested_json(
    data: Dict[str, Any],
    logger: logging.Logger,
    indent: int = 0,
    path: str = "",
    limit_string_length: bool = False,
    max_string_length: int = 50,
) -> None:
    """
    Recursively explores a nested JSON (dictionary/list) structure and prints each
     key-value pair with proper indentation.

    Args:
        data: Dictionary of json data
        logger: The logger to log events.
        indent: indentation level. default = 0
        path: the path of keys to reach this element. default is empty
        limit_string_length: if true then strings are printed up to a max length. Default is False.
        max_string_length: The max length to print if limit_string_length is true. Default is 50
    """
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, (dict, list)):
                logger.info("  " * indent + f"{new_path}:")  # Don't display the values for dict or list
                explore_nested_json(value, logger, indent + 1, new_path, limit_string_length, max_string_length)
            else:
                if isinstance(value, str) and limit_string_length:
                    value = value[:max_string_length] + "..." if len(value) > max_string_length else value
                logger.info("  " * indent + f"{new_path}: {value}")
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = f"{path}[{index}]"
            if isinstance(value, (dict, list)):
                logger.info("  " * indent + f"{new_path}:")
                explore_nested_json(value, logger, indent + 1, new_path, limit_string_length, max_string_length)
            else:
                if isinstance(value, str) and limit_string_length:
                    value = value[:max_string_length] + "..." if len(value) > max_string_length else value
                logger.info("  " * indent + f"{new_path}: {value}")
    else:
        if isinstance(data, str) and limit_string_length:
                data = data[:max_string_length] + "..." if len(data) > max_string_length else data
        logger.info("  " * indent + f"{path}: {data}")