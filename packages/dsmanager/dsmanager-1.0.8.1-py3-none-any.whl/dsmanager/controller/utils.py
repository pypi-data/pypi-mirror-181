"""@Author: Rayane AMROUCHE

Utils functions for controller
"""

import os
import json

import __main__ as main

from dsmanager.datamanager.datastorage import DataStorage


def is_interactive() -> bool:
    """Check wether the code is runned on a notebook

    Returns:
        bool: True if runned on notebook, else False
    """
    return not hasattr(main, '__file__')


def json_to_dict(path: str) -> dict:
    """Read a json file as a dict

    Args:
        path (str, optional): Path of the json file to transform as a
            python dict

    Raises:
        FileNotFoundError: Raised if the file is not found

    Returns:
        dict: Json file as a python dict
    """
    # check if file exists
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as outfile:
            json.dump({}, outfile)

    # check if file is a json
    try:
        with open(path, encoding="utf-8") as json_file:
            file_dict = json.load(json_file, object_pairs_hook=DataStorage)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Given file is not a valid json. Details: {exc}"
        ) from exc
    return file_dict
