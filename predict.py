import ccxt
import pandas as pd
import time
from termcolor import colored
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Binance client
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True
})

# Test connectivity
def test_connection():
    try:
        exchange.load_markets()
        logging.info("Connected to Binance successfully.")
    except Exception as e:
        logging.error(f"Failed to connect to Binance: {e}")
        exit(1)

# Fetch historical data
def fetch_price(symbol, timeframe='1m', limit=100):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        logging.error(f'Error fetching data for {symbol}: {e}')
        return None

# Start
test_connection()

# Main loop
while True:
    try:
        df = fetch_price('BTC/USDT')
        if df is not None and not df.empty:
            last_price = df['close'].iloc[-1]
            print(colored(f'Latest BTC/USDT price: {last_price}', 'green'))
        else:
            logging.warning("No data received.")
        time.sleep(5)
    except KeyboardInterrupt:
        print(colored("Bot stopped by user.", "red"))
        break
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        time.sleep(5)
