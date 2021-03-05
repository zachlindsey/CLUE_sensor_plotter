import board
import time

from plotter import Plotter

from adafruit_clue import clue

initial_title = "Welcome to\nCLUE Plotter"

plotter = Plotter(board.DISPLAY, title=initial_title)

plotter.display_on()
state = 0
button_lockout_timer = time.time()
while True:
	if time.time() - button_lockout_timer > 0.1:
		button_lockout_timer = time.time()
		if clue.button_a:
			state -= 1
			state %= 2

		if clue.button_b:
			state += 1
			state %= 2
			

	if state == 0:
			plotter.update_content(
				temp = clue.temperature, 
				pressure = clue.pressure,
				prox = clue.proximity,
				humid = clue.humidity,
				color = clue.color
			)
	elif state == 1:
		plotter.test()




