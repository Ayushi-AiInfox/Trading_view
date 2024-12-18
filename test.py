# import yfinance as yf

def get_stock_sectors(tickers):
    stock_sectors = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Unknown')  # Get sector, default to 'Unknown' if not available
            stock_sectors[ticker] = sector
        except Exception as e:
            stock_sectors[ticker] = f"Error: {str(e)}"  # Handle errors for missing or invalid data
    
    return stock_sectors

# # Example usage
# tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
# sectors = get_stock_sectors(tickers)
# print(sectors)


# import yfinance as yf

def get_stock_regions(tickers):
    stock_regions = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            region = info.get('country', 'Unknown')  # Default to 'Unknown' if country is not available
            stock_regions[ticker] = region
        except Exception as e:
            stock_regions[ticker] = f"Error: {str(e)}"  # Handle errors for missing or invalid data
    return stock_regions

# # Example usage
# tickers = ['AAPL', 'TSLA', 'BABA', 'SONY', 'TSM']
# regions = get_stock_regions(tickers)
# print(regions)


import yfinance as yf

def get_live_price(ticker):
    """
    Fetch the live price of a stock using yfinance.

    :param ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    :return: Current live price of the stock
    """
    try:
        stock = yf.Ticker(ticker)
        live_price = stock.fast_info['last_price']  # Fast info is faster and optimized for live data
        return live_price
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"

# Example usage
ticker = 'AAPL'
live_price = get_live_price(ticker)
print(f"Live price of {ticker}: ${live_price}")
