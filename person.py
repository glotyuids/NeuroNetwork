# -*- coding:utf-8 -*-
from params import *

class Person(object):
	"""stats for neuronet"""
	def __init__(self,add,hl = 100,hl_max = 100,dh = -10,food_add = 20,d = DISTANCE):
		super(Person, self).__init__()
		self.hl = hl
		self.hl_max = hl_max
		self.dh = dh
		self.food_add = food_add
		self.add = add
		self.history = []
		self.d = DISTANCE
		self.penalty = 0

	def eat(self):
		return self.add_hl(self.food_add)

	def step(self):
		return self.add_hl(self.dh)

	def add_hl(self,n):
		if n == DH_PERS2:
			self.penalty += PEN_BAD2
			# print 'Stepped at PEN_BAD2'
		elif n == DH_FOOD:
			self.penalty += PEN_FOOD
		m = self.hl+n
		if m>0:
			self.hl = min(m,self.hl_max)
			return True
		self.hl = 0
		return False

	def is_alive(self):
		return self.hl>0

	def apply(self,n):
		return self.add_hl(self.add[n])

	def log(self,pos):
		self.history.append(pos)

	def get_d(self):
		return self.d

	def get_score(self):
		changes = 0 # stand at start is wrong!
		h= self.history[:]
		h = [i for x,i in enumerate(h) if i not in h[:x]] #delete all loops
		if len(h)<=1:
			return 0
		prev_d = [h[0][0]-h[1][0],h[0][1]-h[1][1]]
		prev = h[0]
		for i in h[1:]:
			pd = [prev[0]-i[0],prev[1]-i[1]]
			if pd != prev_d:
				changes += 1
				prev_d = pd[:]
			prev = i
		# changes = 1
		return len(self.history)#*changes + self.penalty

	def __str__(self):
		s = ''
		s += 'Person: '+`self`+'\n'
		s += ' max_heal'.ljust(10)+'= '+`self.hl_max`+'\n'
		s += ' dh'.ljust(10)+'= '+`self.dh`+'\n'
		s += ' food_add'.ljust(10)+'= '+`self.food_add`+'\n'
		s += ' add'.ljust(10)+'= '+`self.add`+'\n'
		s += ' history'.ljust(10)+'= '+`self.history`+'\n'
		s += ' d'.ljust(10)+'= '+`self.d`+'\n'
		return s
