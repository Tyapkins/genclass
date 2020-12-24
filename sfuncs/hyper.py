import sys
from math import log, ceil

GEN_MAX = sys.argv[1] if len(sys.argv) > 1 else 10
SIM_NUM = sys.argv[2] if len(sys.argv) > 2 else (ord('9')-ord('0') + ord('z')-ord('a'))

def hyper(size, dotnum):
	maxlen = log(dotnum)/log(SIM_NUM)
	maxlen = ceil(maxlen)
	edgelen = maxlen//GEN_MAX
	return edgelen

