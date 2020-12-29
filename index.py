import serial
from threading import Thread

import logging
# from Queue import Queue

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

connected_to_device=False
TIMEOUT=15
target_ble="CB:E4:C4:4C:95:A4"
    #instantiate necessary objects and try connection
ui_ble=BLERadio()

def print_received_data(service):
    print(service.readline().decode("utf-8"))

def send_HB(service):
    print('HB')
    service.write("IPHB".encode("utf-8"))

def main():
    print('start')
    for device in ui_ble.start_scan(ProvideServicesAdvertisement,timeout=TIMEOUT):
        print(device)
        if UARTService in device.services:
            print(device)
            ui_ble.connect(device,timeout=TIMEOUT)
            if (ui_ble.connected == True):
                    connected_to_device=True
                    print('connected')
                    break
                    
    uart_service = ui_ble.connections[0][UARTService]
    print(uart_service)
    device_input_thread = threading.Thread(target=print_received_data,args=(uart_service,), daemon=True)
    device_input_thread.start()
    while ui_ble.connected:
        print('waiting')


if __name__=="__main__":
    main()
