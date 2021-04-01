# Chapter 0 - Setting Up

TODO

# Chapter 1 - Drawing 

In order to draw on to the screen, you will need to create a Python object that represents the display. For the clue, this is quite simple! We simply need to import the clue's Python object with `from adafruit_clue import clue`, and then we can get the display object with `display = clue.display`. 

## Displays and Groups

To make sure everything is up and running, it might be helpful to check out some properties of the display. Try printing out `display.height`, `display.width`, etc. I have created a `show_display_info` function to do this. Note that the first line of this function calls `display.show(None)`. This will reset the screen to display the terminal, so that the next lines will actually show up! When we have things to draw, we will also use this `display.show()` function to draw them.

Now, we need to understand the way adafruit's `displayio` library is organized. The basic building block is a `Group` object, which you can think of as a list that contains things to draw. What kinds of things can we draw? At the time of this writing, there are three objects we can place inside a `Group`: `TileGrid` objects, `vectorio.VectorShape` objects, and other `Group`s. This last option means that groups can be "nested" to allow for flexible displays and logical grouping of different parts of a display.

## Palettes

Before we can draw anything, we need to know how to color it. This job is handled by `displayio.Palette` objects and `displayio.ColorConverter` objects. For now, we'll use `displayio.Palette`. Essentially, it's just a handy container for storing colors in a way that the device can more readily use. Let's start by making a palette with four colors: white, red, green, and blue.

```
palette = displayio.Palette(color_count = 4)
palette[0] = 0xffffff
palette[1] = 0xff0000
palette[2] = 0x00ff00
palette[3] = 0x0000ff
```

Before going on, make note of the fact that we can set the different colors stored in the `Palettte` to be transparent or opaque. This will be important later when we try to draw multiple things at once.

## `vectorio`

It's actually easier to get started drawing using the `vectorio.VectorShape` library, so we'll do that first! This creates a simple 2d drawing that we can place in a group. Creating one requires we specify a shape object (either a circle, rectangle, or polygon), a color palette, and an x, y location.

So let's get things started by creating a circle `VectorShape`, adding it to a `Group`, and drawing it!

```
circle = vectorio.VectorShape(
	shape = vectorio.Circle(30),
	pixel_shader = palette,
	x = 120,
	y = 120
)

group = displayio.Group()

group.append(circle)

while True:
	display.show(group)
```

You'll see a red circle in the middle of the screen, but also a white rectangle from the upper left corner. This is probably not what you expected, but we will fix it later! For now, let's play with the positioning of the objects.

## Positioning

To understand how the `x`, `y` coordinates for the `Group` and `VectorShape` work, try some different values to see what happens. Rather than creating *new* groups and circles each time, simply update the parameters of the group and circle objects you already created, like this:

```
circle = vectorio.VectorShape(
	shape = vectorio.Circle(30),
	pixel_shader = palette,
	x = 120,
	y = 120
)

group = displayio.Group(x=120, y=120)

group.append(circle)

while True:
	for i in range(-120,120,10):
		circle.x = i
		circle.y = i
		display.show(group)
		time.sleep(0.1)
```

(Exercise: Time how long it takes the circle to move across the screen with this code. Then, move the code that creates the circle and group objects inside the `for` loop and see how much longer it takes!)

For starters, note that we can can have negative values for the circle's `x` and `y` coordinates. This is because these coordinates are relative to the location specified by the `Group` the circle belongs to. The `Group` coordinates can also be negative, and these are relative to the upper left corner of the screen.

## Multiple Shapes

Let's add a rectangle to go with our circle. Try this code:

```
palette = displayio.Palette(color_count = 4)
palette[0] = 0xffffff
palette[1] = 0xff0000
palette[2] = 0x00ff00
palette[3] = 0x0000ff

RADIUS = 30
circle = vectorio.VectorShape(
	shape = vectorio.Circle(RADIUS),
	pixel_shader = palette,
	x = 120,
	y = 120
)

rectangle = vectorio.VectorShape(
	shape = vectorio.Rectangle(60, 120),
	pixel_shader = palette,
	x = 120,
	y = 120
)

group = displayio.Group()


group.append(rectangle)
group.append(circle)

dx = 7
dy = 3

while True:
	circle.x += dx
	if circle.x > 240+RADIUS:
		circle.x -= 240+2*RADIUS
	circle.y += dy
	if circle.y > 240+RADIUS:
		circle.y -= 240+2*RADIUS
	display.show(group)
	time.sleep(0.1)
	display.refresh()

```
You'll notice that our rectangle appears for a second, but is quickly wiped away by the box around the circle! To fix this problem, we need to change the background color on the circle's palette to be transparent. Simply add the line `palette.make_transparent(0)` after creating the palette. Much better! 

Now, how do we make the rectangle a different color? Well, it seems that when using `vectorio`, the value for 0 in the palette controls the background, while the value for 1 controls the shape itself. So we will make two palettes, one for each shape. Remember to set *both* of the 0 colors on those palettes to be transparent.

Finally, notice how the order you place objects into the group matters. The objects are drawn in reverse order, so if you want your circle to appear on top, append it second.

## Polygons

Lastly, let's finish exploring what `vectorio` has to offer by making a simple polygon. All we have to do is specify a list of points for the polygon's vertices, and we're good to go! To make a simple "bow-tie" shape, we can specify `[(30,30), (120,120), (120,30), (30,120)]` as the points. Make sure to give it its own palette with a color of your choice and set the first to be transparent.

# Chapter 2 - Drawing Bitmaps

Vectorio is a great way to draw basic shapes, but what if you have an image already that you want to display? Maybe some sprites? Then we can save those images to the CLUE and display them using `displayio.Bitmap` objects. To start out, let's make a bitmap object "by hand" to see how it stores data. Suppose we want to make an image with red and white pixels. The most obvious thing to do is store the color tuples (255,0,0) and (255,255,255) in each pixel, depending on what color we want it to be. But since we're only using two colors, this is an enormous waste of memory! It is much simpler to just encode red as "color 0" and white as "color 1", and then we can just store one bit per pixel. Let's do just this.

```
bmp = displayio.Bitmap(120, 120, 2)

palette = displayio.Palette(2)
palette[0] = (255,0,0)
palette[1] = (255,255,255)

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

```

This code starts by creating a 120x120 bitmap with two colors. We then create a palette into which we place our two colors. Next, we spell out precisely which color each pixel should be. This is where you'd place the code for whatever pattern you want to draw! We then use a new `vectorio` class, the `TileGrid`. For now, we can think of this as a nice way to combine the raw bitmap and the color palette, but we will see some other nice uses later. Then, we can add our tilegrid to a group and display it!

## Drawing Saved Bitmaps

### `onDiskBitmap`

Suppose you have an image already that you'd like to use, perhaps made in paint or something. How can we extract the image and color data easily? One method is `displayio.onDiskBitmap`. This method allows you to display a bitmap saved directly on the CLUE's disk to the display. In the folder for this chapter is a file called "doge_24bit" that contains an image with full color space that we write to the screen. Note that we need to call `display.refresh()` to make it display.

```

with open('doge_24bit.bmp', 'rb') as f:
	bmp = displayio.OnDiskBitmap(f)
	tg = displayio.TileGrid(bmp, pixel_shader = displayio.ColorConverter())
	gp = displayio.Group()
	gp.append(tg)

	display.show(gp)

	display.refresh(target_frames_per_second=2)
	display.refresh()


while True:
	pass
```

The problem with this method of drawing bitmaps is that it takes a noticeable amount of time to load the image to the screen, so it's best for static images. The long load times are (I think?) because the images are not moved into RAM, and so have to be pulled off disk in pieces each time.

```
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
```

### `adafruit.image_load` and memory issues

A second method to show images is to place them in memory, creating a bitmap and palette object in the process. A handy tool to read off the pixel data and color data exists, so let's see how we can use it:

```
import adafruit_imageload

image, palette = adafruit_imageload.load("doge_24bit.bmp")
```

This code should give you an error on the CLUE. Why? The CLUE has 256KB of memory. A 240x240 image with full colors (24 bits) requires 172.8KB of memory. But we can't just load the image! We have to also load all the Python code into memory. If you run the following code after importing all your libraries

```
import gc
gc.collect()
print(gc.mem_free())
```

You will see how much space is left for all our non-library code, images, etc. to live in memory. I had only 98KB of space, so that full color image is just not going to work! However, a 256 color image (8 bits per pixel) comes in at 57KB. So we can load *one* such image. As expected, trying to go back and forth between the flipped version and the original version gives a `MemoryError`.


```

display = clue.display

bmp, palette = adafruit_imageload.load("doge_8bit.bmp")
tg = displayio.TileGrid(bmp, pixel_shader = palette)
gp = displayio.Group()
gp.append(tg)

bmp_flipped, palette_flipped = adafruit_imageload.load("doge_8bit_flipped.bmp")
# MemoryError!
tg_flipped = displayio.TileGrid(bmp_flipped, pixel_shader = palette_flipped)
gp_flipped = displayio.Group()
gp_flipped.append(tg_flipped)

while True:
	display.show(gp)
	display.refresh()

	display.show(gp_flipped)
	display.refresh()
	
```

One solution is to make the images have even less color: 4 bits per pixel, or 16 colors. The quality is quite low, but we can load multiple images into memory at once, and flipping back and forth between them is quite speedy! Try it with the `doge_4bit` files.

# Chapter 3 - Inputs



