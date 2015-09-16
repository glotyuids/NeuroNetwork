# -*- coding:utf-8 -*-
import random, copy, time
from field import *
from population import Population
from person import Person
from params import *


class Genetic(object):
	"""genetic layer"""
	def __init__(self,epoch_num,pop_len,field_size=(20,15), delta = 0):
		super(Genetic, self).__init__()
		self.size = field_size 
		# self.field = Field(self)
		self.pop_len = pop_len
		self.population = Population(self.pop_len,8,4,delta = delta)

		self.epoch_num = epoch_num
		self.score_history = []
		self.best_pers = None
		self.best_ever = [-1,None]
		self.time = None
		self.bp_hist = []

############ ADD COEFFICIENTS!!!!

	def del_info(self,field,d = 2):
		field = field[d:-d]
		field = [i[d:-d] for i in field]
		return field

	def add_coefficient(self,n,f):
		COEFF[n]=f

	def get_coefficient(self,n):
		return COEFF[n]

	# def start(self):


	def start(self, f = None, analyze = 0):
		self.time = time.time()
		if DBG:
			print '---------------------'
			print 'New genetic'
			print 'Length of population:',self.pop_len
			print 'Number of epochs:',self.epoch_num
			print 'Process: ' ,
		self.score_history = []
		for i in xrange(self.epoch_num):
			fld = Field(self.size)
			fld.generate()
			pos = (random.randint(1,self.size[0]-1),random.randint(1,self.size[1]-1))# random start position
			pop_score = []
			for j in self.population.xrange_population():
				pers,score = self.move_population(j,pos,copy.deepcopy(fld))
				pop_score.append([j,pos,copy.deepcopy(fld),pers,score]) #neuronet,position,field,person,score
				self.population.population[j] = score
			best,nnb = MINUS_INFINITY,None
			for j in pop_score[:]:
				if j[-1]>best:
					best,nnb = j[-1],j
			if nnb is None:
				print pop_score
				raise Exception('Zero lifetime')
			# print nnb.history[:]
			self.score_history.append(best)
			self.best_pers = nnb[:]
			if analyze: 
				self.analyze(self.best_pers[:])
			if self.best_ever[0]<best:
				self.best_ever = [best,nnb[:]][:]
			self.generate_new_population()
			# if DBG: print `i+1` if not (i+1)%5 or i==0 else '.' ,
			if DBG and not (i+1)%5 or i==0: print `i+1` 
			if f is not None:
				if not f(i,self.best_ever):
					break
		print '\n'
		if i < self.epoch_num:
			print 'Stopped at epoch number:',i
		self.epoch_num = i
		print 'Score history last:',self.score_history[-1]
		# print pop_score
		self.save_best_neuronet()
		self.save_last_field()
		self.time  = time.time() - self.time
		print 'Time: ',self.time
		print '---------------------'
		return self.epoch_num

	def do_up(a):
		i = 0
		yield a
		while up(a):
			yield a
			i +=1
			if i > 1000000: # CONSTANT! BAD
				break

	def up(self,a,i=0,i_max=2):
		a[i] += AN_ST
		if a[i]>AN_HG:
			a[i] = AN_LOW
			if (i<len(a)-1) and (i<i_max):
				return self.up(a,i+1)
			else:
				return False
		return True

	def analyze(self,arr):
		a = [AN_LOW]*8
		out = []
		for i in do_up(a):
			arr[0].set_input(a)
			out.append(arr[0].calculate(steps = 10))
		self.bp_hist.append(out)

	def move_population(self,nn,pos,fld):
		p = Person(HEALTH)
		p.log(pos)
		a = 0
		while p.hl>0:
			nn,pos,fld,p = self.move_person(nn,pos,fld,p)
			p.log(pos)
			a+=1
			if a > 100000:
				break
				# raise Exception('Walking dead')
		score = p.get_score()
		return p,score
		#get score

	def move_person(self,nn,pos,fld,p):
		a = fld.get_info_near_pos(pos,p.get_d()) # get info around pers

		""" --> Start nn update """
		nn.set_input(a) # set input for neuronet

		''' Async neuronet work?? '''
		out = nn.calculate(steps = 10) # calculate output for neuronet
		""" <-- End nn update """
		# print 'out before : ',out
		out = map(lambda x:0 if abs(x)<TRANSITION else (-1 if x<0 else 1),out)
		# f = lambda x:0 if abs(x)<TRANSITION else (-1 if i<0 else 1)
		# out = [f(i) for i in out]
		fld.set_as_blank(pos) # null field
		g = lambda x:x//abs(x) if x!=0 else 0
		outs = [g(out[1]-out[3]),g(out[2]-out[0])]
		new_pos = [pos[0]+outs[0],pos[1]+outs[1]] # calculate new position
		if self.check_in_range(fld,new_pos): # check and apply new position
			pos = new_pos[:]
		p.apply(fld.get_field()[pos[1]][pos[0]]) # change health
		fld.move_to_pos(pos)
		return nn,pos,fld,p

	def check_in_range(self,fld,pos):
		# print pos, fld.size
		if not (0<=pos[0]<fld.size[0] and 0<=pos[1]<fld.size[1]):
			# print 'wrong pos', fld.size
			return False
		# print 'Can Move'
		return True


	def save_best_neuronet(self):
		pass

	def save_last_field(self):
		pass

	def generate_new_population(self): #p = neuronet,position,field,porson,score
		self.population.step()
		return True

	def get_score(self):
		return self.best_pers[:]


if __name__ == '__main__':
	g = Genetic(1,1,delta = -0.5)
	g.start()