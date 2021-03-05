from adafruit_display_text.label import Label
import terminalio
import time
import displayio

def RGB_hex(R,G,B):
	R = min(R, 255)
	G = min(G, 255)
	B = min(B, 255)
	return int('{:02x}{:02x}{:02x}'.format(R,G,B), 16)

class Plotter:
	TEMP_SLOT = 1
	PRESSURE_SLOT = 2
	PROX_SLOT = 3
	HUMID_SLOT = 4
	COLOR_SLOT = 5


	LABEL_COLOR = 0xc0c0c0
	def __init__(self, output, title="",
		screen_width=240, screen_height=240):
		self._output = output
		self._title = title
		self._max_title_len = 40
		self._font = terminalio.FONT
		self._content = None
		self._screen_width = screen_width
		self._screen_height = screen_height
		self._init_temp = False
		self.time = time.time()


		self._content = self._create_content()
		self._test_content = self._create_test_content()



	def display_on(self, tg_and_plot=None):
		self._output.show(self._content)

	def get_temp_line(self, temp):

		return Label(
			self._font,
			x = 20,
			y = 80,
			text = f'TEMP:     {temp}',
			max_glyphs = 20,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

	def get_pressure_line(self, pressure):

		return Label(
			self._font,
			x = 20,
			y = 100,
			text = f'PRESSURE: {pressure} ',
			max_glyphs = 20,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

	def get_proximity_line(self, prox):
		return Label(
			self._font,
			x = 20,
			y = 120,
			text = f'PROXIMTY: {prox} ',
			max_glyphs = 20,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

	def get_humidity_line(self, humid):
		return Label(
			self._font,
			x = 20,
			y = 140,
			text = f'HUMIDITY: {humid} ',
			max_glyphs = 20,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

	def get_color_line(self, R,G,B):
		return Label(
			self._font,
			x = 20,
			y = 160,
			# text = f'~~~ COLOR I SEE ~~~',
			text = f'{R}-{G}-{B}',
			max_glyphs = 20,
			scale = 2,
			line_spacing = 1,
			color = RGB_hex(R,G,B)
			# color = RGB_hex(R,G,B)
		)


	def _create_content(self):
		self._displayio_title = Label(
			self._font,
			x = 50,
			y = 20,
			text = self._title,
			max_glyphs = self._max_title_len,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)


		content = displayio.Group(max_size = 6)
		content.append(self._displayio_title)
		content.append(self.get_temp_line('???'))
		content.append(self.get_pressure_line('???'))
		content.append(self.get_proximity_line('???'))
		content.append(self.get_humidity_line('???'))
		content.append(self.get_color_line(0,0,0))




		return content

	def update_content(self, temp, pressure, prox, humid, color):
		if time.time() - self.time < 1:
			return None
		self.time = time.time()
		self._content[self.TEMP_SLOT] = self.get_temp_line(temp)
		self._content[self.PRESSURE_SLOT] = self.get_pressure_line(pressure)
		self._content[self.PROX_SLOT] = self.get_proximity_line(prox)
		self._content[self.HUMID_SLOT] = self.get_humidity_line(humid)
		r,g,b, _ = color
		self._content[self.COLOR_SLOT] = self.get_color_line(r,g,b)
		self._output.show(self._content)

	def test(self):
		self._output.show(self._test_content)

	def _create_test_content(self):
		text = Label(
			self._font,
			x = 50,
			y = 20,
			text = "TEST",
			max_glyphs = 4,
			scale = 4,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)


		content = displayio.Group(max_size = 1)
		content.append(text)
		return content
