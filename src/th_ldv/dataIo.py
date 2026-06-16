import pandas as pd
import xarray as xr
import doctest
import os
import re
from th_ldv import DATA_PATH


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ABSOLUTE_PATH = str(DATA_PATH)
data_files = {'ldv': 'LDA', 'ffid': 'PC_LabView'}

# SOURCE LOCATION -1655 -921 -488
Y_SOURCE = -921  # mm
Z_FLOOR = -513 - 65  # mm
Z_SOURCE = -488  # mm
X_SOURCE = -1655  # mm


def get_lda_data_coordinates(path: str) -> tuple:
    """
    Get the coordinates of the LDA data point from the file path.

    Parameters:
    -----------
    path : str
        The file path to the CSV file containing the LDA data.

    Returns:
    --------
    tuple
        The x, y, and z coordinates of the LDA data point.

    Examples:
    ---------
    >>> path = os.path.join(DATA_ABSOLUTE_PATH, r'raw\\2024_11_26\\TH_F0USY25_Zhigh_lpm_000_40hz\\VEL_TH_F0DSY25_Zlow_lpm_000_40hz.000879.txt')
    >>> coords = get_lda_data_coordinates(path)
    """
    meta_data = pd.read_csv(path, nrows=5, header=None)
    x, y, z = [float(re.split(' ', cord)[0]) for cord in re.split(';', meta_data.iloc[3, 0])[1:]]
    return x, y, z


def lda_coordinate_transform(x: float, y: float, z: float) -> tuple:
    """
    Transform the LDA coordinates to the coordinate system used in the thesis.

    Parameters:
    -----------
    x : float
        The x-coordinate of the LDA data.
    y : float
        The y-coordinate of the LDA data.
    z : float
        The z-coordinate of the LDA data.

    Returns:
    --------
    tuple
        The transformed x, y, and z coordinates.

    Examples:
    ---------
    >>> lda_coordinate_transform(X_SOURCE, Y_SOURCE, Z_FLOOR)
    (0, 0, 0)
    >>> lda_coordinate_transform(X_SOURCE, Y_SOURCE, Z_SOURCE)
    (0, 0, 90)
    """
    return x-X_SOURCE, Y_SOURCE-y, z-Z_FLOOR


def load_lda_point(path: str) -> xr.Dataset:
    """
    Load LDA data from a CSV file and return it as an xarray Dataset.

    Parameters:
    -----------
    path : str
        The file path to the CSV file containing the LDA data.

    Returns:
    --------
    xr.Dataset
        An xarray Dataset containing the LDA data with coordinates and variables.

    Examples:
    ---------
    >>> path = os.path.join(DATA_ABSOLUTE_PATH, r'raw\\2024_11_26\\TH_F0USY25_Zhigh_lpm_000_40hz\\VEL_TH_F0DSY25_Zlow_lpm_000_40hz.000879.txt')
    >>> a = load_lda_point(path)
    """
    date = 0
    data = pd.read_csv(path, header=5, index_col=0)
    variables = {
        'w': data['Velocity U [m/s]'],
        'u': data['Velocity V [m/s]'],
        'transit_time': data['Transit Time [us]'],
    }
    t = data['Arrival Time [ms]'] #+ data['Transit Time [us]'] / 2 * 1e-3
    t = t - t.iloc[0]  # remove the first time point
    data_set = xr.Dataset({key: (['time'], variables[key]) for key in variables},
                          coords={'time': t})
    coords = get_lda_data_coordinates(path)
    x, y, z = lda_coordinate_transform(*coords)
    data_set = data_set.assign_coords(x=x, y=y, z=z)
    data_set.attrs["date"] = date
    return data_set



# Run doctests

if __name__ == "__main__":
    doctest.testmod()