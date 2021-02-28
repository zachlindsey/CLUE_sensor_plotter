import board
import displayio
import terminalio
import vectorio

display = board.DISPLAY

circle = vectorio.Circle(radius = 20)

group = displayio.Group(max_size = 10, scale = 1)
group.append(circle)

while True:
	display.show(group)

