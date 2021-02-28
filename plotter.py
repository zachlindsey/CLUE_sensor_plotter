from adafruit_display_text.label import Label
import terminalio
import displayio

class Plotter:
	LABEL_COLOR = 0xc0c0c0
	def __init__(self, output, title="",
		screen_width=240, screen_height=240):
		self._output = output
		self._title = title
		self._max_title_len = 40
		self._font = terminalio.FONT
		self._displayio_graph = None
		self._screen_width = screen_width
		self._screen_height = screen_height



	def display_on(self, tg_and_plot=None):
		if self._displayio_graph is None:
			self._displayio_graph = self._make_empty_graph()
		self._output.show(self._displayio_graph)

	def _make_empty_graph(self):
		self._displayio_title = Label(
			self._font,
			x = 50,
			y = 100,
			text = self._title,
			max_glyphs = self._max_title_len,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

		g_background = displayio.Group(max_size = 4)
		g_background.append(self._displayio_title)

		return g_background