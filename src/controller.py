import serial
import time
import json

def retrieve_params() -> float:
    with open('../web_server/params.json', 'r') as file:
        params = json.load(file)
        amount_per_feed = params['AMOUNT_PER_FEED']
        return amount_per_feed

def validate_feed() -> bool:
    return

def send_feed(amount_per_feed: float, comport: str):
    ser = serial.Serial(port=comport, baudrate=9600, timeout=1)
    ser.write(f"{amount_per_feed}")
