
#getting GF value
def get_GF_Value(ticker):
    import requests
    from lxml import html

    # Send an HTTP GET request to the URL
    url = f"https://www.gurufocus.com/stock/{ticker}/summary"
    response = requests.get(url)

    tree = html.fromstring(response.content)

    xpath_expression = '//span[@class="t-primary"]/text()'
    key = 'GF Value'

    element = tree.xpath(xpath_expression)

    elements = dict()    
    if element:
        elements[key] = float(element[0].replace('$',''))
        print(f"Return on {key} : {elements[key]}")
    else:
        elements[key]=0
        print("information not found on the webpage.")

    return elements


#getting some ratio (specified in get_xhtml dict) from gurufocus website by providing xhtml 
def get_ratio_gurufocus(ticker):

    import requests
    from lxml import html

    from get_xhtml import ProfitabilityRank
    # Send an HTTP GET request to the URL
    url = f"https://www.gurufocus.com/stock/{ticker}/summary"
    response = requests.get(url)

    tree = html.fromstring(response.content)
    #xhtml for ROE
    # xpath_expression = '//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[4]/td[3]/span/span' #'//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[4]/td[2]/a'
    # roe_element = tree.xpath(xpath_expression)
    
    #getting xhtml for different ratio of gurufocus website
    elements = dict()
    for key,value in ProfitabilityRank.items():
        xpath_expression = value
        element = tree.xpath(xpath_expression)
        
        if element:
            elements[key] = element[0].text.strip()
            print(f"Return on {key} : {elements[key]}")
        else:
            elements[key]=''
            print("information not found on the webpage.")

    return elements
#get_ratio_gurufocus(ticker="NKE")    


#getting some ratio (profitability_rank section) from gurufocus website by providing xhtml 
def get_profitability_rank(ticker):
    
    import requests
    import pandas as pd
    from lxml import html

    # Construct the URL for the GuruFocus summary page of the given ticker
    url = f"https://www.gurufocus.com/stock/{ticker}/summary"
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the response
    tree = html.fromstring(response.content)
    
    # Define the XPath expression to locate the desired element
    xpath_expression = '//*[@id="financial-strength"]/div[2]/div[1]'
    
    # Use the XPath expression to find the element
    selected_element = tree.xpath(xpath_expression)
    
    # Extract and clean the text content of the selected element
    element_text = selected_element[0].text_content().strip()
    
    # Split the text by newline characters and remove empty strings
    data = [x.strip() for x in element_text.split('\n') if x.strip()]
    
    # Extract the relevant data by skipping the first two lines
    relevant_data = data[2:]
    
    # Separate the first two items as column headers and the rest as values
    columns = relevant_data[0:2]
    your_list = relevant_data[4:]
    
    # Create a list of tuples where each tuple contains two consecutive items from your_list
    pairs = [(your_list[i], your_list[i+1]) for i in range(0, len(your_list), 2)]
    
    # Create a DataFrame from the list of pairs with appropriate column names
    df = pd.DataFrame(pairs, columns=columns)
    
    # Return the resulting DataFrame containing profitability rank information
    return df


#getting some ratio from gurufocus website by providing xhtml by table name
def get_table_gurufocus(ticker,tablename):
    #table name should be one of 
    # FinancialStrength
    # GrowthRank
    # MomentumRank
    # LiquidityRatio
    # DividendBuyBack
    # ProfitabilityRank
    # GFValueRank

    from get_xhtml import gurufocusSummeryTable
    
    import requests
    import pandas as pd
    from lxml import html
    
    # Construct the URL for the GuruFocus summary page of the given ticker
    url = f"https://www.gurufocus.com/stock/{ticker}/summary"
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the response
    tree = html.fromstring(response.content)
    
    # Define the XPath expression to locate the desired element
    xpath_expression = f'//*[@id="financial-strength"]/div[{gurufocusSummeryTable[tablename][0]}]/div[{gurufocusSummeryTable[tablename][1]}]'
    
    # Use the XPath expression to find the element
    selected_element = tree.xpath(xpath_expression)
    
    # Extract and clean the text content of the selected element
    element_text = selected_element[0].text_content().strip()
    
    # Split the text by newline characters and remove empty strings
    data = [x.strip() for x in element_text.split('\n') if x.strip()]
    
    # Extract the relevant data by skipping the first two lines
    if gurufocusSummeryTable[tablename][1]>3:
        relevant_data = data[1:]
    else:
        relevant_data = data[2:]


    
    # Separate the first two items as column headers and the rest as values
    columns = relevant_data[0:2]
    your_list = relevant_data[4:]
    
    # Create a list of tuples where each tuple contains two consecutive items from your_list
    pairs = [(your_list[i], your_list[i+1]) for i in range(0, len(your_list), 2)]
    
    # Create a DataFrame from the list of pairs with appropriate column names
    df = pd.DataFrame(pairs, columns=columns)
    
    # Return the resulting DataFrame containing profitability rank information
    return df

# get_table_gurufocus(ticker='NKE',tablename='FinancialStrength')


#get all five ratio from gurufocus and return as dataframe
def get_all_ratio(ticker):

    import requests
    import pandas as pd
    from lxml import html
    
    # Construct the URL for the GuruFocus summary page of the given ticker
    url = f"https://www.gurufocus.com/stock/{ticker}/summary"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the response
    tree = html.fromstring(response.content)

    xpath_expression = '//span[@class="t-primary"]/text()'
    key = 'GF Value'

    element = tree.xpath(xpath_expression)

    elements = dict()    
    if element:
        elementsvalue = float(element[0].replace('$',''))
    else:
        elementsvalue=0


    dfs = []
    for i in range(1,3):
        for j in range(1,6):
            if ((i==1) or (i==2 and j<3)):
                # Define the XPath expression to locate the desired element
                xpath_expression = f'//*[@id="financial-strength"]/div[{i}]/div[{j}]'
                # Use the XPath expression to find the element
                selected_element = tree.xpath(xpath_expression)

                # Extract and clean the text content of the selected element
                element_text = selected_element[0].text_content().strip()

                # Split the text by newline characters and remove empty strings
                data = [x.strip() for x in element_text.split('\n') if x.strip()]

                # Extract the relevant data by skipping the first two lines
                if( (j>3) or (len(data)%2>0)):
                    relevant_data = data[1:]
                else:
                    relevant_data = data[2:]

                # Separate the first two items as column headers and the rest as values
                columns = relevant_data[0:2]
                your_list = relevant_data[4:]

                # Create a list of tuples where each tuple contains two consecutive items from your_list
                pairs = [(your_list[i], your_list[i+1]) for i in range(0, len(your_list), 2)]

                # Create a DataFrame from the list of pairs with appropriate column names
                df = pd.DataFrame(pairs, columns=columns)
                
                #Add GF Value
                df.loc[df.index[-1] + 1] = {'Name':'GFValue' , 'Current':elementsvalue}

                dfs.append(df)
                
                # Return the resulting DataFrame containing profitability rank information
                # print(df)#    return df

    return pd.concat(dfs, ignore_index=True)    
