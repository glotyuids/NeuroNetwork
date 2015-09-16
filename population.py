# -*- coding:utf-8 -*-
import operator, random, copy
from neuronet import NeuroNet
from params import *

class Population(object):
	"""docstring for Population"""
	def __init__(self,num,inum,onum,def_layers=3, delta = 0):
		super(Population, self).__init__()
		self.num = num
		self.def_layers = def_layers
		self.population = {NeuroNet(inum,onum,def_layers,delta = delta):0 for a in xrange(num)}
		self.w = self.generate_weight()

	def generate_weight(self):
		# k = K_WEIGTH
		# w8 = 1/54.
		# w6 = k*w8+2/54.
		# w5 = k*w6+2/18.
		# w4 = k*w5+1/18.
		# w3 = k*w4+2/18.
		# w2 = k*w3+1/16.
		# w7 = 1
		# print 'weigths:',w2,w3,w4,w5,w6,w7,w8
		w1,w2,w3,w4,w5,w6,w7 = 0.001,0.002,0.012,0.02,0.025,0.95,1
		return {w1:(0,0,0),
				w2:(1,0,0),
				w3:(2,0,0),
				w4:(2,1,0),
				w5:(2,-1,0),
				w6:(2,2,0),
				w7:(2,2,1)
			}

	def find_mutation_type(self,n):
		less = 1
		last = None
		# svi = 0
		for i in self.w:
			a = i-n
			if a<0:
				continue
			if a < less:
				less = a
				# svi = i
				last = self.w[i]
		# print 'last = ',last,'less = ',less,'svi = ',i, 'n = ',n
		# print last
		return last

	def step(self):
		self.selection()
		self.genetic_operator()
		self.new_population()

	def genetic_operator(self):
		self.choose_method()
		pass

	def choose_method(self):
		return self.find_mutation_type(random.random())

	def selection(self):
		# print 'Score of Populations = ',[self.population[i] for i in self.population]
		srt = sorted(self.population.iteritems(), key = operator.itemgetter(1))
		srt.reverse()
		# print 'srt',[i[1] for i in srt]
		pp = []
		pp.extend([i[0] for i in srt[:int(len(self.population)*PARENT_PERCENT)]])
		pp.append(srt[-1][0])
		# print 'choosed: ',[self.population[i] for i in pp]
		coeff = int(len(self.population)/len(pp))
		new_pp = []
		for i in xrange(coeff):
			arr = copy.deepcopy(pp[:])
			[j.modify(*self.choose_method()) for j in arr]
			new_pp.extend(arr)
		new_pp.extend([i[0] for i in srt[:len(self.population)-len(new_pp)]])
		self.population = {i:0 for i in new_pp}
		# print 'Generated Population = ',len(new_pp),[self.population[i] for i in self.population]
		pass

	def new_population(self):
		pass

	def xrange_population(self):
		for i in self.population:
			yield i

	def set_score(self,nn,score):
		self.population[nn] = score


if __name__ == '__main__':
	p = Population(10,16,4)
	print p.population
	print len(p.population)
	# p.selection()
	# p.selection()
	# p.selection()