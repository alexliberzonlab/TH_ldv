import re
import pandas as pd
from glob import glob
import numpy as np
import os
from th_ldv import DATA_PATH

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


def extract_date_from_filepath(filepath: str) -> int:
    pattern = r"\d{4}_\d{2}_\d{2}|\d{8}"
    match = re.search(pattern, filepath)
    date_str = match.group()
    date = ""
    for s in date_str.split("_"):
        date += s
    return int(date)


def parse_keyword_vars(keyword: str) -> list:
    """
    Parses the product key (e.g., 'xy') into a list of variables (e.g., ['x', 'y']).
    :param keyword: String, e.g., 'xy'
    :return: List of variables ['x', 'y']
    >>> parse_keyword_vars('xy')
    ['x', 'y']
    >>> parse_keyword_vars('x')
    ['x']
    >>> parse_keyword_vars("x'y'")
    ["x'", "y'"]
    """
    if "'" in keyword:
        keyword = keyword.replace("'", "")
        return [c+"'" for c in list(keyword)]
    return list(keyword)



 
if __name__ == "__main__":
    import doctest
    doctest.testmod()
