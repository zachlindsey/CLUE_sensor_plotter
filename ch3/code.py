from adafruit_clue import clue
import displayio
import vectorio

import time

display = clue.display


a_gp = displayio.Group(y = 120)
f = open("A.bmp", "rb")
a_bmp = displayio.OnDiskBitmap(f)
a_tg = displayio.TileGrid(a_bmp, pixel_shader=displayio.ColorConverter())
a_tg.hidden = True
a_gp.append(a_tg)

b_gp = displayio.Group(x = 224, y = 120)
g = open("B.bmp", "rb")
b_bmp = displayio.OnDiskBitmap(g)
b_tg = displayio.TileGrid(b_bmp, pixel_shader=displayio.ColorConverter())
b_tg.hidden = True
b_gp.append(b_tg)

zero_pad_gp = displayio.Group(x = 0, y = 224)
one_pad_gp = displayio.Group(x = 112, y = 224)
two_pad_gp = displayio.Group(x = 224, y = 224)
h = open("check.bmp", "rb")

pads_gp = displayio.Group()

for gp in [zero_pad_gp, one_pad_gp, two_pad_gp]:
	pad_bmp = displayio.OnDiskBitmap(h)
	pad_tg = displayio.TileGrid(pad_bmp, pixel_shader=displayio.ColorConverter())
	gp.append(pad_tg)
	pads_gp.append(gp)

buttons = displayio.Group()
buttons.append(a_gp)
buttons.append(b_gp)
buttons.append(pads_gp)

display.show(buttons)


while True:
	if clue.button_a:
		a_tg.hidden = False
	else:
		a_tg.hidden = True

	if clue.button_b:
		b_tg.hidden = False
	else:
		b_tg.hidden = True

	pads_gp[0].hidden = not clue.touch_0
	pads_gp[1].hidden = not clue.touch_1
	pads_gp[2].hidden = not clue.touch_2