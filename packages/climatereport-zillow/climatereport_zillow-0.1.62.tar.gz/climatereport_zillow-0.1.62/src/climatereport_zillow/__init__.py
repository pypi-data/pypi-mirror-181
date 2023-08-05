import pandas as pd
import os

# read version from installed package
from importlib.metadata import version
__version__ = version("climatereport_zillow")


dir_path = os.path.dirname(os.path.realpath(__file__))
def get_file(name):
    return pd.read_csv(f"{dir_path}/data/{name}.csv")


fire_zip_file = get_file('fsf_fire_zcta_summary')
heat_zip_file = get_file('fsf_heat_zcta_summary')
flood_zip_file = get_file('fsf_flood_zcta_summary')

fire_state_file = get_file('fsf_fire_state_summary')
heat_state_file = get_file('fsf_heat_state_summary')
flood_state_file = get_file('fsf_flood_state_summary')