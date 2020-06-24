# [Crypto Updates](https://crypto-updates.herokuapp.com/)

Finds price difference for a currency pair between multiple exchanges. It lists the trades with more than 3% profit (calculated by price difference) if you buy from one exchange and sell to other.

Enable the sound to get alert whenever a new trade is found

## Adding Exchanges

Currently used exchanges are:
1. Binance
2. Bitfinex
3. Livecoin

Add more exchanges to the `Exchanges` table. The fields required are:
1. `exchange_name` : The display name of exchange
2. `price_endpoint` : The exchange API endpoint for symbols ticker. It should provide all symbols tickers in an array
3. `is_all_coins` : If price endpoint has all symbols in array. Currently it does not work for exchanges that provide tickers for only a single symbols in one request
4. `has_usdt` : If exchange uses USDT for naming USD Trading coin. If set to False, USD will be treated at USDT
5. `symbol_format` : A string showing how exchange names currency pairs. If exchange adds some characters it should be set "pretext{symbol}appendtext". "{symbol}" is used as an identifier for normal pair name (it's fine if it contains non alpha characters or is lowercase)
5. `price_datatype` : A JSON datafield showing the response to price endpoint. It should be set like the following
```bash
{
    "path": "path.to.prices.array",     # Leave it "" if response gives array directly
    "name": "symbol",                   # Name of field used for currency pair
    "price": "last",                    # Name of field used to give last price
    "volume": "volume",                 # Name of field used for volume
    "bid": "best_bid",                  # Name of field used for best bid Qty
    "ask": "best_ask",                  # Name of field used for best ask Qty
}

# The name of fields can be integer indexes too as is case of bitfinex
# See the value used in already added Exchanges to know more
```

## Installation

```bash
# Activate virtualenv
source ./bin/activate

# Setup Databases
python3 manage.py makemigrations
python3 manage.py migrate

# Create Super User for Admin Dashboard
python3 manage.py createsuperuser
```

To run the Django server in Development environment
```bash
# Run daphne server
daphne multichat.asgi:application

# Run channels worker
python3 manage.py runworker channels multichat.asgi
```

## Deployment
Test : [HerokuApp](https://crypto-updates.herokuapp.com/)

## License
[MIT](https://choosealicense.com/licenses/mit/)
