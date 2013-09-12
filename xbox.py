import pygame
from pygame.locals import *

class Xbox_Control:
	def __init__(self,joy=0,_debug=False):
		try:
			pygame.init()
		except:
			pass
		try:
			self.control=pygame.joystick.Joystick(joy)
			self.control.init()
		except:
			print "No Xbox control detected!"

		self.axis=[0,0,0,0,0,0]
		self.buttons_raw=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.buttons=[0,0]
		self.change=False
		self.debug=_debug
		self.data=[0,0,0,0,0,0,0,0]

	def get_data(self):
		buf=[0,0,0,0,0,0]
		for event in pygame.event.get():
			if event.type == JOYAXISMOTION:
				for i in range(6):
					if i==2 or i==5:
						if int((self.control.get_axis(i)+1)*5)>=3:
							buf[i]=int((self.control.get_axis(i)+1)*5)
						else:
							buf[i]=0;
					else:
						if abs(int(self.control.get_axis(i)*10))>=3:
							buf[i]=self.control.get_axis(i)
						else:
							buf[i]=0;
			elif event.type == JOYBUTTONDOWN:
				self.buttons_raw[event.button]=1
			elif event.type == JOYBUTTONUP:
				self.buttons_raw[event.button]=0
			elif event.type == JOYHATMOTION:
				if self.control.get_hat(0)[1]==1:
					self.buttons_raw[13]=1 					#Button Up
				if self.control.get_hat(0)[1]==-1:
					self.buttons_raw[14]=1 					#Button Down
				if self.control.get_hat(0)[1]==0:
					self.buttons_raw[13]=0
					self.buttons_raw[14]=0
				if self.control.get_hat(0)[0]==1:
					self.buttons_raw[11]=1 					#Button Right
				if self.control.get_hat(0)[0]==-1:
					self.buttons_raw[12]=1 					#Button Left
				if self.control.get_hat(0)[0]==0:
					self.buttons_raw[11]=0
					self.buttons_raw[12]=0
			self.axis=[int(buf[0]*10),int(buf[1]*-10),int(buf[3]*10),int(buf[4]*-10),buf[2],buf[5]]
		if self.axis!=[0,0,0,0,0,0] or self.buttons_raw!=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
			self.buttons=[0,0]
			for i in range(0,8):
				self.buttons[0]+=self.buttons_raw[i]*(2**i)
				self.buttons[1]+=self.buttons_raw[i+8]*(2**i)
			self.make_data()
			self.change=True
			if self.debug:
				print self.data
			return True
		else:
			if self.change:
				self.axis=[0,0,0,0,0,0]
				self.buttons_raw=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				self.buttons=[0,0]
				self.change=False
				self.data=[0,0,0,0,0,0,0,0]
				if self.debug:
					print self.data
				return True
			return False

	def starting(self):
		while 1:
			self.get_data()
			if self.axis==[0,0,0,0,0,0] and self.change:
				return True

	def make_data(self):
		for i in range(6):
			if self.axis[i] < 0:
				self.data[i]=255+self.axis[i]
			else:
				self.data[i]=self.axis[i]
		self.data[6]=self.buttons[0]
		self.data[7]=self.buttons[1]
