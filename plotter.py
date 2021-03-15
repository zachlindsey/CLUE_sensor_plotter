from adafruit_display_text.label import Label
import terminalio
import time
import displayio

import gc

def RGB_hex(R,G,B):
	R = min(R, 255)
	G = min(G, 255)
	B = min(B, 255)
	return int('{:02x}{:02x}{:02x}'.format(R,G,B), 16)

def out_of_bounds(y_min, y_max, min_data, max_data):
		delta = max_data - min_data
		if y_max < max_data or y_min > min_data:
			return True
		if max_data < y_max - 0.1*delta or min_data > y_min+0.1*delta:
			return True
		return False

class Plotter:
	LABEL_COLOR = 0xc0c0c0

	def __init__(self, output,
		screen_width=240, 
		screen_height=240
		):
		self._output = output
		self._font = terminalio.FONT
		self._screen_width = screen_width
		self._screen_height = screen_height

		LABEL_COLOR = 0xc0c0c0
		self.cur_source = None



		# create title
		cur_val = 0
		self.title = Label(
			self._font,
			x = 5,
			y = 10,
			text = f'No source!\nCurrent: {round(cur_val,2)}\nFree Mem: {gc.mem_free()}',
			max_glyphs = 80,
			scale = 2,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

		# create graph
		self.palette = displayio.Palette(color_count = 4)
		self.palette[0] = 0x000000
		self.palette[1] = 0xFF0000
		self.palette[2] = 0x00FF00
		self.palette[3] = 0X0000FF

		graph_width = 200
		self.graph_bitmap = displayio.Bitmap(graph_width, 120, 4)

		self.graph_tg = displayio.TileGrid(
			self.graph_bitmap,
			pixel_shader = self.palette,
			x = 240-graph_width,
			y = 120
		)

		# create y axis ticks
		self.num_ticks = 5

		# these quantities will be the min and max of graph window
		self.y_min = 0
		self.y_max = self.num_ticks - 1

		self.y_axis_labels = displayio.Group(max_size = self.num_ticks)
		for tick_num in range(self.num_ticks):
			y_screen = int(120-(self.num_ticks - tick_num)*24)
			# for x in range(5):
			# 	y_axis_bitmap[x,y_screen] = 0
	
			self.y_axis_labels.append(Label(
				self._font,
				x = 0,
				y = 120+y_screen,
				text = f'{round(tick_num,2)}',
				max_glyphs = 10,
				scale = 1,
				color = 0xFFFFFF
		))

		# merge together into the display group
		self.content = displayio.Group(max_size = 4)
		self.content.append(self.title)
		self.content.append(self.graph_tg)
		self.content.append(self.y_axis_labels)

	def redraw_y_axis(self, cur_val):
		if max(cur_val) > self.y_max:
			self.y_max = max(cur_val)
		if min(cur_val) < self.y_min:
			self.y_min = min(cur_val)

		for tick_num in range(self.num_ticks):
			y = self.y_min + tick_num * (self.y_max - self.y_min)/(self.num_ticks-1)
			# for x in range(5):
			# 	y_axis_bitmap[x,y_screen] = 0
	
			self.y_axis_labels[self.num_ticks - tick_num-1].text = f'{round(y,2)}'

	def replot(self, source_data, data_pointer, y_min, y_max):
		self.graph_bitmap.fill(0)
		x_offset = 0
		for x, y_meas_vect in enumerate(source_data[data_pointer:]):
			for i, y_meas in enumerate(y_meas_vect):
				y = int(119*(1 - (y_meas - y_min)/(y_max - y_min)))
				self.graph_bitmap[x,y] = i+1
				x_offset += 1
		for x, y_meas_vect in enumerate(source_data[:data_pointer]):
			for i, y_meas in enumerate(y_meas_vect):
				y = int(119*(1 - (y_meas - y_min)/(y_max - y_min)))
				
				self.graph_bitmap[x_offset + x,y] = i+1

		





	def draw_graph(self, source_name, source_data, data_pointer):
		gc.collect()
		cur_val = source_data[data_pointer-1]

		if len(cur_val) == 1:
			self.title.text = f'{source_name}\nCurrent: {round(cur_val[0],2)}\nFree Mem: {gc.mem_free()}'
		else:
			self.title.text = f'{source_name}'+'\n'.join(
				[f'Current{i}: {round(cur_val[i],2)}' for i in range(len(cur_val))]
			) + f'\nFree Mem: {gc.mem_free()}'

		if source_name != self.cur_source:
			self.cur_source = source_name
	
			self.y_min = min(map(min, source_data))
			self.y_max = max(map(max, source_data))

			if self.y_min == self.y_max:
				self.y_min -= 0.00001
				self.y_max += 0.00001
			self.redraw_y_axis(cur_val)
			self.replot(source_data, data_pointer, self.y_min, self.y_max)
		elif out_of_bounds(self.y_min, self.y_max, min(map(min, source_data)), max(map(max, source_data))):
			self.redraw_y_axis(cur_val)
			self.replot(source_data, data_pointer, self.y_min, self.y_max)
		else:
			new_y_vect = source_data[data_pointer-1]
			x = data_pointer
			for j in range(120):
				self.graph_bitmap[x,j] = 0
			for i, new_y in enumerate(new_y_vect):
				y = int(119*(1 - (new_y - self.y_min)/(self.y_max - self.y_min)))

				self.graph_bitmap[x,y] = i+1
		self._output.show(self.content)





class Plotter_old:
	TEMP_SLOT = 1
	PRESSURE_SLOT = 2
	PROX_SLOT = 3
	HUMID_SLOT = 4
	COLOR_SLOT = 5


	LABEL_COLOR = 0xc0c0c0
	def __init__(self, output, title="",
		screen_width=240, 
		screen_height=240
		):
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

		self.redraw_test = True

		self.test_text = 'a'
		self.y_min = None
		self.y_max = None

		

	def draw_graph(self, name, data, data_pointer):
		self.title.text = f'{name.upper()}\nCurrent: {round(data[data_pointer-1],2)}\nFree Mem: {gc.mem_free()}'
		

		if self.y_min == None or out_of_bounds(self.y_min, self.y_max, data[data_pointer-1]):
			self.y_min = min(data)
			self.y_max = max(data)
			self.init_graph(
				name, 
				data[data_pointer-1],
				y_min = self.y_min, 
				y_max = self.y_max
			)

		y_max = self.y_max
		y_min = self.y_min
		if y_max == y_min:
			delta_y = 1
			y_window_max = y_max + 1
			y_window_min = y_max - 1
			delta_y_window = 1.2*delta_y 
		else:
			delta_y = y_max - y_min
			y_window_max = y_max + 0.1*delta_y
			y_window_min = y_min - 0.1*delta_y
			delta_y_window = 1.2*delta_y
			
			

		x_offset = 0
		for x, y_meas in enumerate(data[data_pointer:]):
			y = int(119*(1 - (y_meas - y_window_min)/delta_y_window))
			
			self.graph_bitmap[x,y] = 1
			x_offset += 1
		for x, y_meas in enumerate(data[:data_pointer]):
			y = int(119*(1 - (y_meas - y_window_min)/delta_y_window))
			
			self.graph_bitmap[x_offset + x,y] = 1


		for tick_num in range(self.num_ticks):
			y_true = y_min + tick_num*(y_max - y_min)/float(self.num_ticks)
			y_screen = int(119*(1 - (y_true - y_min)/delta_y))
			# for x in range(5):
			# 	y_axis_bitmap[x,y_screen] = 0
			self.y_axis_labels[tick_num] = Label(
				self._font,
				x = 0,
				y = 120+y_screen,
				text = f'{round(y_true,2)}',
				max_glyphs = 10,
				scale = 1,
				color = 0xFFFFFF
		)


		
		self._output.show(self.content)









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
		text_string = "Here is a single Palette+Bitmap\nplaced on a 2x3 TileGrid"
		text1 = Label(
			self._font,
			x = 5,
			y = 5,
			text = text_string,
			max_glyphs = len(text_string),
			scale = 1,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

		text_string = "The bitmap:"
		text2 = Label(
			self._font,
			x = 5,
			y = 40,
			text = text_string,
			max_glyphs = len(text_string),
			scale = 1,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

		text_string = "The tiled bitmap:"
		text3 = Label(
			self._font,
			x = 5,
			y = 80,
			text = text_string,
			max_glyphs = len(text_string),
			scale = 1,
			line_spacing = 1,
			color = self.LABEL_COLOR
		)

		# to draw something other than text, first make
		# a palette object to store the colors
		palette = displayio.Palette(color_count = 4)

		palette[0] = 0xFF0000
		palette[1] = 0x00FF00
		palette[2] = 0x0000FF
		palette[3] = 0x000000

		# then, create a bitmap object
		bitmap = displayio.Bitmap(30, 30, 4)
		
		# we can fill up the bitmap.
		# the values are just integers, which correspond
		# to the indices in the palette we just set up
		for x in range(25):
			for y in range(25):
				bitmap[x,y] = x//10
			for y in range(25,30):
				bitmap[x,y] = 3
		for x in range(25,30):
			for y in range(30):
				bitmap[x,y] = 3


		# now, we need to place it in a TileGrid object...
		tilegrid1 = displayio.TileGrid(
			bitmap,
			pixel_shader = palette,
			width = 2,
			height = 3,
			x = 20,
			y = 100
		)

		tilegrid2 = displayio.TileGrid(
			bitmap,
			pixel_shader = palette,
			x = 80,
			y = 40
		)



		# and, finally... we place this on a group


		content = displayio.Group(max_size = 5)
		content.append(text1)
		content.append(text2)
		content.append(text3)
		content.append(tilegrid1)
		content.append(tilegrid2)
		return content
