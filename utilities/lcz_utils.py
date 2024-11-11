from typing import Literal
import json
import pandas as pd


def convert_LCZ_num_to_class(
    LCZ_num: pd.Series,
    mapper_file_path: str,
) -> pd.Series:
    """
    Convert Local Climate Zone numerical codes `LCZ_num` to their corresponding classes
    using the mapper at `mapper_file_path`. The conversion is based on Ana Oliveira et
    al.'s 2020 work (doi: 10.1016/j.mex.2020.101150).

    Parameters:
    ----------
    LCZ_num : pd.Series
        The LCZ numerical codes to be converted.

    mapper_file_path : str, optional
        File path to the JSON file that maps LCZ numerical codes to classes.

    Returns:
    -------
    pd.Series
        The LCZ classes associated with the input LCZ numerical codes.

    Raises:
    ------
    FileNotFoundError
        If the JSON mapper file is not found at the specified path.
    JSONDecodeError
        If the JSON file is malformed or cannot be decoded.
    """

    # Get dictionary map between LCZ numerical codes and classes
    with open(mapper_file_path, "r") as file:
        LCZ_num_to_class = json.load(
            file,
            object_hook=lambda dct: {int(key): value for key, value in dct.items()},
        )

    # Map LCZ numerical codes into classes
    LCZ_class = LCZ_num.map(LCZ_num_to_class)

    return LCZ_class


def load_LCZ_class_palette(
    mapper_file_path: str,
) -> dict:
    """
    Load the color palette for Local Climate Zone classes from a JSON file. This palette
    has been taken from QGIS software.

    Parameters
    ----------
    mapper_file_path : str
        The path to a JSON file containing the mapping of LCZ classes to their color
        values.

    Returns
    -------
    dict
        A dictionary where keys are LCZ classes and values are color codes.

    Raises
    ------
    FileNotFoundError
        If the specified JSON file does not exist at the given path.
    JSONDecodeError
        If the JSON file is malformed or cannot be decoded.
    """

    # Get color palette for the LCZ classes
    with open(mapper_file_path, "r") as file:
        LCZ_class_to_palette = json.load(file)

    return LCZ_class_to_palette


def get_LCZ_order(
    LCZ: pd.Series,
    mapper_file_path: str,
    LCZ_kind: Literal["num", "class"] = "class",
) -> list:
    """
    Retrieve an ordered list of unique Local Climate Zone values from the issued `LCZ`.
    The order would be in accordance with the one of the number-to-class mapper found at
    `mapper_file_path`.

    Parameters
    ----------
    LCZ : pd.Series
        The LCZ values, either as numerical codes or classes.
    mapper_file_path : str
        The path to a JSON file containing the mapping between LCZ numerical codes
        and their respective classes.
    LCZ_kind : Literal["num", "class"], optional
        The kind of Local Climate Zone values associated with the issued `LCZ`:
        - `"num"`: if numerical codes.
        - `"class"`: if classes (default).

    Returns
    -------
    list
        An ordered list of unique LCZ values from the input `LCZ`, ordered according to
        the mapping in `mapper_file_path`.

    Raises
    ------
    FileNotFoundError
        If the specified JSON file does not exist.
    JSONDecodeError
        If the JSON file is malformed or cannot be decoded.
    ValueError
        If `LCZ_kind` is not one of the specified valid options: "num" or "class".
    """

    # Get dictionary map between LCZ numerical codes and classes
    with open(mapper_file_path, "r") as file:
        LCZ_num_to_class = json.load(
            file,
            object_hook=lambda dct: {int(key): value for key, value in dct.items()},
        )

    # Get unique values of the given LCZ
    LCZ_unique = LCZ.unique()

    # Get reference LCZ values as stated in the mapper
    match LCZ_kind:
        case "num":
            LCZ_ref = LCZ_num_to_class.keys()
        case "class":
            LCZ_ref = LCZ_num_to_class.values()
        case _:
            ValueError('Error: LCZ_kind must be "num" or "class"')

    # Define a list of unique values of the given LCZ, ordered as in the mapper
    LCZ_order = [LCZ for LCZ in LCZ_ref if LCZ in LCZ_unique]

    return LCZ_order
