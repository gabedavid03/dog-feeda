import serial
from datetime import datetime
import time
import json
import pytz

def retrieve_cycles(feed_number) -> float:
    with open('../web_server/params.json', 'r') as file:
        params = json.load(file)
        amount_per_feed = params['feeds'][f'{feed_number}']['amount']
        cycles = int(amount_per_feed*4)
        return cycles

def validate_feed() -> int:
    est = pytz.timezone('America/Toronto')
    utc_now = datetime.utcnow()
    current_time = utc_now.astimezone(est)

    with open('../web_server/params.json', 'r') as file:
        params = json.load(file)
        for feed in params['feeds']:
            if feed['completed']:
                continue
            start_time = feed['start_time']
            end_time = feed['end_time']
            if start_time <= current_time <= end_time:
                return feed['feed_number']
        return 0

def send_feed(comport: str):
    cycles = retrieve_cycles()
    ser = serial.Serial(comport, 9600, timeout=2)
    time.sleep(2)
    ser.write(f"{cycles}\n".encode('utf-8'))
    i=0
    while ser.in_waiting == 0:
        print(f"waiting for acknowledge...")
        time.sleep(0.1)
        i = i+1
        if i >= 10:
            print("connection failed")
            return
    line = ser.readline().decode('utf-8').rstrip()
    print(f"{line}")
    return