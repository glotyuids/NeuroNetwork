# -*- coding:utf-8 -*-
"""

"""
import random
from neuron import Neuron

MIN_NUM_OF_NEURONS = 2
MAX_NUM_OF_NEURONS = 30
NUM_OF_COLUMNS = 1

DEPTH = 3
PS = ' '
PST = PS*DEPTH

class Layer(object):
	"""layer implementation"""
	def __init__(self,num = None, next = None):
		super(Layer, self).__init__()
		if num == None:
			num = MIN_NUM_OF_NEURONS
		self.neurons = []
		self.alpha_neuron = Neuron(is4alpha = True)
		self.next_layer = []
		self.prev_layer = []
		self.history = []
		for i in xrange(num):
			self.add_neuron()
		if not(next == None):
			self.connect(next)

	def set_input(self,arr):
		if len(arr)!=len(self.neurons):
			raise Exception('Wrong input length')
		for i,x in enumerate(self.neurons):
			x.set_input(arr[i])

	def null_input(self):
		set_input([0]*len(self.neurons))

	def get_value(self):
		return [i.value for i in self.neurons]
	"""
	Добаление нейрона в слой
	"""
	def add_neuron(self):
		# return True
		if len(self.neurons) >= MAX_NUM_OF_NEURONS:
			return False
		new = Neuron()
		self.neurons.append(new)
		self.alpha_neuron.connect(new)
		for i in self.next_layer:
			for a in i.neurons:
				new.connect(a)
		for k in self.prev_layer:
			for b in k.neurons:
				b.connect(new)
		self.history.append([1,`new`])
		return True

	"""
	Удаление нейрона из слоя с ограничением на минимальное количество нейронов в слое
	"""
	def delete_neuron(self,neuron):
		if len(self.neurons) <= MIN_NUM_OF_NEURONS:
			return False
		# try:
		self.alpha_neuron.disconnect(neuron)
		for i in self.prev_layer:
			for j in i.neurons:
				del j.axon[neuron]
		del self.neurons[self.neurons.index(neuron)]
		# except Exception, e:
			# return False
		self.history.append(2)
		return True

	"""
	Добавить случайный нейрон
	"""
	def rand_add_neuron(self):
		self.add_neuron()
		return True

	"""
	Удалить случайный нейрон
	"""
	def rand_del_neuron(self):
		self.delete_neuron(random.choice(self.neurons))
		return True

	"""
	Изменение параметров случайного нейрона
	"""
	def rand_modify_neuron(self,tp):
		random.choice(self.neurons).modify(tp)
		self.history.append(3)
		return True

	# def connect_neuron(self,neuron):
	# 	for i in self.neurons:
	# 		i.connect(neuron)
	# 		self.alpha_neuron.connect(neuron)
	# 	return True

	"""
	Отработка всех нейронов в слое
	"""
	def calculate(self):
		self.alpha_neuron.calculate()
		for i in self.neurons:
			i.set_alpha(self.alpha_neuron)
		for i in self.neurons:
			# print i
			i.calculate()
		return True

	"""
	Добавить соединение с предыдущим слоем
	"""
	def add_prev_layer(self,layer):
		self.prev_layer.append(layer)
		return True

	"""
	Удалить соединение с предыдущим слоем
	"""
	def del_prev_layer(self,layer):
		while layer in self.prev_layer: 
			self.prev_layer.remove(layer)
		return True

	"""
	Соединить со следующим слоем
	"""
	def connect(self,layer):
		self.next_layer.append(layer)
		layer.add_prev_layer(self)
		for i in self.neurons:
			i.add_next_layer(layer.neurons)
		return True

	"""
	Удалить соединение со следующим слоем
	"""
	def disconnect(self,layer):
		while layer in self.next_layer: self.next_layer.remove(layer) # may be loop!
		layer.del_prev_layer(self)
		for i in self.neurons:
			i.delete_next_layer(layer.neurons)
		return True

	"""
	Для предыдущего слоя удалить все соединеине с текущим слоем
	"""
	def remove_connections(self):
		for i in self.prev_layer[:]:
			i.disconnect(self)
			for j in self.next_layer[:]:
				i.connect(j)
		# while self in self.prev_layer:
		# 	self.prev_layer.remove(self)
		# for k in self.next_layer:
		# 	k.prev_layer.remove(self)
		return True

	"""
	Изменение параметров текущего слоя
	"""
	def modify(self,tp,atp = 0):
		if tp == 0:
			self.rand_add_neuron()
		elif tp == 1:
			self.rand_del_neuron()
		elif tp == 2:
			self.rand_modify_neuron(atp)
		elif tp == 3:
			for i in self.neurons:
				i.modify(0)
		elif tp == -1:
			for i in self.neurons:
				i.modify(0)
		return True

	def set_delta(self,c):
		for i in self.neurons:
			i.set_delta(c)

	def __str__(self):
		s =  PST+'This layer:'.ljust(14)+`self`+'\n'
		s += PST+'Next layers:'.ljust(14)+`self.next_layer`+'\n'
		s += PST+'Prev layers:'.ljust(14)+`self.prev_layer`+'\n'
		s += PST+'Neurons ('+`len(self.neurons)`+'): \n'
		s += PST+'>Alpha neuron '+': '+`self.alpha_neuron`+'\n'+str(self.alpha_neuron)+'\n'
		for n,i in enumerate(self.neurons):
			s += PST+'>Neuron '+`n`+': '+`i`+'\n'+str(i)+'\n'
		return s

	def code(self,i):
		return `i`


