import serial
import time
import json

def retrieve_cycles() -> float:
    with open('../web_server/params.json', 'r') as file:
        params = json.load(file)
        amount_per_feed = float(params['AMOUNT_PER_FEED'])
        cycles = int(amount_per_feed*4)
        return cycles

def validate_feed() -> bool:
    return

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