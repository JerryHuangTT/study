import serial

ser = None

def open():
    global ser
    if not ser or not ser.is_open:
        ser = serial.Serial("/dev/ttyAMA0", 512000)
        print('open')

def get():
    count = ser.inWaiting()
    if count > 0:
        buf = ser.read(count).decode()
        return parse(buf)

def send(tx_str):
    ser.write(tx_str.encode())

def parse(buf):
    try:
        if buf.count(',') == 5:
            return [float(i) for i in buf.split(',')]       
    except Exception as e:
        return