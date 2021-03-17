import requests
import pandas as pd


from time import sleep


def download_data(from_symbol, to_symbol, exchange, datetime_interval):
    supported_intervals = {'minute', 'hour', 'day'}
    assert datetime_interval in supported_intervals,'datetime_interval should be one of %s' % supported_intervals    
    print('Downloading %s trading data for %s %s from %s' %(datetime_interval, from_symbol, to_symbol, exchange))
    base_url = 'https://min-api.cryptocompare.com/data/histo'
    url = '%s%s' % (base_url, datetime_interval)    
    params = {'fsym': from_symbol, 'tsym': to_symbol,
              'limit': 2000, 'aggregate': 1,
              'e': exchange}
    request = requests.get(url, params=params)
    data = request.json()
    
    return data
def convert_to_dataframe(data):
    df = pd.json_normalize(data, ['Data'])
    df['datetime'] = pd.to_datetime(df.time, unit='s')
    df = df[['datetime', 'low', 'high', 'open',
             'close', 'volumefrom', 'volumeto']]
    return df

def filter_empty_datapoints(df):
    indices = df[df.sum(axis=1) == 0].index
    print('Filtering %d empty datapoints' % indices.shape[0])
    df = df.drop(indices)
    
    return df

to_symbol = 'USDT'
exchange = 'binance'
datetime_interval = 'day'

coin_list=['ada','algo','atom','band','bat','bch','bnb','dash','enj','eos','etc','eth','iost','kava','kmd','knc','link','lrc','ltc','neo','omg','ont','qtum','rlc','theta','tomo','trx','vet','waves','xlm','xmr','xrp']

for coin in coin_list:
    from_symbol = coin.upper()
    data = download_data(from_symbol,to_symbol,exchange, datetime_interval) 
    df = convert_to_dataframe(data)
    df = filter_empty_datapoints(df)
    df['symbol'] = from_symbol
    if coin != 'ada':
        dff = dff.append(df)
    else:
        dff = df
dff.to_csv("binance_all_daily.csv", index=False)