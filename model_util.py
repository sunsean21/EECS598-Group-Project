import matplotlib.pyplot as plt
import matplotlib.patches as patches

class EventHandler():
	''' This is a general purpose event handler. Any composite that has children and that wants to delegate event handling to those children should inherit from this class.'''
	def __init__(self, name, label, top_left_x, top_left_y, width, height):
		'''Initializes an event handler with (unique) name, label, no chilndren, and position. Top left (x,y) relative to parent.'''
		self.children = {}
		self.name = name
		self.label  = label
		self.parent = None
		self.top_left_x = top_left_x
		self.top_left_y = top_left_y
		self.width = width
		self.height = height

	def handle(self, event):
		''' Default handling of events--simply delegate to all children. Subclasses can choose to implement their own.'''
		is_handled = False
		for child in self.children.values():
			if self.__intersects(event.x, event.y, child):
				translated_event = self.__translate(child, event)
				is_handled = child.handle(translated_event)
				if is_handled:
					break
		return is_handled

	def intersects(self, loc_x, loc_y):
		''' Tests if a point intersects this handler.'''
		if (loc_x > self.top_left_x and loc_x < self.top_left_x + self.width) and (loc_y > self.top_left_y and loc_y < self.top_left_y + self.height):
			return True
		else:
			return False

	def find_intersect(self, event):
		''' Default way to find the intersecting child on top--simply delegate to all children. Retunrs intersecting handler in coordinates relative to the self. Subclasses can choose to implement their own.'''

		intersecting_handler = None

		for child in self.children.values():
			if self.__intersects(event.x, event.y, child):
				translated_event = self.__translate(child, event)
				intersecting_handler = child.find_intersect(translated_event)

				if intersecting_handler is not None:
					# Translate.
					intersecting_handler.top_left_x += self.top_left_x
					intersecting_handler.top_left_y += self.top_left_y

					break;

		if intersecting_handler is None:
			intersecting_handler = self.copy()
				
		return intersecting_handler
			
	def __translate(self, child, event):
		''' Translates an event to child's coordinates.'''
		translated_event = event.copy()
		translated_event.x = event.x - child.top_left_x
		translated_event.y = event.y - child.top_left_y

		return translated_event

	def __intersects(self, loc_x, loc_y, child):
		''' Tests if a point intersects child.'''
		return child.intersects(loc_x, loc_y)

	def add_child(self, child, top_left_x, top_left_y):
		''' Adds a child to this event handler at a new location. Removes child from its old parent.'''
		if isinstance(child, EventHandler):
			if self.children is None:
				self.children = {}
			child.top_left_x = top_left_x
			child.top_left_y = top_left_y
			self.children[child.name] = child

			if not(child.parent == self):
				if child.parent:
					child.parent.remove_child(child)
				child.parent = self 
		else:
			raise Exception('Trying to add incorrect type of child')

	def remove_child(self, child):
		''' Removes a child from the handler. It will no longer be handled by this  handler.'''
		if child.parent == self:
			if self.children:
				del self.children[child.name]
			child.parent = None

	def remove_all_children(self):
		''' Removes all children from the handler. None of them will be handled by this handler any longer.'''

		for child_key in list(self.children.keys()):
			self.remove_child(self.children[child_key])

	def set_parent(self, parent):
		''' Sets a parent for this event handler. '''
		self.parent = parent
		if not self.parent.children.contains(self):
			self.parent.add_child(self)

	def find_descendant(self, name):
		''' Find and return a descendant, but with its position in the coordiantes of this event handler. '''

		descendant  = None

		# First look in children. If there, then descendant is already relative to this handler.
		if name in self.children:
			descendant = self.children[name].copy()
		
		else:
			# If descendant is not a child, keep searching recursively.
			for child in self.children.values():

				descendant = child.find_descendant(name)

				if descendant is not None:
					# Found it.
					break

		if descendant is not None:
			# Translate relative to this handler and stop searching.
			descendant.top_left_x += self.top_left_x
			descendant.top_left_y += self.top_left_y
			
		return descendant

	def get_descendant(self, name):
		''' Find and return a descendant, but with its original position in its parent handler. '''

		descendant  = None

		# First look in children. If there, then descendant is already relative to this handler.
		if name in self.children:
			descendant = self.children[name]
		
		else:
			# If descendant is not a child, keep searching recursively.
			for child in self.children.values():

				descendant = child.get_descendant(name)

				if descendant is not None:
					# Found it.
					break
			
		return descendant

	def copy(self):
		''' Creates a shallow copy of self (i.e., no children are copied).'''
		handler_copy = EventHandler(self.name, self.label, self.top_left_x, self.top_left_y, self.width, self.height)

		return handler_copy

	def draw(self, ax, origin_x=0, origin_y=0):
		''' Draws itself and all of its children.'''
		ax.add_patch(patches.Rectangle((origin_x + self.top_left_x, origin_y + self.top_left_y), self.width, self.height, fill=False))

		for child in self.children.values():
			child.draw(ax, origin_x + self.top_left_x, origin_y + self.top_left_y)

class Event():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def copy(self):
		return Event(self.x, self.y)

class MoveBodyPartEvent(Event):
	def __init__(self, body_part, x, y):
		super(MoveBodyPartEvent, self).__init__(x, y)
		self.body_part = body_part
	
	def move(self):
		pass
	
	def copy(self):
		return MoveBodyPartEvent(self.body_part, self.x, self.y)