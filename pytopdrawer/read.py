import re
import glob
import os
import numpy as np
import copy
from pytopdrawer.topplot import Join, TopPlot
import re
from smpl import plot
import pandas as pd
import matplotlib.pyplot as plt
from uncertainties import unumpy

def read(topfile,powheg=True,mcfm=False): # mcfm option is removed
	return read_powheg(topfile,powheg)


def read_powheg(topfile, powheg=True):
	topplots = []
	cur = TopPlot()
	cur_data = []
	lim = re.compile(r'set\s+limits\s+x\s+([0-9\.E\+-]+)\s+([0-9\.E\+-]+)\s+y\s+([0-9\.E\+-]+)\s+([0-9\.E\+-]+)')
	title = re.compile(r'title\s+(\w+)\s+"(.*)"')
	data = re.compile(r'([0-9\.Ee\+-]+)\s+([0-9\.Ee\+-]+)')
	join = re.compile(r'join')
	newplot = re.compile('newplot')
	with open(topfile) as topo_file:
		for line in topo_file:
			g = lim.search(line)
			if g is not None:
				cur.limits.xmin = float(g.group(1))
				cur.limits.xmax = float(g.group(2))
				cur.limits.ymin = float(g.group(3))
				cur.limits.ymax = float(g.group(4))
			g = title.search(line)
			if g is not None:
				cur.title.position = g.group(1)
				cur.title.text = g.group(2)
			g = data.search(line)
			if g is not None:
				cur_data.append([float( g.group(1)) ,float( g.group(2)) ])
			g = join.search(line)
			if g is not None:
				if len(cur_data) == 2:
					j = Join(cur_data[0][0],cur_data[0][1],cur_data[1][0],cur_data[1][1])
					cur.joins.append(j)
				else:
					cur.data = cur_data
				cur_data = []
			g = newplot.search(line)
			if g is not None:
				if powheg:
					cur.joins.append(Join(0,0,1,0))
					cur.joins.append(Join(0,0,0,1))
					cur._doskip(1)
				topplots.append(copy.deepcopy(cur))
				cur_data = []
				cur = TopPlot()
	return topplots


