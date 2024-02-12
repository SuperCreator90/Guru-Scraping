import numpy as np
import pandas as pd
import requests
import os 
from datetime import datetime

from gurufocus import get_all_ratio
from gurufocus import get_GF_Value

# Get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create the gurufocus folder if it doesn't exist
if not os.path.exists('gurufocus'):
    os.makedirs('gurufocus')

#get ticker list by filtering only above 1 billion dollar company
DFUSA = pd.read_csv('america_2023-09-16.csv')
tickerlst = list(DFUSA.query('`Market Capitalization`>1e9').Ticker)
print(f"Number of Tickers: {len(tickerlst)}")

# Main loop to retrieve profitability ranks for each ticker
dfs=[]
counter=0
for ticker in tickerlst:
    counter+=1
    print(f'{counter} out of {len(tickerlst)} {ticker}')
    try:
        # Get profitability rank for the current ticker
        dftemp = get_all_ratio(ticker)
        
        # Add the Ticker column for reference
        dftemp['Ticker'] = ticker
        dfs.append(dftemp)
    except:
        print(f"could not retrieve data for {ticker}")
        pass

# Concatenate the DataFrames in the list to create a single DataFrame    
DFtotal = pd.concat(dfs, ignore_index=True)    
# DFtotal.to_csv(f'gurufocus/DFtotal_{current_datetime}.csv',index=False)

# Function to check if a string can be converted to a number to remove it
def is_convertible_to_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Filter out rows where the 'Name' column cannot be converted to a number; first table made this error    
df_filtered = DFtotal[~DFtotal['Name'].apply(is_convertible_to_number)]
# df_filtered.Name.unique()

df_filtered = df_filtered.drop_duplicates(subset=['Ticker', 'Name'])
# Using pivot method to rearrange the data
DFfinal = df_filtered.pivot(index='Ticker',columns='Name', values='Current')
DFfinal = DFfinal.reset_index()
# Save the final DataFrame to a CSV file
# DFfinal.to_csv(f'gurufocus/GuruFocus_{current_datetime}.csv')

DFfinal_merged= pd.merge(DFfinal,DFUSA[['Ticker','Market Capitalization','Industry','Sector']],on='Ticker')

#Fixing non-value items

# Define a function to replace non-float strings with NaN
def replace_non_float_with_nan(value):
    if isinstance(value, str) and not value.replace(".", "", 1).isdigit():
        return np.nan
    return value

# Apply the function to the entire DataFrame
# df = DFfinal_merged.applymap(replace_non_float_with_nan)
# Apply the function to the specific column "Column1"
df = DFfinal_merged.copy()
for column in DFfinal_merged:
    if column not in ['Ticker', 'Sector' , 'Industry']:
        df[column] = DFfinal_merged[column].apply(replace_non_float_with_nan)
        
df.to_csv(f'gurufocus/GuruFocus_merged_{current_datetime}.csv',index=False)
