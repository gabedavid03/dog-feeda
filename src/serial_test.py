import serial
import time

# Function to send data and receive confirmation
def send_and_receive(ser, message):
    ser.write((message + "\n").encode())  # Send message
    while ser.in_waiting == 0:
        time.sleep(0.1)  # Wait for response
    return ser.readline().decode().strip()  # Read response

# Establish serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
time.sleep(2)  # Wait for connection to establish

try:
    # Send a message and receive confirmation
    response = send_and_receive(ser, "Hello Arduino")
    print(f"Arduino says: {response}")
finally:
    ser.close()  # Ensure the serial connection is closed on exit
