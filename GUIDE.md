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

