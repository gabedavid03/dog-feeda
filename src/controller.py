import serial
from datetime import datetime
import time
import json
import pytz

COMPORT = '/dev/ttyACM0'

def retrieve_cycles(feed_number: int) -> float:
    with open('../web_server/feeds.json', 'r') as file:
        params = json.load(file)
        for feed in params['feeds']:
            if feed['feed_number'] == feed_number:
                amount_per_feed = feed['amount']
                cycles = int(amount_per_feed)
                print(f"{cycles}")
                return cycles
        print("Feed number not found")
        return 0

def validate_feed_time() -> int:
    est = pytz.timezone('America/Toronto')
    utc_now = datetime.utcnow()
    print(f"{utc_now}")
    current_time = utc_now.astimezone(est).time()

    with open('../web_server/feeds.json', 'r') as file:
        params = json.load(file)
    for feed in params['feeds']:
        if feed['completed']==1:
            continue
        start_time_str = feed['start_time']
        end_time_str = feed['end_time']
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
        if start_time <= current_time <= end_time:
            feed['completed'] = 1
            print(f"feed validated")
            with open('../web_server/feeds.json', 'w') as file:
                json.dump(params, file, indent=4)
            return feed['feed_number']
    return 0

def reset_completed() -> None:
    est = pytz.timezone('America/Toronto')
    utc_now = datetime.utcnow()
    current_time = utc_now.astimezone(est)
    midnight_str = '00:00'
    midnight = datetime.strptime(midnight_str, "%H:%M").time()

    if current_time == midnight:
        with open('../web_server/feeds.json', 'r') as file:
            params = json.load(file)
        for feed in params['feeds']:
            print(f"reseted")
            feed['completed'] = 0
        params["feeds_today"] = 0
        with open('../web_server/feeds.json', 'w') as file:
            json.dump(params, file, indent=4)
        return
    return

def autofeed() -> None:
    est = pytz.timezone('America/Toronto')
    utc_now = datetime.utcnow()
    # NEED TO SET TO CURRENT TIME!!!!!!!!
    currentstr = '08:00'
    current_time = datetime.strptime(currentstr, "%H:%M").time()

    with open('../web_server/feeds.json', 'r') as file:
        params = json.load(file)

    for feed in params['feeds']:
        end_time_str = feed['end_time']
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
        if current_time == end_time:
            if feed['completed'] == 0:
                if params['autodispense'] == 1:
                    cycles  = retrieve_cycles(feed['feed_number'])
                    send_feed(COMPORT, cycles)
            else: 
                return
        else:
            continue
    return
    
def feed_now() -> None:
    with open('../web_server/feeds.json', 'r') as file:
        params = json.load(file)
    if params['feed_now']['valid'] == 0:
        return
    else:
        cycles = params['feed_now']['amount']
        send_feed(COMPORT, cycles)
        params['feed_now']['valid'] = 0
        with open('../web_server/feeds.json', 'w') as file:
            json.dump(params, file, indent=4)
        return

def send_feed(comport: str, cycles: float) -> None:
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
    with open('../web_server/feeds.json', 'r') as file:
        params = json.load(file)
    params["feeds_today"] = int(params["feeds_today"]) + 1
    with open('../web_server/feeds.json', 'w') as file:
        json.dump(params, file, indent=4)
    return

def main(args = None) -> None: 
    print(f"Main Function")

if __name__ == '__main__':
        try:
            main()
        except Exception as e:
            print(e)