#
# main.py
# Entry point for the game
#
# Jayant Shivarajan, Jonatan H Sundqvist
# May 15 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



def main():

	'''
	Docstring goes here

	'''

	print(noIntegersPlease(5.2, 3+3j, 5e2j))



def decorator(f):
	def enhanced(*args, **kwargs):
		assert all(not isinstance(arg, int) for arg in args)
		print('Hurrah, no integers! I just hate them soo much! Haughty bastards...')
		return f(*args, **kwargs)
	return enhanced



def prohibit(types):
	def wrapper(f):
		def restricted(*args, **kwargs):
			for arg in args:
				for t in types:
					assert not isinstance(arg, t), 'Arrrgh, I hate {0}s!'.format(t)
			return f(*args, **kwargs)
		return restricted
	return wrapper




@prohibit((int, float, tuple, dict))
def noIntegersPlease(*args):
	return sum(args)



if __name__ == '__main__':
	main()