import requests

def get_token_prices():
    binance_url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(binance_url)
    data = response.json()
    return {token['symbol'][:-4]: token['price'] for token in data if token['symbol'].endswith('USDT')}

def get_tokens():
    binance_url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(binance_url)
    data = response.json()
    return {token['symbol'][:-4]: token['symbol'][:-4] for token in data if token['symbol'].endswith('USDT')}
