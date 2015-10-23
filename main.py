# -*- encoding: utf-8 -*-
import sys
from game import Game

if __name__ == '__main__':
    p,n,vis,log = int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4]
    g = Game(p,n,log,vis = 0)
    g.main_loop()