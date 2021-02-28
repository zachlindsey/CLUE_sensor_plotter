import board
import time

from plotter import Plotter

from adafruit_clue import clue

initial_title = "Welcome to\nCLUE Plotter"

plotter = Plotter(board.DISPLAY, title=initial_title)

plotter.display_on()
while True:
	plotter.update_content(
		temp = clue.temperature, 
		pressure = clue.pressure,
		prox = clue.proximity,
		humid = clue.humidity,
		color = clue.color
	)
	time.sleep(1)

