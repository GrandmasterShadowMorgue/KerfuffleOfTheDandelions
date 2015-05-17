#
# mozart.py
# ?
#
# Jonatan H Sundqvist
# May 17 2015
#
# Adapted from an example found here (https://people.csail.mit.edu/hubert/pyaudio/)

# TODO | - Implement with coroutines (?)
#        - 

# SPEC | -
#        -



import pyaudio

import queue
import threading
import time

import tkinter



class Mozart(object):

	'''
	Docstring goes here

	'''

	def __init__(self):

		'''
		Docstring goes here

		'''

		#

		# Stream parameters
		self.CHUNKSIZE  = 1024  #
		self.WIDTH      = 2     # ?
		self.CHANNELS   = 2     # Number of channels
		self.SAMPLERATE = 44100 # Sample rate (samples per second)

		#
		self.pyaudio = pyaudio.PyAudio() #
		self.stream  = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.WIDTH),
			                             channels=self.CHANNELS,
			                             rate=self.SAMPLERATE,
			                             input=True,
			                             output=True,
			                             frames_per_buffer=self.CHUNKSIZE)

		#
		self.queue = queue.Queue() #

	
	def read(self, duration, oncomplete):
		for i in range(0, int(self.SAMPLERATE/self.CHUNKSIZE * duration)):
			self.queue.put(self.stream.read(self.CHUNKSIZE))
		oncomplete()


	def write(self, duration, oncomplete):
		for i in range(0, int(self.SAMPLERATE/self.CHUNKSIZE * duration)):
			self.stream.write(self.queue.get(), self.CHUNKSIZE)
		oncomplete()



def delayedPlayback():

	'''
	Docstring goes here

	'''
	
	duration = 20  #
	delay    = 2.6 #

	mozart = Mozart()
	print('Recording...')
	threading.Thread(target=lambda: mozart.read(duration, lambda: print('Done recording'))).start()
	time.sleep(delay)
	print('Playing...')
	threading.Thread(target=lambda: mozart.write(duration, lambda: print('Done playing'))).start()



def keyToSpeak():

	'''
	Docstring goes here

	'''

	app = tk.Tk()
	app.title('Speak')
	app.geometry('{width}x{height}'.format(width=500, height=500))

	def speak(event):
		
	speaking = False

	mozart = Mozart()


	app.mainloop()



def main():
	
	'''
	Docstring goes here

	'''

	delayedPlayback()




if __name__ == '__main__':
	main()