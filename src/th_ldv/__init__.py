# from .dataset_accesor import TurbAccessor
from pathlib import Path
import pandas as pd
import xrturb

# from .spectra import non_uniform_spectra

PKG_PATH = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PKG_PATH / "data"
DATA_LST = pd.read_csv(DATA_PATH / "velocity_files.csv")