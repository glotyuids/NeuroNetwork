# -*- coding: utf-8 -*-
import pygame, copy
from pygame.locals import *
from params import *
import math

#pygame.init()
class Window(object):
	def __init__(self,fld, wd=640,hg=480,caption=''):
		self.wd = wd
		self.hg = hg
		# self.fld = fld
		self.height = fld.size[0]+INFO[0]*2
		self.width = fld.size[1]+INFO[0]*2
		self.scale = TILE_WIDTH #""" TODO: """# Расчитывать ДИНАМИЧЕСКИ!!!
		self.tiles = self.load_tile_table(fld.tsf, self.scale,self.scale)
		self.cells = CELLS
		self.filename = ICON_FILENAME
		self.i_now = 0
		self.iconset = None

		self.Surface = pygame.Surface((wd,hg))
		self.windowSurfaceObj = pygame.display.set_mode((wd,hg))
		
		self.redcolor = pygame.Color(255,0,0)
		self.greencolor = pygame.Color(0,255,0)
		self.bluecolor = pygame.Color(0,0,255)
		self.whitecolor = pygame.Color(255,255,255)
		self.bkgnd_color = self.greencolor

		self.init_icon()
		self.upd_icon()
		pygame.display.set_caption(caption)
		#return self.windowSurfaceObj

	def update(self,fld):
		# draw background and coordinate grid
		self.windowSurfaceObj.fill(self.whitecolor)
		fld = copy.deepcopy(fld)
		fld.add_info(INFO[0],INFO[1],1)
		self.windowSurfaceObj.blit(self.redraw(fld),(0,0))

	def init_icon(self):
		print self.filename
		self.iconset = [pygame.transform.scale(pygame.image.load(self.filename[0]+str(i+1)+self.filename[1]).convert_alpha(), (32, 32)) for i in xrange(self.filename[2])]
	
	def upd_icon(self):
		pygame.display.set_icon(self.iconset[self.i_now])
		self.i_now += 1
		if self.i_now >= len(self.iconset):
			self.i_now = 0

	def load_tile_table(self,filename, width, height):
		image = pygame.image.load(filename).convert_alpha()
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, image_width/width):
			line = []
			tile_table.append(line)
			for tile_y in range(0, image_height/height):
				rect = (tile_x*width, tile_y*height, width, height)
				line.append(image.subsurface(rect))
		return tile_table

	def get_tile(self,tp):
		return self.tiles[self.cells[tp][0]][self.cells[tp][1]]

	def loading(self,k,WD,HG,EN,BE):
		self.Surface.fill(pygame.Color(222,222,222))
		self.windowSurfaceObj.fill((0,0xB6,0x4F))
		sf = self.redraw(BE[1][-3],0)
		sf.set_alpha(127)
		self.Surface.blit(sf,(self.scale,self.scale))
		his = [(int((i[0]+1.5)*self.scale),int((i[1]+1.5)*self.scale)) for i in BE[1][-2].history]
		pygame.draw.lines(self.Surface, (0x7d, 0, 0x57), 0, his, 3)
		for i in his:
			pygame.draw.circle(self.Surface, (0x7d, 0, 0x57), i, 3, 2)
		pygame.draw.circle(self.Surface, (0x7d, 0, 0x57), his[0], 5, 3)
		pygame.draw.arc(self.Surface, (0, 153, 153), ((WD//2-100, HG//2-100), (200, 200)), 0, math.pi*2*(k+1)/EN, 20)
		self.Surface.blit(pygame.font.SysFont("None", 50).render(str(k*100//EN)+'%', 1, (2,2,2)), (WD//2-28,HG//2-10)) 
		self.windowSurfaceObj.blit(self.Surface,(0,0))

	def redraw(self,fld,flg = 1):
		self.upd_icon()
		surface = pygame.Surface((self.wd,self.hg))
		# dt = INFO[0]*TILE_WIDTH
		for y, i in enumerate(fld.get_field()):
			for x, j in enumerate(i):
				scl = (x*self.scale, y*self.scale)
				# for i in fld.layers:
					# self.Surface.blit(self.get_tile(i[y][x]),scl)
				surface.blit(self.get_tile(fld.get_blank()[y][x]),scl)
				surface.blit(self.get_tile(fld.get_base()[y][x]),scl)
				surface.blit(self.get_tile(j), scl)
		if flg:
			self.Surface = surface
		return surface