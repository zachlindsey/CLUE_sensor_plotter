# import board

# import gc

# from plotter import Plotter
# from games import CenterGame

from adafruit_ble import BLERadio, Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.characteristics.stream import StreamIn
from adafruit_ble.services import Service

# from adafruit_display_text.label import Label
# import terminalio
import time
# import displayio

ble = BLERadio()
ble.name = "CLUE BLE"

class CustomUART(Service):

    uuid = VendorUUID("8ba86973-935c-447c-91ad-bdcbad575f31")
    _server_rx = StreamIn(
        uuid=VendorUUID("8ba86974-935c-447c-91ad-bdcbad575f31"),
        timeout=1.0,
        buffer_size=64,
    )

    def __init__(self, service=None):
        # just steal the uuid code from MIDISerivce
        
        super().__init__(service = service)
        self.connectable = True
        self._rx = self._server_rx

    def read(self, nbytes=None):
        return self._rx.read(nbytes)


service = CustomUART()
ad = ProvideServicesAdvertisement(service)


while True:
    if ble.connected:
        print('connected!' + service.read(1).decode('utf-8'))

    else:
        print('not connected...')
        if not ble.advertising:
            ble.start_advertising(ad)
    time.sleep(1)


#
#   BLE Broadcast Measurements
#

# import time
# from adafruit_clue import clue
# import adafruit_ble_broadcastnet

# while True:
#     measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()

#     measurement.temperature = clue.temperature
#     measurement.pressure = clue.pressure
#     measurement.relative_humidity = clue.humidity
#     measurement.acceleration = clue.acceleration
#     measurement.magnetic = clue.magnetic

#     print(measurement)
#     print(measurement.data_dict[255])
#     adafruit_ble_broadcastnet.broadcast(measurement)
#     time.sleep(60)




#
# GAME
#


# center_game = CenterGame(board.DISPLAY)


# while True:
#     center_game.draw(clue.acceleration)


#
# SENSORS
#


# initial_title = "Welcome to\nCLUE Plotter"

# plotter = Plotter(board.DISPLAY)

# state = 0

# class Source:
#     def __init__(self,
#         name,
#         clue_reading,
#         is_scalar
#     ):
#         self.name = name
#         self.data = []
#         self.data_pointer = 0
#         self.clue_reading = clue_reading
#         self.is_scalar = is_scalar

#     def update(self):
#         graph_window_size = 200
#         if len(self.data) < graph_window_size:
#             if self.is_scalar:
#                 self.data.append([self.clue_reading()])
#             else:
#                 self.data.append(self.clue_reading())
#         else:
#             if self.is_scalar:
#                 self.data[self.data_pointer] = [self.clue_reading()]
#             else:
#                 self.data[self.data_pointer] = self.clue_reading()

#         self.data_pointer += 1
#         self.data_pointer %= graph_window_size


# sources = [
#     Source("temperature", lambda: clue.temperature, True),
#     Source("pressure", lambda : clue.pressure, True),
#     Source("accel", lambda: clue.acceleration, False),
#     Source("humidity", lambda: clue.humidity, True),
#     Source("touch_0", lambda: clue.touch_0, True)
# ]
# num_screens = len(sources)

# last_source = ''
# while True:
#     gc.collect() 
#     print(gc.mem_free())

#     for source in sources:
#         source.update()

#     if clue.button_a:
#         state -= 1
#         state %= num_screens
#         changed = True
#         time.sleep(0.1)

#     elif clue.button_b:
#         state += 1
#         state %= num_screens
#         changed = True
#         time.sleep(0.1)
            
#     data = sources[state].data
#     data_pointer = sources[state].data_pointer
#     name = sources[state].name

#     plotter.draw_graph(name, data, data_pointer)

