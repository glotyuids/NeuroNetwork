# -*- coding: utf-8 -*-
# import pudb
import pygame, sys, copy,math,time
from pprint import pprint
from field import *
from window import Window
from genetic import Genetic
from logger import Logger
# from draw_network import Draw
from datetime import datetime as dt
import os
from pygame.locals import *

pygame.init()
pygame.font.init()
MLOG = 0

class Game(object):
	def __init__(self,p,n,log = 'log',vis = 0,al = 0): #al - plot analyze
		# pu.db
		s = """ Keyboard:
			Space - show
			Up - log now
			Down - stop"""
		print s
		self.WD = FIELD_SIZE[0]*TILE_WIDTH+INFO[0]*TILE_WIDTH*2
		self.HG = FIELD_SIZE[1]*TILE_WIDTH+INFO[0]*TILE_WIDTH*2
		# self.WD = 1024
		# self.HG = 768
		self.al = al
		self.vis = vis
		size = FIELD_SIZE
		self.timestamp = reduce(lambda x,y: str(x)+'_'+str(y),[i for i in dt.now().timetuple()][0:6])
		self.foldername = 'Logs'
		self.full_folder = self.foldername+os.sep+self.timestamp+os.sep
		self.logfile = str(p)+'_'+str(n)+'_'+str(DEFAULT_TYPE)+log
		self.mousex,self.mousey = 0,0
		self.Field = Field(size)
		self.MainWindow = None
		self.mousexy = pygame.mouse.get_pos()
		self.fpsClock = pygame.time.Clock()
		if self.vis:
			pygame.display.set_mode((self.WD,self.HG), pygame.NOFRAME)
			self.MainWindow = Window(self.Field,self.WD,self.HG)
		self.g = Genetic(p,n,field_size = size,delta = -0.5)
		self.pos = [2,2]
		self.a = None
		self.b = None
		self.his = None
		self.show = 0
		self.run = 1
		self.ep_num = 0
		self.log_now = 0
		
	def mouse_button_up(self,GameMap):
		pass

	def do_update(self,i,be):
		if not i%100:
			self.log_now = 1
		self.MainWindow.loading(i,WD=self.WD,HG=self.HG,EN=self.g.epoch_num,BE=be)
		pygame.display.update()
		self.user_action()
		self.fpsClock.tick(1)
		if self.log_now:
			l = Logger(None,self.g.score_history,self.g.time,self.logfile+str(i), folder = self.full_folder)
			l2 = Logger(None,self.g.best_ever[0],self.g.time,self.logfile+'BE'+str(i), folder = self.full_folder)
			l.log()
			l2.log()
			self.log_now = 0
		return self.run

	def do_genetic(self):
		try:
			self.ep_num = self.g.start(f = self.do_update)
		except Exception, e:
			print 'Error in genetic '+str(e)
		self.a = self.g.get_score()
		self.b = self.g.best_ever[1]
		# print self.a
		# self.Field = self.a[2]
		# pers = self.a[-2]
		# self.his = pers.history
		l = Logger(self.a,self.g.score_history,self.g.time,self.logfile, folder = self.full_folder)
		l2 = Logger(self.b,self.g.best_ever[0],self.g.time,self.logfile+'BE', folder = self.full_folder)
		l.log()
		l2.log()

	def vis_genetic(self,type_a = 1):
		if not self.vis:
			return None
		if type_a:
			self.Field = self.a[2]
			pers = self.a[-2]
			self.his = pers.history
		else:
			self.Field = self.b[2]
			pers = self.b[-2]
			self.his = pers.history

		for i in self.his:			
			# TODO:
			self.Field.move_to_pos(i)
			self.MainWindow.update(self.Field)
			self.user_action()
			# print 'Tick'
			pygame.display.update()
			self.fpsClock.tick(3)
			
		self.Field.change_field(DEAD,self.his[-1])
		self.MainWindow.update(self.Field)

	def main_loop(self):
		#score = neuronet,position,field,porson,score
		# seld.dn = Draw(a[0])
		# self.dn.draw()
		# his = [(1,1),(1,2),(2,2),(2,3),(2,4),(2,5),(1,5),(4,6),(2,5)]
		try:
			self.do_genetic()
		except Exception, e:
			print 'Error in genetic '+str(e)
		while 1:
			if self.al:
				import matplotlib.pyplot as plt
				from mpl_toolkits.mplot3d import Axes3D
				
			if self.show is not None: #??
				self.vis_genetic(self.show)
				self.show = None
			self.user_action()
			pygame.display.update()
			self.MainWindow.upd_icon()
			self.fpsClock.tick(30)
		return None

	def user_action(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == MOUSEBUTTONDOWN:
				# mouse_button_up()
				self.mousexy = pygame.mouse.get_pos()
				# 1 - LB 2 - MB 3 - RB 4 - SU 5 - SD
				pass
				
			elif event.type == MOUSEMOTION:
				self.mousexy = pygame.mouse.get_pos()

			elif event.type == MOUSEBUTTONUP:
				self.mousexy = pygame.mouse.get_pos()
				if event.button == 1:
					pass

			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					# self.pos[0] += 1
					self.show = 0
					pass
				elif event.key == K_LEFT:
					self.pos[0] -= 1
					pass
				elif event.key == K_UP:
					self.log_now = 1
					pass
				elif event.key == K_DOWN:
					self.run = 0
					pass
				elif event.key == K_SPACE:
					self.show = 1
					pass

			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

if __name__=="__main__":

	mainGame = Game(200000,67,vis = 1, al=1)
	mainGame.main_loop()
