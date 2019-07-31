import requests
import time
from datetime import datetime

# define api url for bitcoin and ethereum(changed to ripple)
bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
eth_api_url = 'https://api.coinmarketcap.com/v1/ticker/ripple/'

# define ifttt post url
btc_ifttt_url = 'https://maker.ifttt.com/trigger/bitcoin_price_update/with/key/nozbZcx0SqhwkNiKTRD8hDe5Hhwuz8S73viooWeDPP-'
eth_ifttt_url = 'https://maker.ifttt.com/trigger/eth_price_update/with/key/nozbZcx0SqhwkNiKTRD8hDe5Hhwuz8S73viooWeDPP-'

# get latest bitcoin and ethereum price from api url
def get_latest_bitcoin_price():
    response = requests.get(bitcoin_api_url)
    btc_json = response.json()
    return float(btc_json[0]['price_usd'])

def get_latest_ethereum_price():
    response = requests.get(eth_api_url)
    eth_json = response.json()
    return float(eth_json[0]['price_usd'])

# post latest bitcoin and ethereumprice to ifttt, triggering notification
def post_ifttt_btc(event, value):
    data = {'value1': value}        # value1 corresponds to the value1 tag in the notification message
    ifttt_event_url = btc_ifttt_url.format(event)
    requests.post(ifttt_event_url, json=data)

def post_ifttt_eth(event, value):
    data = {'value1': value}
    ifttt_event_url = eth_ifttt_url.format(event)
    requests.post(ifttt_event_url, json=data)

# learn how to make this dynamic so I don't have to change with fluctuations
btc_threshold = 12000
eth_threshold = .42

def main():
    bitcoin_history = []
    eth_history = []
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")
    print("Starting price checker at " + date_time)

    while True:
        btc_price = get_latest_bitcoin_price()
        eth_price = get_latest_ethereum_price()
        date = datetime.now()
        bitcoin_history.append({'date' : date, 'price' : btc_price})
        eth_history.append({'date' : date, 'price' : eth_price})

        # emergency price drop notifications
        if btc_price > btc_threshold:
            post_ifttt_btc('bitcoin_price_emergency', btc_price)

        if eth_price > eth_threshold:
            post_ifttt_eth('eth_price_emergency', eth_price)

        # send update
        if len(bitcoin_history) == 5:
            post_ifttt_btc('bitcoin_price_update', format_btc_history(bitcoin_history))
            bitcoin_history = []

        if len(eth_history) == 5:
            post_ifttt_eth('eth_price_update', format_eth_history(eth_history))
            eth_history = []

        time.sleep(5*60) # update 10 * 60 seconds = every 10 minutes

def format_btc_history(bitcoin_history):
    rows = []
    for btc_price in bitcoin_history:
        date = btc_price['date'].strftime('%d.%m.%Y %H:%M')
        price = btc_price['price']

        row = '{}:  {}'.format(date, price)
        rows.append(row)
    return '\n'.join(rows)


def format_eth_history(eth_history):
    rows = []
    for eth_price in eth_history:
        date = eth_price['date'].strftime('%d.%m.%Y %H:%M')
        price = eth_price['price']

        row = '{}:  {}'.format(date, price)
        rows.append(row)
    return '\n'.join(rows)


if __name__ == '__main__':
    main()

