import time
from xbox import Xbox_Control

xbox = Xbox_Control()

def main():
	print "Push RT+LT and after thar push any button"
	xbox.starting()
	while 1:
		if xbox.get_data():
			print xbox.data

if __name__ == "__main__":
	main()