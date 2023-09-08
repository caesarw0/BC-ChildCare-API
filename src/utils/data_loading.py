import pandas as pd
import numpy as np

def load_data_from_csv():
    df = pd.read_csv('../data/childcare_locations.csv')
    df.replace({np.NAN: "N/A"}, inplace=True)
    return df