import serial

ser = None
def open():
    global ser
    if not ser or not ser.is_open:
        print('reopen serial')
        ser = serial.Serial("/dev/ttyAMA0", 115200)

def query_rx():
    count = ser.inWaiting()
    if count > 0:
        buf = ser.read(count)
        rx_str = buf.decode()
        print(rx_str)
        tx_str = '{}\n'.format(rx_str)
        ser.write(tx_str.encode())
        return rx_str