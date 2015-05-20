#
# mozart.py
# ?
#
# Jonatan H Sundqvist
# May 17 2015
#
# Adapted from an example found here (https://people.csail.mit.edu/hubert/pyaudio/)

# TODO | - Implement with coroutines (?)
#        - Figure out API

# SPEC | -
#        -



import pyaudio

import queue
import threading
import time

import tkinter as tk

from PIL import ImageTk, Image



class Mozart(object):

	'''
	Docstring goes here

	'''

	def __init__(self):

		'''
		Docstring goes here

		'''

		#
		self.playing = False

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

	
	def stop(self):
		self.playing = False


	def record(self):
		pass


	def save(self):
		pass

		
	def playback(self):
		# TODO: This method is haunted
		# TODO: This method is very inefficient
		while True:
			if self.playing:
				self.queue.put(self.stream.read(self.CHUNKSIZE))
				self.stream.write(self.queue.get(), self.CHUNKSIZE)


	def read(self, duration, oncomplete, consumer=None, async=False):
		for i in range(0, int(self.SAMPLERATE/self.CHUNKSIZE * duration)):
			self.queue.put(self.stream.read(self.CHUNKSIZE))
		oncomplete()


	def write(self, duration, oncomplete):
		for i in range(0, int(self.SAMPLERATE/self.CHUNKSIZE * duration)):
			self.stream.write(self.queue.get(), self.CHUNKSIZE)
		oncomplete()


	def cleanup(self):
		self.stream.stop_stream()
		self.stream.close()
		self.pyaudio.terminate()



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

	img    = Image.open('assets/speechbubble.png')
	img.thumbnail((64, 64), Image.ANTIALIAS)
	
	bubble = ImageTk.PhotoImage(img)
	label  = tk.Label(image=bubble)
	# label.pack()

	def speak(event):
		mozart.playing = True
		label.place(x=500-64-20, y=500-64-20)

	def stop(event):
		# mozart.stop()
		mozart.playing = False
		label.place_forget()
		# label.pack_forget()

	app.bind('v', speak)	
	app.bind('<KeyRelease-v>', stop)

	speaking = False
	mozart = Mozart()

	threading.Thread(target=lambda: mozart.playback(), daemon=True).start()

	app.mainloop()

	print('Cleaning up...')
	mozart.cleanup()



def main():
	
	'''
	Docstring goes here

	'''

	# delayedPlayback()
	keyToSpeak()



if __name__ == '__main__':
	main()