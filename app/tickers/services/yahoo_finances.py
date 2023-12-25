import yfinance


class YahooFinances:
    @staticmethod
    def get_ticker(symbol: str):
        for ticker_key, ticker in yfinance.Tickers(symbol).tickers.items():
            if ticker_key == symbol:
                return ticker
