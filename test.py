import pandas as pd
import yfinance as yf

# URL containing S&P 500 tickers
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
sp500_data = pd.read_csv(url)

# Get the list of symbols
sp500_symbols = sp500_data['Symbol'].tolist()

# Validate using yfinance
valid_symbols = []
for symbol in sp500_symbols:
    try:
        yf.Ticker(symbol)  # Validate the ticker
        valid_symbols.append(symbol)
    except Exception as e:
        print(f"Invalid symbol: {symbol}, Error: {e}")

print(valid_symbols)  # List of validated tickers