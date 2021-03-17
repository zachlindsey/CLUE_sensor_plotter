import board
import time

import gc

from plotter import Plotter
from games import CenterGame

from adafruit_clue import clue

from adafruit_display_text.label import Label
import terminalio
import time
import displayio

initial_title = "Welcome to\nCLUE Plotter"

plotter = Plotter(board.DISPLAY)
center_game = CenterGame(board.DISPLAY)

state = 0

class Source:
    def __init__(self,
        name,
        clue_reading,
        is_scalar
    ):
        self.name = name
        self.data = []
        self.data_pointer = 0
        self.clue_reading = clue_reading
        self.is_scalar = is_scalar

    def update(self):
        graph_window_size = 200
        if len(self.data) < graph_window_size:
            if self.is_scalar:
                self.data.append([self.clue_reading()])
            else:
                self.data.append(self.clue_reading())
        else:
            if self.is_scalar:
                self.data[self.data_pointer] = [self.clue_reading()]
            else:
                self.data[self.data_pointer] = self.clue_reading()

        self.data_pointer += 1
        self.data_pointer %= graph_window_size


sources = [
    Source("temperature", lambda: clue.temperature, True),
    Source("pressure", lambda : clue.pressure, True),
    Source("accel", lambda: clue.acceleration, False),
    Source("humidity", lambda: clue.humidity, True),
    Source("touch_0", lambda: clue.touch_0, True)
]
num_screens = len(sources)

while True:
    center_game.draw(clue.acceleration)

last_source = ''
while True:
    gc.collect() 
    print(gc.mem_free())

    for source in sources:
        source.update()

    if clue.button_a:
        state -= 1
        state %= num_screens
        changed = True
        time.sleep(0.1)

    elif clue.button_b:
        state += 1
        state %= num_screens
        changed = True
        time.sleep(0.1)
            
    data = sources[state].data
    data_pointer = sources[state].data_pointer
    name = sources[state].name

    plotter.draw_graph(name, data, data_pointer)







#
# This is some code from the site that shows off
# all the features of the CLUE!
#


# clue.sea_level_pressure = 1020

# clue_data = clue.simple_text_display(title="CLUE Sensor Data!", title_scale=2)

        # clue_data[0].text = "Acceleration: {:.2f} {:.2f} {:.2f}".format(*clue.acceleration)
        # clue_data[1].text = "Gyro: {:.2f} {:.2f} {:.2f}".format(*clue.gyro)
        # clue_data[2].text = "Magnetic: {:.3f} {:.3f} {:.3f}".format(*clue.magnetic)
        # clue_data[3].text = "Pressure: {:.3f}hPa".format(clue.pressure)
        # clue_data[4].text = "Altitude: {:.1f}m".format(clue.altitude)
        # clue_data[5].text = "Temperature: {:.1f}C".format(clue.temperature)
        # clue_data[6].text = "Humidity: {:.1f}%".format(clue.humidity)
        # clue_data[7].text = "Proximity: {}".format(clue.proximity)
        # clue_data[8].text = "Gesture: {}".format(clue.gesture)
        # clue_data[9].text = "Color: R: {} G: {} B: {} C: {}".format(*clue.color)
        # clue_data[10].text = "Button A: {}".format(clue.button_a)
        # clue_data[11].text = "Button B: {}".format(clue.button_b)
        # clue_data[12].text = "Touch 0: {}".format(clue.touch_0)
        # clue_data[13].text = "Touch 1: {}".format(clue.touch_1)
        # clue_data[14].text = "Touch 2: {}".format(clue.touch_2)
        # clue_data.show()