# import requests
# from lxml import html

# ticker = "AAPL"
# # Send an HTTP GET request to the URL
# url = f"https://www.gurufocus.com/stock/{ticker}/summary"
# response = requests.get(url)

# tree = html.fromstring(response.content)

# xpath_expression = '//span[@class="t-primary"]/text()'
# key = 'GF Value'

# element = tree.xpath(xpath_expression)

# elements = dict()    
# if element:
#     elements[key] = float(element[0].replace('$',''))
#     print(f"Return on {key} : {elements[key]}")
# else:
#     elements[key]=0
#     print("information not found on the webpage.")


import pandas as pd
import requests

from gurufocus import get_GF_Value
#get ticker list by filtering only above 1 billion dollar company
DFUSA = pd.read_csv(r"\\192.168.1.1\New Volume\storage\premarket\america_2023-12-08.csv")[['Ticker','Price','Market Capitalization','Sector','Industry']]
# DFUSA = pd.read_csv('america_2023-09-16.csv')
tickerlst = list(DFUSA.query('`Market Capitalization`>.1e9').Ticker)
print(f"Number of Tickers: {len(tickerlst)}")

# Main loop to retrieve profitability ranks for each ticker
dfs=[]
counter=0
for ticker in tickerlst:
    counter+=1
    print(f'{counter} out of {len(tickerlst)} {ticker}')
    try:
        # Get profitability rank for the current ticker
        dftemp = pd.DataFrame(get_GF_Value(ticker).values(), columns=['GF Value'])    

        # Add the Ticker column for reference
        dftemp['Ticker'] = ticker
        dfs.append(dftemp)
    except:
        print(f"could not retrieve data for {ticker}")
        pass

# Concatenate the DataFrames in the list to create a single DataFrame    
DFmerge = pd.concat(dfs, ignore_index=True)    
DFtotal = DFmerge.merge(DFUSA)

DFtotal['GFValuediff'] = 100* (DFtotal['GF Value'] - DFtotal['Price']) / DFtotal['Price']
DFtotal.to_csv('GFvalue.csv')
DFtotal.query('`Market Capitalization`>100e9 & `GF Value`>0').sort_values(by='GFValuediff',ascending=True).head(10)