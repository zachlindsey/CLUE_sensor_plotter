import displayio
import vectorio

class Drawer:

	def __init__(self, output):
		self.output = output
		self.palette = displayio.Palette(color_count = 2)
		self.palette[0] = 0x000000
		self.palette[1] = 0xFFFFFF

		self.rect = vectorio.VectorShape(
			shape = vectorio.Rectangle(100,100),
			pixel_shader = self.palette,
		)

		self.gp = displayio.Group(max_size = 1)
		self.gp.append(self.rect)

	def draw(self, hexcode: str):
		print(hexcode)
		try:
			self.palette[1] = int(hexcode, 16)
			self.output.show(self.gp)
		except ValueError:
			print("ValueError... bad hexcode?")

