import pandas as pd
import pathlib
import json

def get_config(path):
    with open(path, "r") as jsonfile:
        return(json.load(jsonfile))

RAWDATA_PATH = pathlib.Path(r'datasets/raw')


# Belgium
belgium_config = get_config(RAWDATA_PATH / 'belgium.json')
belgium_df = pd.read_csv(RAWDATA_PATH / 'belgium.csv', sep=', ', header=None, engine='python')
belgium_df.columns = belgium_config['column names']

belgium_std_error = belgium_df.loc[belgium_df['payment/revenue'] == 'carbon revenue',
                'price'].std()
print(f"The estimated error (standard deviation) for Belgium is +/- {belgium_std_error:.2f} {belgium_config['info']['unit']}")

print(belgium_df['payment/revenue'].unique())

print(belgium_df.head())
print(belgium_config)
print(belgium_std_error)
