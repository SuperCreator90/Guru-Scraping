
#Get rank of a ticker from tiprank.com uisng pure lxml
def get_tiprank_value(ticker):
    import requests
    from lxml import html

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
    }
    xpath_expression = '//*[@id="tr-stock-page-content"]/div[1]/div[4]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[1]/svg/text/tspan'
    
    # # Send an HTTP GET request to the URL
    url = f"https://www.tipranks.com/stocks/{ticker.lower()}"
    response = requests.get(url, headers=headers)

    elements = dict()    
    key = 'SmartScore'

    if response.status_code == 200:
        tree = html.fromstring(response.content)

        tspan_element = tree.find('.//tspan')
        if tspan_element is not None:
            tspan_element = tree.find('.//tspan', tspan_element)
            elements[key] = tspan_element.text
        else:
            print("tspan element not found.")
            elements[key]="-1"

    return elements



#Get rank and price target of a ticker from tiprank.com using beautifulsoup
def get_tiprank_values(ticker):

    from bs4 import BeautifulSoup
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
    }

    # # Send an HTTP GET request to the URL
    url = f"https://www.tipranks.com/stocks/{ticker.lower()}"
    response = requests.get(url, headers=headers)

    elements = dict()    
    key = 'SmartScore'

    # key = list(xpathdict.keys())[0]

    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Use CSS selector to extract the value
        elements['AveragePriceTarget'] = float(soup.select_one('.colorblack.fonth10_semibold').text[1:])
        elements['SmartScore'] = int(soup.select_one('.w_pxsmall60.mxauto.fontWeightbold.fontSizelarge').text)

    return elements


###############################################################################
#Main Loop
###############################################################################

import pandas as pd
import requests
import time
import os
from datetime import datetime

#get ticker list by filtering only above 1 billion dollar company
DFUSA = pd.read_csv(r"\\192.168.1.1\New Volume\storage\premarket\america_2024-02-09.csv")[['Ticker','Price','Market Capitalization','Sector','Industry']]
# DFUSA = pd.read_csv('america_2023-09-16.csv')
tickerlst = list(DFUSA.query('`Market Capitalization`>1e9').Ticker)
print(f"Number of Tickers: {len(tickerlst)}")

# Main loop to retrieve profitability ranks for each ticker
dfs=[]
counter=0
for ticker in tickerlst:
    counter+=1
    print(f'{counter} out of {len(tickerlst)} {ticker}')
    if '/' in ticker:
        pass
    # try:
    # Get profitability rank for the current ticker
    # value = "-1"
    # while value == "-1":
    #     valuedic = get_tiprank_value(ticker)
    #     value = valuedic['rank']

    try:
        time.sleep(15)  # Pause for 15 seconds
        # dftemp = pd.DataFrame(get_tiprank_value(ticker).values(), columns=['SmartScore'])    
        dftemp = pd.DataFrame([get_tiprank_value(ticker)])

        # Add the Ticker column for reference
        dftemp['Ticker'] = ticker
        dfs.append(dftemp)
    except:
        print(f"could not retrieve data for {ticker}")
        pass

# Concatenate the DataFrames in the list to create a single DataFrame    
DFmerge = pd.concat(dfs, ignore_index=True)    
DFtotal = DFmerge.merge(DFUSA)

DFtotal['AveragePriceTarget_percent'] = 100 * (DFtotal['AveragePriceTarget'] - DFtotal['Price']) /DFtotal['Price']


if not os.path.exists('./tipranks'):
    os.mkdir('tipranks')
    
current_datetime = datetime.now().strftime("%Y-%m-%d")    
DFtotal.to_csv(rf'.\tipranks\tipranks_{current_datetime}.csv' , index=False)


# Fill NaN values with 0 and convert the column to integer
# DFtotal['SmarrtScore'] = DFtotal['SmarrtScore'].fillna(0).astype(int)

#or re-read it
DFtotal = pd.read_csv(rf'.\tipranks\tipranks_{current_datetime}.csv')
DFtotal.query('`Market Capitalization`>1e9 & `SmartScore`>0').sort_values(by='SmartScore',ascending=True).head(20)


#Merging with Gurufocus
DFgurufocus = pd.read_csv(rf'.\gurufocus\GuruFocus_merged_{current_datetime}.csv')[['Ticker' , 'GFValue']] # , 'GFValuediff']]
DFmerge_tipranks_gurufocus = DFgurufocus.merge(DFtotal)

if not os.path.exists(f'.\gurufocus_tipranks'):
    os.mkdir(f'.\gurufocus_tipranks')
DFmerge_tipranks_gurufocus.to_csv(f'.\gurufocus_tipranks\DFmerge_tipranks_gurufocus.csv_{current_datetime}.csv',index=False)


# list(DFmerge_tipranks_gurufocus.query('SmartScore>8 & GFValuediff>25 & `Market Capitalization`>10e9').Ticker)
# DFmerge_tipranks_gurufocus.query('SmartScore>8 & GFValuediff>25 & `Market Capitalization`>25e9')

# DFmerge_tipranks_gurufocus.query('Ticker == "AEP"').T
# DFmerge_tipranks_gurufocus.query('Ticker == "FIS"').T

# DFmerge_tipranks_gurufocus.query('SmartScore>9 & GFValuediff>25 & `Market Capitalization`>10e9')