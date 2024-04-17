import time
import requests
from datetime import datetime


def trades_buda_endpoint(last_timestamp, market_id):
    try:
        url = f'https://www.buda.com/api/v2/markets/{market_id}/trades?timestamp={last_timestamp}'
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()['trades']
    except Exception as e:
        print(f"Error al obtener transacciones: {e}")
        return None

all_trades = []
timestamp_marzo_1 = datetime(2024, 3, 1).timestamp()
timestamp_12pm = timestamp_marzo_1 + (12 * 3600 ) 
timestamp_1pm = timestamp_marzo_1 + (13 * 3600) 

last_timestamp = int(timestamp_1pm * 1000)
all_transaction = 0


while True:
    data = trades_buda_endpoint(int(last_timestamp), 'btc-clp')
    last_timestamp = data['last_timestamp']

    for trade in data['entries']:
        trade_timestamp = int(trade[0])
        if trade_timestamp  <= int(timestamp_12pm * 1000):
            break
        transaction = float(trade[1]) * float(trade[2])
        all_transaction += transaction

    if int(last_timestamp) <= int(timestamp_12pm * 1000):
        break
    
    time.sleep(0.5)


print("Se transó durante el evento Black Buda BTC-CLP ",round(all_transaction,2))


all_trades_2023 = []

timestamp_marzo_1_2023 = datetime(2023, 3, 1).timestamp()
timestamp_12pm = timestamp_marzo_1_2023 + (12 * 3600 ) 
timestamp_1pm = timestamp_marzo_1_2023 + (13 * 3600) 


last_timestamp = int(timestamp_1pm * 1000)
all_transaction_2023 = 0

while True:
    
    data = trades_buda_endpoint(int(last_timestamp), 'btc-clp')
    
    last_timestamp = data['last_timestamp']

    for trade in data['entries']:
        trade_timestamp = int(trade[0])
        if trade_timestamp  <= int(timestamp_12pm * 1000):
            break
        transaction = float(trade[1]) * float(trade[2])
        all_transaction_2023 += transaction

    if int(last_timestamp) <= int(timestamp_12pm * 1000):
        break
    
    time.sleep(0.5)

percentage = (( all_transaction - all_transaction_2023 ) / all_transaction ) * 100

print("El aumento porcentual en comparación con el día del año anterior fue de ",(round(percentage, 2)),"%")


normal_commision = all_transaction * 0.008
print("Dinero que se dejó de ganar debido a la liberacion de comisiones", (round(normal_commision, 2)))