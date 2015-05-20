#
# pronounce.py
# Record pronunciations for word entries
#
# Jonatan H Sundqvist
# May 18 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import mozart
import sqlite3

import queue
import tkinter as tk



class Pronounce(object):

	'''
	Docstring goes here

	'''

	def __init__(self):

		'''
		Docstring goes here

		'''

		#
		self.size = (700, 420)

		#
		self.window = tk.Tk()          #
		self.window.title('Pronounce') #
		self.window.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))§


	def run(self):
		return self.window.mainloop()



def main():
	app = Pronounce()
	app.run()



if __name__ == '__main__':
	main()