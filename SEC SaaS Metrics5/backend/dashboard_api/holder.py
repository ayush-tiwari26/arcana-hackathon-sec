import yfinance as yf

import yahoo_fin.stock_info as si
x=si.get_holders('twlo')

print(x['Direct Holders (Forms 3 and 4)'])
df=x['Direct Holders (Forms 3 and 4)']
print(df['Shares'].tolist())

