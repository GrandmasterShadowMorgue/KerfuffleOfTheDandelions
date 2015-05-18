#
# SirJonSample.py
# ?
#
# None
# May 15 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import pygame
# import PyQt4, OpenGL

import geometry



class Trigger(object):

	'''
	Docstring goes here

	'''

	def __init__(self, bbox, ontriggered):

		'''
		Docstring goes here

		'''

		self.bbox = bbox
		self.ontriggered = ontriggered


	def trigger(self, position):
		# TODO: Provide arguments to ontriggered (?)
		if position in self.bbox:
			self.ontriggered()


		

class App(object):
	
	'''
	Docstring goes here

	'''
	
	def __init__(self):
		
		#
		self.size = 720, 480
		self.title = 'Sir Jon'

		self.running = True

		#
		pygame.init()
		self.surface = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		# Events
		self.listeners = {
			pygame.QUIT: lambda e: self.quit(),
			pygame.MOUSEMOTION: lambda e: None,
			pygame.MOUSEBUTTONDOWN: lambda e: None,
			pygame.MOUSEBUTTONDOWN: lambda e: None
		}

		self.noop = lambda event: None #


	def run(self):
		self.mainloop()

	def quit(self):
		self.running = False

	def mainloop(self):
		while self.running:
			event = pygame.event.poll()                      # Poll the event queue
			self.listeners.get(event.type, self.noop)(event) # Dispatch



def main():

	'''
	Docstring goes here

	'''

	App().run()



if __name__ == '__main__':
	main()