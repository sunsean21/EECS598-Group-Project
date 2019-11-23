from model_util import EventHandler
from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Interface(EventHandler):

	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Interface, self).__init__(name, label,top_left_x, top_left_y, width, height)

	def accept(self, body_part):
		return body_part.visit_interface(self)

class Input_Widget(Interface):

	def __init__(self, name, label,top_left_x, top_left_y, width, height):
		super(Input_Widget, self).__init__(name, label,top_left_x, top_left_y, width, height)


class Output_Widget(Interface):

	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Output_Widget, self).__init__(name, label,top_left_x, top_left_y, width, height)


class Button(Input_Widget):
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Button, self).__init__(name, label, top_left_x, top_left_y, width, height)
	
	def handle(self, event):
		return self.accept(event.body_part)
	
	def press(self):
		'''Change state of device to pressed, if successful'''
		pass

	def see(self):
		''' Default button has no eye tracking, so do nothing.'''
		pass

	def draw(self, ax, origin_x=0, origin_y=0):
		''' In addition to rectangle it draws character text. '''
		super().draw(ax, origin_x, origin_y)

		label_x = origin_x + self.top_left_x + self.width/2
		label_y = origin_y + self.top_left_y + self.height/2

		ax.annotate(self.label, (label_x, label_y), color='black', weight='bold', fontsize=6, ha='center', va='center')

class KeyboardKey(Button):
	def __init__(self, name, label, top_left_x, top_left_y, width, height, output):
		super(KeyboardKey, self).__init__(name, label, top_left_x, top_left_y, width, height)
		self.output = output
	
	def press(self):
		'''Change state of device to pressed, if successful'''
		self.output.set_text(self.output.label + self.label)

class KeyboardDeleteKey(Button):
	def __init__(self, name, label, top_left_x, top_left_y, width, height, output):
		super(KeyboardDeleteKey, self).__init__(name, label, top_left_x, top_left_y, width, height)
		self.output = output
	
	def press(self):
		'''Change state of device to pressed, if successful'''
		if len(self.output.label) > 0:
			self.output.set_text(self.output.label[:len(self.output.label) -1])

class TextBox(Output_Widget):
	def __init__(self, name, label, top_left_x, top_left_y, width, height, character_width, character_height):
		super(TextBox, self).__init__(name, label, top_left_x, top_left_y, width, height)

		self.character_width = character_width
		self.character_height = character_height
	
	def handle(self, event):
		return self.accept(event.body_part)

	def press(self):
		''' Nothing happens when you press on a character in a text field.'''
		pass

	def see(self):
		''' Nothing happens when you press on a character in a text field.'''
		pass

	def set_text(self, text):
		''' Utility method to set the characters of this text box. '''

		self.label  = text

		self.remove_all_children()

		# make the text in the middle of the textbox
		character_top_left_x = (self.width - len(text) * self.character_width) / 2 # TODO: remove fixed padding
		character_top_left_y = (self.height - self.character_height)/2 # Centered.

		character_index = 0

		for character in text:
			# print(character)
			character_widget = Character(self.name + ':' + str(character_index) + '_' + character, character, character_top_left_x, character_top_left_y, self.character_width, self.character_height)
			self.add_child(character_widget, character_top_left_x, character_top_left_y)

			character_top_left_x += self.character_width
			character_index += 1


class Character(Output_Widget):
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		super(Character, self).__init__(name, label, top_left_x, top_left_y, width, height)
	
	def handle(self, event):
		return self.accept(event.body_part)
	
	def press(self):
		''' Nothing happens when you press on a character in a text field.'''
		pass

	def see(self):
		''' Nothing happens when you press on a character in a text field.'''
		pass

	def draw(self, ax, origin_x=0, origin_y=0):
		''' Only draw character text. '''

		label_x = origin_x + self.top_left_x + self.width/2
		label_y = origin_y + self.top_left_y + self.height/2

		ax.annotate(self.label, (label_x, label_y), color='black', weight='normal', fontsize=4, ha='center', va='center')