ProfitabilityRank = dict()

ProfitabilityRank = {
    'GrossMarginperc'     : '//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[1]/td[3]/span/span',
    'OperatingMarginperc' : '//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[2]/td[3]/span/span',
    'NetMarginperc'       : '//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[3]/td[3]/span/span',
    'ROE %' : '//*[@id="financial-strength"]/div[2]/div[1]/table/tbody/tr[4]/td[3]/span/span'
    }

gurufocusSummeryTable = dict()

gurufocusSummeryTable = {
'FinancialStrength' : (1,1),
'GrowthRank' : (1,2),
'MomentumRank' : (1,3),
'LiquidityRatio' :  (1,4),
'DividendBuyBack' : (1,5),
'ProfitabilityRank' : (2,1),
'GFValueRank' : (2,2)
}

