import displayio
import vectorio as vt


def empty_circle(radius, x, y, outer_palette, inner_palette, thickness = 2):
	# radius = radius
	# x, y = location of circle in group
	# outer_palette = determines the color of boundary and outer fill
	# inner_pallete = determines fill color; the first value MUST BE
	# 	TRANSPARENT

	circle_gp = displayio.Group(max_size = 2)

	circle_gp.append(
		vt.VectorShape(
			shape = vt.Circle(radius), 
			pixel_shader = outer_palette,
			x = x, 
			y = y
		)
	)

	circle_gp.append(
		vt.VectorShape(
			shape = vt.Circle(radius-thickness),
			pixel_shader = inner_palette,
			x = x,
			y = y
		)
	)

	return circle_gp



class CenterGame:
	def __init__(self, output):
		self._output = output


		# when drawing circles, 0 is the background color
		# that is drawn in the bounding box of the cirlce
		# 1 is the fill color

		# you can make the background color"transparent"

		self.circle_palette = displayio.Palette(color_count = 2)
		self.circle_palette[0] = 0x000000
		self.circle_palette[1] = 0xb0a3a2
		self.circle_palette.make_transparent(0)

		self.inner_circle_palette = displayio.Palette(color_count = 2)
		self.inner_circle_palette[0] = 0x000000
		self.inner_circle_palette[1] = 0x000000
		self.inner_circle_palette.make_transparent(0)

		self.circle_gp = displayio.Group(max_size = 4)

		for r in [120, 80, 40]:
			self.circle_gp.append(
				empty_circle(
					r, 
					120, 
					120, 
					self.circle_palette, 
					self.inner_circle_palette)
			)

		self.main_circle_palette = displayio.Palette(color_count = 2)
		self.main_circle_palette[0] = 0x000000
		self.main_circle_palette[1] = 0xffffff
		self.main_circle_palette.make_transparent(0)

		self.main_inner_circle_palette = displayio.Palette(color_count = 2)
		self.main_inner_circle_palette[0] = 0x000000
		self.main_inner_circle_palette[1] = 0xff0000
		self.main_inner_circle_palette.make_transparent(0)

		self.circle_gp.append(
			empty_circle(
					15, 
					120, 
					120, 
					self.circle_palette, 
					self.main_inner_circle_palette)
		)
		

		

	def draw(self, accels):
		if accels[0]**2 + accels[1]**2 < 0.5:
			self.main_inner_circle_palette[1] = 0x00ff00
		else:
			self.main_inner_circle_palette[1] = 0xff0000

		self.circle_gp[-1][0].x = 120+int(10*accels[0])
		self.circle_gp[-1][0].y = 120+int(10*accels[1])
		self.circle_gp[-1][1].x = 120+int(10*accels[0])
		self.circle_gp[-1][1].y = 120+int(10*accels[1])
		self._output.show(self.circle_gp)