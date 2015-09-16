# -*- encoding:utf-8 -*-

""" FIELD """
NOWAY = -1
FLOOR = 0
FOOD = 1
PERS = 2
GOOD = 3
DEAD = 4
WAY = 5
BAD1 = 6
PERS2 = 7

#Tileset_1
TILESET_FILE = 'tiles_1.png'
NOWAY_POS = (0,58)
FLOOR_POS = (8,2)
FOOD_POS = (21,35)
PERS_POS = (0,34)
GOOD_POS = (11,33)
DEAD_POS = (6,31)
WAY_POS = (14,30)#(2,15)
BAD1_POS = (5,53)
PERS2_POS = (8,33)

# Tileset_2
# TILESET_FILE = 'tiles_2.png'
# FLOOR_POS = (1,5)
# FOOD_POS = (6,39)
# PERS_POS = (3,17)
# DEAD_POS = (2,17)
# WAY_POS = (0,0)

CELLS = {
			NOWAY:	NOWAY_POS,
			FLOOR:	FLOOR_POS,
			FOOD:	FOOD_POS,
			PERS:	PERS_POS,
			GOOD:	GOOD_POS,
			DEAD:	DEAD_POS,
			WAY:	WAY_POS,
			BAD1:	BAD1_POS,
			PERS2:	PERS2_POS,
		}


BASEF = 0
BLANKF = 1
FIELD = 2

FIELD_SIZE = (25,15)

""" GENETIC """
COEFF = {
			NOWAY:-30, 
			FLOOR :0, 
			FOOD:2, 
			GOOD:-2, 
			DEAD:0, 
			WAY:0, 
			BAD1:-5,
			PERS2:-10,
		} # coefficients

DH_PERS2 = -100
DH_FOOD = 20
HEALTH = {
			NOWAY:-100,
			FLOOR :-10,
			FOOD:DH_FOOD,
			PERS:-50,
			GOOD:-5, 
			DEAD:0, 
			WAY:0, 
			BAD1:-30,
			PERS2:DH_PERS2,
		}
# COEFF = {i:HEALTH[i]+abs(HEALTH[FOOD]) for i in HEALTH}

BASE_WEIGHT = 10#0.3
FILL = {
			PERS2:	(0.2,1),
			# # BAD1:	(0.00001,1),
			# GOOD:	(0.3,1),
			# FOOD:	(0.5,1),
			FOOD:	(1,1)
		}

DBG = 1
TRANSITION= 0.5

""" POPULATION """

PARENT_PERCENT = 0.3
K_WEIGTH = 1.0

""" NEURON """

TYPE_SIGMOID_UP = 0
TYPE_SIGMOID_BP = 1
TYPE_LINEAR_UP = 2
TYPE_LINEAR_BP = 3
TYPE_RELAY_UP = 4
TYPE_RELAY_BP = 5

MAX_TYPE = 5

DEFAULT_WEIGHT = 0.5
DEFAULT_TYPE = 1

MIN_VALUE_ALPHA = 0.1
MAX_VALUE_ALPHA = 10

""" VISUALIZE """
INFO = 1,NOWAY
TILE_WIDTH = 32
ICON_FILENAME = ('Icons/flame_a_000','.png',6)

""" PENALTY """

PEN_BAD2 = -5
PEN_FOOD = 5

""" GENERAL """

MINUS_INFINITY = -10**6
DISTANCE = 2

""" ANALYZE """

AN_LOW = -10 	# low number for analyze input
AN_HG = 10 		# high number for analyze input
AN_ST = 1 		# delta for change input number
IN_NUM = 8
