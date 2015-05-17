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
	# TODO: Normalisations (constructor and possibly attribute assignments), mapping
	# TODO: Use complex for points and vectors (?)
	# TODO: Coordinate systems (agnostic, or make assumptions?)

	# TODO: Shrink or pad (uniformly or one edge), nudge (eg. move), place (incl. anchors)

	def __init__(self, left, right, top, bottom):

		'''
		Docstring goes here

		'''

		self.left   = min(left, right)
		self.right  = max(left, right)
		self.top    = min(top, bottom)
		self.bottom = max(top, bottom)


	def hAligned(self, point):
		return self.left <= point.real <= self.right # Point is horizontally aligned (eg. on or between the left and right edges)


	def vAligned(self, point):
		return self.top <= point.real <= self.bottom # Point is vertically aligned (eg. on or between the top and bottom edges)


	def __in__(self, point):
		return self.hAligned(point) and self.vAligned(point) # Point is inside the Rectangle


	def __str__(self):
		return 'Rectangle(left={left}, right={right}, top={top}, bottom={bottom})'.format(left=self.left, right=self.right, top=self.top, bottom=self.bottom)


	def __eq__(self, other):
		return self.left == other.left and self.right == other.right and self.top == other.top and self.bottom == other.bottom


	def width(self):
		return abs(self.left - self.right)


	def height(self):
		return abs(self.top - self.bottom)


	def centre(self):
		return (self.left + self.right)/2 + (self.top + self.bottom)/2*1j


	def size(self):
		return self.width()+self.height()*1j


	def area(self):
		return self.width()*self.height()


	def asDict(self):
		return { 'left': self.left, 'right': self.right, 'top': self.top, 'bottom': bottom }


	def asTuple(self):
		return (self.left, self.top, self.right, self.bottom) # TODO: Order, namedtuple (?)


	def intersect(self, other):
		# TODO: Allow multiple rects (?)
		# TODO: Test graphically
		# TODO: Refactor (eg. use min with key argument)
		# TODO: Performance (eg. short-circuit if overlapX is None)
		
		overlapX = overlap(self.left, self.right, other.left, other.right)
		overlapY = overlap(self.top,  self.bottom, other.top, other.bottom)
		return Rectangle(left=overlapX[0], right=overlapX[1], top=overlapY[0], bottom=overlapY[1]) if (overlapX and overlapY) is not None else None



def overlap(amin, amax, bmin, bmax, key=lambda ln: ln[0]):
	# TODO: Rename (?)
	# TODO: Refactor
	ordered = sorted((amin, amax, bmin, bmax)) #
	return ordered[1:3] if min(((amin, amax), (bmin, bmax)), key=key) != tuple(ordered[:2]) else None
	


class Maybe(object):
	def __init__(self, value):
		self.value = value

	def apply(self, f):
		return Maybe(f(self.value)) if self.value is not None else self

	def __str__(self):
		return 'Just {0}'.format(self.value) if self.value is not None else 'Nothing'



def main():
	app = tk.Tk()
	app.title('Intersections')
	app.geometry('{0}x{1}'.format(500, 500))

	canvas = tk.Canvas(width=500, height=500) #
	canvas.pack()

	rectangles    = []
	intersections = []

	styles = {
	 'normal':    {'fill': '#28E031',  'width': 0},
	 'intersect': {'fill': '#E240B2', 'width': 0}
	}


	rects = [canvas.create_rectangle(r.asTuple(), **styles['normal']) for r in rectangles]
	inter = [canvas.create_rectangle(r.asTuple(), **styles['normal']) if r is not None else None for r in intersections]

	#
	# TODO: Clean up the input logic (state machine)
	transaction = { 'count': 0, 'drawing': False, 'anchor': None }

	def mousedown(event):
		transaction['count']   += 1   #
		transaction['drawing'] = True #

		r = Rectangle(left=event.x, right=event.x, top=event.y, bottom=event.y)
		rectangles.append(r) #
		rects.append(canvas.create_rectangle(r.asTuple(), **styles['normal']))

		transaction['anchor'] = (event.x, event.y)

		if transaction['count'] == 2:
			r = rectangles[-2].intersect(rectangles[-1])                                                          # 
			intersections.append(r)                                                                               # 
			inter.append(canvas.create_rectangle(r.asTuple(), **styles['intersect']) if r is not None else None) # 

	def mouseup(event):
		transaction['drawing'] = False
		transaction['count']   = transaction['count'] % 2 

	def mousemove(event):
		if transaction['drawing']:
			rectangles[-1] = Rectangle(left=transaction['anchor'][0], top=transaction['anchor'][1], right=event.x, bottom=event.y)
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
					inter[-1] = canvas.create_rectangle(r.asTuple(), **styles['intersect'])

	#
	app.bind('<1>', mousedown)             # 
	app.bind('<ButtonRelease-1>', mouseup) # 
	app.bind('<Motion>', mousemove)        # 

	app.mainloop()





if __name__ == '__main__':
	main()