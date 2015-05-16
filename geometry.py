#
# geometry.py
# Utilities for dealing with geometry
#
# Jonatan H Sundqvist
# May 15 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import tkinter as tk
import random



class Rectangle(object):

	'''
	Docstring goes here

	'''

	# TODO: Immutable, slots (?)
	# TODO: Performance (cpu, ram) (eg. caching)
	# TODO: Descriptor (?)
	# TODO: Boolean operations (operators?)
	# TODO: Normalisations, mapping
	# TODO: Use complex for points and vectors (?)
	# TODO: Coordinate systems (agnostic, or make assumptions?)

	# TODO: Shrink or pad (uniformly or one edge), nudge (eg. move), place (incl. anchors)

	def __init__(self, left, right, top, bottom):

		'''
		Docstring goes here

		'''

		self.left   = left
		self.right  = right
		self.top    = top
		self.bottom = bottom


	def hAligned(self, point):
		return min(self.left, self.right) <= point.real <= max(self.left, self.right) # Point is horizontally aligned (eg. on or between the left and right edges)


	def vAligned(self, point):
		return min(self.top, self.bottom) <= point.real <= max(self.top, self.bottom) # Point is vertically aligned (eg. on or between the top and bottom edges)


	def __in__(self, point):
		return self.hAligned(point) and self.vAligned(point) # Point is inside the Rectangle


	def width(self):
		return abs(self.left - self.right)


	def height(self):
		return abs(self.top - self.bottom)


	def centre(self):
		return (self.left + self.right)/2 + (self.top + self.bottom)/2*1j


	def size(self):
		return self.width()+self.height()*1j


	def asDict(self):
		return { 'left': self.left, 'right': self.right, 'top': self.top, 'bottom': bottom }


	def asTuple(self):
		return (self.left, self.top, self.right, self.bottom) # TODO: Order, namedtuple (?)


	def intersect(self, other):
		# TODO: Test graphically
		# TODO: Refactor (eg. use min with key argument)
		horizontal = sorted((self.left, self.right, other.left, other.right)) #
		xOverlap = horizontal[1:3] if (horizontal[0] in (self.left, self.right)) != (horizontal[1] in (self.left, self.right)) else None
		
		vertical = sorted((self.top, self.bottom, other.top, other.bottom)) #
		yOverlap = vertical[1:3] if (vertical[0] in (self.top, self.bottom)) != (vertical[1] in (self.top, self.bottom)) else None

		if xOverlap == None or yOverlap == None:
			return None
		else:
			return Rectangle(left=xOverlap[0], right=xOverlap[1], top=yOverlap[0], bottom=yOverlap[1])



class Maybe(object):
	def __init__(self, value):
		self.value = value

	def apply(self, f):
		return Maybe(f(self.value)) if self.value is not None else self

	def __str__(self):
		return 'Just {0}'.format(self.value) if self.value is not None else 'Nothing'


def main():
	print(Rectangle(5, 20, 10, 40).intersect(Rectangle(5, 15, 10, 50)))
	value = Maybe(5).apply(lambda v: v * 2)
	print(value)

	app = tk.Tk()
	app.title('Intersections')
	app.geometry('{0}x{1}'.format(500, 500))

	canvas = tk.Canvas(width=500, height=500) #
	canvas.pack()

	rectangles    = []
	intersections = []


	rects = [canvas.create_rectangle((r.left, r.top, r.right, r.bottom), fill='white', width=1) for r in rectangles]
	inter = [canvas.create_rectangle((r.left, r.top, r.right, r.bottom), fill='orange', width=1) if r is not None else None for r in intersections]

	#
	# TODO: Clean up the input logic (state machine)
	transaction = { 'count': 0, 'drawing': False }

	def mousedown(event):
		transaction['count'] = (transaction['count'] + 1) # % 2 #
		transaction['drawing'] = True

		r = Rectangle(left=event.x, right=event.x, top=event.y, bottom=event.y)
		rectangles.append(r) #
		rects.append(canvas.create_rectangle(r.asTuple(), fill='white', width=1))

		if transaction['count'] == 2:
			r = rectangles[-2].intersect(rectangles[-1])                                                          # 
			intersections.append(r)                                                                               # 
			inter.append(canvas.create_rectangle(r.asTuple(), fill='orange', width=1) if r is not None else None) # 

	def mouseup(event):
		transaction['drawing'] = False
		transaction['count']   = transaction['count'] % 2 

	def mousemove(event):
		if transaction['drawing']:
			rectangles[-1].right  = event.x
			rectangles[-1].bottom = event.y
			canvas.coords(rects[-1], rectangles[-1].asTuple())

			if transaction['count'] == 2:
				r = rectangles[-2].intersect(rectangles[-1])
				intersections[-1] = r #
				if r is None:
					if inter[-1] is not None:
						canvas.coords(inter[-1], (0,0,0,0))
				elif inter[-1] is not None:
					canvas.coords(inter[-1], r.asTuple())
				else:
					inter[-1] = canvas.create_rectangle(r.asTuple(), fill='orange', width=1)

	#
	app.bind('<1>', mousedown)             # 
	app.bind('<ButtonRelease-1>', mouseup) # 
	app.bind('<Motion>', mousemove)        # 

	app.mainloop()





if __name__ == '__main__':
	main()