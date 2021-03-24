from adafruit_clue import clue
import displayio
import vectorio

import time

display = clue.display


def show_display_info(display):
	display.show(None)
	print("DISPLAY INFO")
	print('height:', display.height)
	print('width:', display.width)
	print('rotation (deg)', display.rotation)
	print('auto_refresh:', display.auto_refresh)
	print('brightness:', display.brightness)
	print('auto_brightness:', display.auto_brightness)
	print('bus_object:', display.bus)

# show_display_info(display)


circle_palette = displayio.Palette(color_count = 2)
circle_palette[0] = 0xffffff
circle_palette[1] = 0xff0000

circle_palette.make_transparent(0)

RADIUS = 30
circle = vectorio.VectorShape(
	shape = vectorio.Circle(RADIUS),
	pixel_shader = circle_palette,
	x = 120,
	y = 120
)


rect_palette = displayio.Palette(color_count = 2)
rect_palette[0] = 0xffffff
rect_palette[1] = 0x00ff00
rect_palette.make_transparent(0)

HEIGHT = 120
WIDTH = 60
rectangle = vectorio.VectorShape(
	shape = vectorio.Rectangle(WIDTH, HEIGHT),
	pixel_shader = rect_palette,
	x = 120,
	y = 120
)

poly_palette = displayio.Palette(color_count = 2)
poly_palette[0] = 0xffffff
poly_palette[1] = 0x0000ff
poly_palette.make_transparent(0)

points = [
	(30,30),
	(120, 120),
	(120, 30),
	(30, 120)
]

polygon = vectorio.VectorShape(
	shape = vectorio.Polygon(points),
	pixel_shader = poly_palette,
	x = 0,
	y = 0
)

group = displayio.Group()

group.append(rectangle)
group.append(circle)
group.append(polygon)


dx = 7
dy = 3

display.show(group)
while True:
	circle.x += dx
	if circle.x > 240+RADIUS:
		circle.x -= 240+2*RADIUS
	circle.y += dy
	if circle.y > 240+RADIUS:
		circle.y -= 240+2*RADIUS

	rectangle.x -= dy
	if rectangle.x < -WIDTH:
		rectangle.x += 240+WIDTH

	rectangle.y += dx
	if rectangle.y > 240:
		rectangle.y -= 240 + HEIGHT
	
	time.sleep(0.1)








