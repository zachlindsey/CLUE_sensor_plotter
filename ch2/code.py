from adafruit_clue import clue
import displayio
import vectorio
import adafruit_imageload

import gc

import time

display = clue.display

bmp, palette = adafruit_imageload.load("doge_4bit.bmp")
tg = displayio.TileGrid(bmp, pixel_shader = palette)
gp = displayio.Group()
gp.append(tg)

bmp_flipped, palette_flipped = adafruit_imageload.load("doge_4bit_flipped.bmp")
tg_flipped = displayio.TileGrid(bmp_flipped, pixel_shader = palette_flipped)
gp_flipped = displayio.Group()
gp_flipped.append(tg_flipped)

while True:
	display.show(gp)
	display.refresh(target_frames_per_second = 30)

	display.show(gp_flipped)
	display.refresh(target_frames_per_second = 30)

#
#	trying to load from memory, but no space!
#

bmp, palette = adafruit_imageload.load("doge_8bit.bmp")
tg = displayio.TileGrid(bmp, pixel_shader = palette)
gp = displayio.Group()
gp.append(tg)

bmp_flipped, palette_flipped = adafruit_imageload.load("doge_8bit_flipped.bmp")
tg_flipped = displayio.TileGrid(bmp_flipped, pixel_shader = palette_flipped)
gp_flipped = displayio.Group()
gp_flipped.append(tg_flipped)

while True:
	display.show(gp)
	display.refresh()

	display.show(gp_flipped)
	display.refresh()

#
#	loading from disk, viewing the long load times
#

f = open('doge_24bit.bmp', 'rb')
bmp = displayio.OnDiskBitmap(f)
tg = displayio.TileGrid(bmp, pixel_shader = displayio.ColorConverter())
gp = displayio.Group()
gp.append(tg)

g = open('doge_24bit_flipped.bmp', 'rb')
bmp_flip = displayio.OnDiskBitmap(g)
tg_flip = displayio.TileGrid(bmp_flip, pixel_shader = displayio.ColorConverter())
gp_flip = displayio.Group()
gp_flip.append(tg_flip)

display.show(gp_flip)


while True:
	display.show(gp)
	display.refresh()

	display.show(gp_flip)
	display.refresh()


while True:
	pass


bmp = displayio.Bitmap(240, 240, 256)


with open('doge_16.bmp', 'rb') as f:
	data = f.read()


	header_field = data[:2]
	print(header_field.decode('utf-8'))

	filesize = data[2:6]
	print("FILESIZE:", int.from_bytes(filesize, "little"))

	pixel_loc = data[10:14]
	print("DATA START:", int.from_bytes(pixel_loc, "little"))

	header_size = data[14:18]
	print("HEADER SIZE:",int.from_bytes(header_size, "little"))

	if header_field.decode('utf-8') == 'BM':

		width = data[18:22]
		print("WIDTH:", int.from_bytes(width, "little"))

		height = data[22:24]
		print("HEIGHT:", int.from_bytes(height, "little"))

while True:
	pass


tg = displayio.TileGrid(bitmap = bmp, pixel_shader =None )


bmp = displayio.Bitmap(120, 120, 2)



for i in range(120):
	for j in range(120):
		if (i + j) % 8 in [0,1,2,4]:
			bmp[i,j] = 1
		else:
			bmp[i,j] = 0

tg = displayio.TileGrid(bitmap = bmp, pixel_shader = palette)

gp = displayio.Group(x = 60, y = 60)
gp.append(tg)

display.show(gp)
while True:
	pass









