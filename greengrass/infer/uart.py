import serial

ser = None

def open():
    global ser
    if not ser or not ser.is_open:
        ser = serial.Serial("/dev/ttyAMA0", 115200)

def get():
    count = ser.inWaiting()
    if count > 0:
        buf = ser.read(count)
        rx_str = buf.decode()
        return parse(rx_str)

def parse(rx_str):
    data = []
    str_array = rx_str.split('\r\n')
    for str in str_array:
        row = [float(i) for i in (str.split(','))]
        data.append(row)
    return data    

def send(tx_str):
    tx_str = '{}\n'.format(tx_str)
    ser.write(tx_str.encode())