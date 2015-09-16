# -*- coding:utf-8 -*-
import random, copy
from params import *

class Field(object):
	"""field for neuronetwork"""
	def __init__(self,size,bw = 0.5):
		super(Field, self).__init__()
		BASE_WEIGHT = bw
		self.size = size[:]
		self.weight = BASE_WEIGHT
		self.layers = []
		field = self.generate_blank_field() 
		self.layers.append(copy.deepcopy(field[:])) # Пустое поле - 0 слой
		self.layers.append(copy.deepcopy(field[:])) # Поле с расположенными на них предметами - 1 слой
		self.layers.append(copy.deepcopy(field[:])) # Поле с объектами, 2 слой

		self.tsf = TILESET_FILE


	def get_info_near_pos(self,ps,d = 1,info = -1):
		fld = self.add_info(d+1,info)
		pos = ps[0]+d+1,ps[1]+d+1

		n = [sum([COEFF[fld[pos[1]-(i+1)][j]] for j in xrange(pos[0]-i,pos[0]+i+1)]) for i in xrange(d+1)]
		s = [sum([COEFF[fld[pos[1]+(i+1)][j]] for j in xrange(pos[0]-i,pos[0]+i+1)]) for i in xrange(d+1)]
		w = [sum([COEFF[fld[j][pos[0]-(i+1)]] for j in xrange(pos[1]-i,pos[1]+i+1)]) for i in xrange(d+1)]
		e = [sum([COEFF[fld[j][pos[0]+(i+1)]] for j in xrange(pos[1]-i,pos[1]+i+1)]) for i in xrange(d+1)]

		nw, ne, se, sw = [],[],[],[]
		for i in xrange(d+1):
			tmpnw, tmpne, tmpsw, tmpse = 0,0,0,0
			
			tmpnw += COEFF[fld[pos[1]-(i+1)][pos[0]-(i+1)]]
			tmpne += COEFF[fld[pos[1]-(i+1)][pos[0]+(i+1)]]
			tmpsw += COEFF[fld[pos[1]+(i+1)][pos[0]-(i+1)]]
			tmpse += COEFF[fld[pos[1]+(i+1)][pos[0]+(i+1)]]

			for j in xrange(i):
				tmpnw += COEFF[fld[pos[1]-(j+1)][pos[0]-(i+1)]]
				tmpnw += COEFF[fld[pos[1]-(i+1)][pos[0]-(j+1)]]
				
				tmpne += COEFF[fld[pos[1]-(j+1)][pos[0]+(i+1)]]
				tmpne += COEFF[fld[pos[1]-(i+1)][pos[0]+(j+1)]]
			
				tmpsw += COEFF[fld[pos[1]+(j+1)][pos[0]-(i+1)]]
				tmpsw += COEFF[fld[pos[1]+(i+1)][pos[0]-(j+1)]]
			
				tmpse += COEFF[fld[pos[1]+(j+1)][pos[0]+(i+1)]]
				tmpse += COEFF[fld[pos[1]+(i+1)][pos[0]+(j+1)]]
			
			nw.append(tmpnw)
			ne.append(tmpne)
			sw.append(tmpsw)
			se.append(tmpse)
		out = [n,ne,e,se,s,sw,w,nw]
		out = [sum(x*1./(i+1) for i,x in enumerate(n)) for n in out]

		return out

	def add_info(self,d = 1,info = -1,all_rewrite = 0):
		if all_rewrite:
			for n,i in enumerate(self.layers):
				inf = info if n else 0
				field = i 
				field = [[inf]*d+i+[inf]*d for i in field]
				self.layers[n] = [[inf]*len(field[0])]*d+field+[[inf]*len(field[0])]*d
			field = None
		else:
			field = self.get_field()
			field = [[info]*d+i+[info]*d for i in field]
			field = [[info]*len(field[0])]*d+field+[[info]*len(field[0])]*d
		return field

	def generate_blank_field(self):
		return [[0]*self.size[0] for i in xrange(self.size[1])]

	def fill_by_type(self,tp,weight=BASE_WEIGHT,rewrite = 0,field = None,set_base = 1):
		if field == None:
			field = self.layers[FIELD][:]
		ln = len(field[0])
		for i in xrange(len(field)):
			for j in xrange(ln):
				if (rewrite or (field[i][j] == 0)) and (weight>random.random()):
						field[i][j] = tp
		self.layers[FIELD] = field[:]
		self.layers[BASEF] = copy.deepcopy(field[:])
		return field

	def check_coord(self, coord):
		if (0<=coord[0]<self.size[0] and 0<=coord[1]<self.size[1]):
			return True
		return False

	def change_field(self,tp,pos,field=None):
		if type(tp) == type(''):
			tp = self.get_type(tp)
		if field == None:
			field = copy.deepcopy(self.layers[FIELD][:])
		if self.check_coord(pos):
			field[pos[1]][pos[0]] = tp
		self.layers[FIELD] = copy.deepcopy(field[:])
		return copy.deepcopy(field)

	def change_base(self,tp,pos):
		if type(tp) == type(''):
			tp = self.get_type(tp)
		if self.check_coord(pos):
			self.layers[BASEF][pos[1]][pos[0]] = tp
		return True

	def set_as_blank(self,pos):
		if self.check_coord(pos):
			self.layers[FIELD][pos[1]][pos[0]] = self.layers[BLANKF][pos[1]][pos[0]]
			self.layers[BASEF][pos[1]][pos[0]] = self.layers[BLANKF][pos[1]][pos[0]]

	def get_field(self):
		return self.layers[FIELD][:]

	def get_blank(self):
		return self.layers[BLANKF][:]

	def get_base(self):
		return self.layers[BASEF][:]

	def generate(self):
		for i in FILL:
			# print 'FILL by ',i,FILL[i]
			self.fill_by_type(i,weight = FILL[i][0], rewrite = FILL[i][1])

	def get_type(self,s):
		if s == 'floor':
			return FLOOR
		elif s == 'person':
			return PERS
		elif s == 'dead':
			return DEAD
		elif s == 'way':
			return WAY
		return None

	def return_to_base(self):
		self.layers[FIELD] = copy.deepcopy(self.layers[BASEF])
		return True

	def move_to_pos(self,pos):
		self.change_base('way',pos) #change floor
		self.return_to_base()
		self.change_field('person',pos)
		return pos