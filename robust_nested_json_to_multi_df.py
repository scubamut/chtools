# def robust_nested_json_to_multi_df(data): 
#     """
#     Convert nested JSON to multi-index DataFrame with clean hierarchical columns
#     """
#     # First get the flattened data
#     flattened_data = []

#     if isinstance(data, dict):
#         flattened_data.append(explore_nested_json(data))
#     elif isinstance(data, list):
#         for item in data:
#             flattened_data.append(explore_nested_json(item))

#     # Create initial DataFrame
#     df = pd.DataFrame(flattened_data)

#     # Convert flat column names to multi-index
#     columns = df.columns
#     index_tuples = [col.split('.') for col in columns]

#     # Get the maximum depth
#     max_depth = max(len(tup) for tup in index_tuples)

#     # Pad shorter tuples with empty strings instead of NaN
#     clean_tuples = [
#         tuple(list(tup) + [''] * (max_depth - len(tup)))
#         for tup in index_tuples
#     ]

#     # Create MultiIndex with cleaned tuples
#     multi_index = pd.MultiIndex.from_tuples(
#         clean_tuples,
#         names=[f'level_{i}' for i in range(max_depth)]
#     )

#     df.columns = multi_index
#     return df

# chtools/ch_utils/robust_nested_json_to_multi_df.py
import pandas as pd
from typing import List, Dict, Any
import logging

def robust_nested_json_to_multi_df(
    data: List[Dict[str, Any]],
    logger: logging.Logger,
    record_path: List[str] = None,
    meta: List[str] = None
) -> Dict[str, pd.DataFrame]:

    import pandas as pd
    from typing import List, Dict, Any
    import logging

    """
    Converts a list of nested JSON objects into multiple Pandas DataFrames.
    Args:
        data: List of nested json data
        logger: The logger to log events.
        record_path: path of record, can be nested path. Default None
        meta: list of meta cols. Default None
    Returns:
        Dictionary of dataframes
    """
    dfs = {}
    if record_path:
        try:
             df_main = pd.json_normalize(data, record_path=record_path, meta=meta)
             dfs['main'] = df_main
        except Exception as e:
            logger.warning(f"Error creating main dataframe: {e}")
    else:
        try:
            df_main = pd.json_normalize(data, meta=meta)
            dfs['main'] = df_main
        except Exception as e:
            logger.warning(f"Error creating main dataframe: {e}")
    
    def _recursive_extract(json_data, path_prefix="", dfs_dict=None):
        """Inner method to recursively extract data into dataframes"""
        if dfs_dict is None:
            dfs_dict = {}
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                current_path = f"{path_prefix}_{key}" if path_prefix else key
                if isinstance(value, list):
                    try:
                        df = pd.json_normalize(value, meta=meta)
                        if not df.empty:
                            dfs_dict[current_path] = df
                            # Recursively explore each list element. For example, multiple dates in a history element
                            for list_element in value:
                                _recursive_extract(list_element, current_path, dfs_dict)
                    except Exception as e:
                        logger.warning(f"Error creating dataframe at {current_path} path: {e}")
                elif isinstance(value, dict):
                        _recursive_extract(value, current_path, dfs_dict)
        elif isinstance(json_data, list):
                for item in json_data:
                    _recursive_extract(item, path_prefix, dfs_dict)
        return dfs_dict
    
    dfs.update(_recursive_extract(data))
    return dfs