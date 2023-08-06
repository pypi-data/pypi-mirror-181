# Ripio Client for Python
###  ALPHA SOFTWARE
  

This is a lightweight library that works as a client to [Ripio](https://www.ripio.com) Services

## Installation
```bash
pip install ripio-client
```

## Usage example
```python
from ripio.trade import Client

# API key is required for user data endpoints
client = Client(api_key='<api_key>')

# Get balance information
print(client.balance())

# Post a new order
params = {
	'pair': 'BTC_USDC',
	'side': 'buy',
	'amount': 0.01,
	'type': 'market'
}
response = client.create_order(**params)
print(response)
```
