# -*- coding: utf-8 -*-
from neuronet import NeuroNet
import networkx as nx
import matplotlib.pyplot as plt

class Draw(object):
	"""docstring for Draw"""
	def __init__(self, nw):
		super(Draw, self).__init__()
		self.nw = nw

	def draw_network(self):
		a = {}
		G = nx.DiGraph()
		a[self.nw.input_layer] = 'In'
		a[self.nw.output_layer] = 'Out'
		for x,i in enumerate(self.nw.layers):
			a[i] = x+2
		# for i in a:
		# 	G.add_node(a[i])
		# 	print `i`
		for i in a:
			# print '----------\n',i
			for j in i.next_layer:
				# G.add_edge(`i`.split()[-1][:-1],`j`.split()[-1][:-1])
				G.add_edge(a[i],a[j])
		# pos = nx.random_layout(G)
		# nx.draw(G, pos)

		# nx.draw_circular(G)

		pos=nx.spring_layout(G,iterations=200)
		nx.draw(G,pos,node_color=range(len(a)),node_size=400,cmap=plt.cm.Blues)
		plt.show()

if __name__ == '__main__':
	nn = NeuroNet(4,4,10)
	for i in xrange(100):
		nn.rand_add_layer()
	dr = Draw(nn)
	dr.draw_network()

