import json
import time
import websocket
from settings import currency_collection
from kafka import KafkaProducer, KafkaConsumer


consumer = KafkaConsumer(
    'crypto',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)

streams = []


arr_crypto = [
    "btcusdt@kline_1m",
    "ethusdt@kline_1m",
    "bnbusdt@kline_1m",
]


def check(name_crypto):
    for s in arr_crypto:
        if s.split('@')[0].upper() == name_crypto.upper() and s not in streams:
            return streams.append(s)


def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)


def on_message(ws, message):
    data = json.loads(message).get('data', {})
    s = data.get('s', {})
    o_price = data.get('k', {}).get('o')

    if o_price:
        result = currency_collection.insert_one({'name': s, 'price': o_price})
    print(s, o_price)
    if o_price is not None:
        message = f"{s} {o_price}"
        producer.send(topic='parsing', value=message)


def on_error(ws, error):
    print(error)


def on_close(ws, *lst):
    print("Connection")
    reconnect()


def on_open(ws):
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": streams,
        "id": 1
    }))


def reconnect():
    delay = 5
    print(f"Reconnection dans {delay} seconds...")
    time.sleep(delay)
    connect_to_binance_websocket()


def consumer_read():
    try:
        for message in consumer:
            my_bytes_value = message.value
            my_json = my_bytes_value.decode('utf8').replace("'", '"')
            name = json.loads(my_json)
            check(name)
            print(name)
            print(streams)
            connect_to_binance_websocket()
    finally:
        consumer.close()
        producer.close()


def task_thread(loop):
    print('thread running')
    websocket_url = "wss://stream.binance.com:9443/stream?streams="
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    coro = ws.run_forever()


def connect_to_binance_websocket():
    websocket_url = "wss://stream.binance.com:9443/stream?streams="
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
