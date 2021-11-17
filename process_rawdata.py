import pandas as pd
import pathlib
import json

def get_config(path):
    with open(path, "r") as jsonfile:
        return(json.load(jsonfile))
DATA_PATH = pathlib.Path(r'datasets')
RAWDATA_PATH = pathlib.Path(r'datasets/raw')
MANDATORY_COLUMNS = ['carbon payment', 'carbon revenue', 'net gain']

def test_data(df):
    EPS = 1.E-0
    for col in MANDATORY_COLUMNS:
        assert(col in df.columns), f"column {col} not present in data, aborting"
    assert df.index.name == "income decile", f"name of index is {df.index}, expecting 'income decile'"
    assert df.index.min() == 1, f"index should start at 1. Index is: {df.index}"
    sum_net_gain = df['net gain'].sum()
    print('Dataframe tested successfully for column names and index')
    print(f"net gain is equal to {sum_net_gain:.3f}")
    if abs(df['net gain'].sum()) > EPS:
        print(f"(Warning, this is not equal to zero!")

# Belgium
column_names = ["bar number", "price", "income decile", "payment/revenue"]
pivot_dict = {"values" : "price",
              "index" : "income decile",
              "columns" : "payment/revenue"}
revenue_column = 'carbon revenue'
payment_column = 'carbon payment'
post_average_column = 'carbon revenue'
net_gain_column = 'net gain'
decile_column = 'income decile'

belgium_metadata = get_config(RAWDATA_PATH / 'belgium.json')
belgium_df = pd.read_csv(RAWDATA_PATH / 'belgium.csv', sep=', ', header=None, engine='python')
belgium_df.columns = column_names
belgium_df[decile_column] = belgium_df[decile_column] + 1
belgium_df = belgium_df.pivot(**pivot_dict)



try:
    belgium_std_error = belgium_df[revenue_column].std()
    belgium_std_mae = (belgium_df[revenue_column] - belgium_df[payment_column] - belgium_df[net_gain_column]).abs().mean()
except KeyError:
    print(f"Warning. Could not find revenue column {revenue_col}. Existing column names: {list(belgium_df.columns)}")

try:
    belgium_df[post_average_column] = belgium_df[post_average_column].mean()
except KeyError:
    print(f"Warning. Could not find column {post_average_column} for revenue averaging. Existing column names: {list(belgium_df.columns)}"\
    "No averaging over deciles was applied")

try:
    belgium_df['calc_tCO2'] = belgium_df[payment_column] / float(belgium_metadata['info']['price'])
except KeyError:
    print(f"Warning. Could not find column '{payment_column}' for calculating effective CO2 emission based on price and payment. "\
    f"Existing column names: {list(belgium_df.columns)}"
    "Not calculating calc_tCO2")

print(f"The estimated error (standard deviation) for Belgium is +/- {belgium_std_error:.2f} {belgium_metadata['info']['price_unit']}")
print(f"The estimated error (MAE) for Belgium is {belgium_std_mae:.3f} {belgium_metadata['info']['price_unit']}")
print(f"Writing Belgium output data to {DATA_PATH / 'belgium.csv'}")
test_data(belgium_df)
belgium_df.to_csv(DATA_PATH / 'belgium.csv')



#UK
uk_df = pd.read_csv(RAWDATA_PATH / 'UK.csv', decimal=',')
unnamed_cols = [col for col in uk_df.columns if 'Unnamed' in col]
# drop all unnamed columns except for Unnamed: 0
uk_df = uk_df.drop(columns=unnamed_cols[1:])
uk_df = uk_df.rename(columns={unnamed_cols[0]:'category'})
uk_df = uk_df.set_index('category')
uk_df = uk_df.T
# bring the deciles back as a column (modifying indices is a pain)
uk_df = uk_df.reset_index()
uk_df = uk_df[uk_df['index'] != 'Total']
uk_df['income decile'] = uk_df['index'].str.extract(r'(\d+)').astype(int)
uk_df = uk_df.set_index('income decile')
uk_df = uk_df.drop(columns=['index'])


uk_df['carbon payment'] = uk_df.iloc[:, :3].sum(axis=1)
uk_df = uk_df.rename(columns={'Household Dividend' : 'carbon revenue'})
uk_df['net gain'] = uk_df['carbon revenue'] - uk_df['carbon payment']
print(uk_df['net gain'])
print(uk_df['net gain'].sum())
test_data(uk_df)
uk_df.to_csv(DATA_PATH / 'uk.csv')
