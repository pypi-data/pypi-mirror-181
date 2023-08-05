"""
Methods related with dicts management
"""


def clean_dict(data_dict: dict) -> dict:
    """
    Delete key from a dict where value is None

    Example:
    clean_dict({"id": "123", "field": None}) -> {"id": "123"}

    :param data_dict: dictionary to clean

    :return: dictionary with cleaned key-values

    """
    return_dict: dict = dict()
    for key, value in data_dict.items():
        if value:
            return_dict[key] = value

    return return_dict
