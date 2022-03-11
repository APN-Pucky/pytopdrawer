from unittest import skip
import numpy as np
from smpl import plot
from tqdm import tqdm


class Title:
	def __init__(self,position="top",text=""):
		self.position = position
		self.text = text
class Limits:
	def __init__(self,xmin=0,xmax=1,ymin=0,ymax=1):
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
class Join:
	def __init__(self,x1,y1,x2,y2):
		self.x1=x1
		self.y1=y1
		self.x2=x2
		self.y2=y2
	def as_arrays(self):
		return [self.x1,self.x2],[self.y1,self.y2]

class TopPlot:

	def __init__(self,limits: Limits= Limits(), title:Title =Title(), data = None,joins = None,skipentries=0):
		if data is None:
			data = []
		if joins is None:
			joins = []
		self.limits = limits
		self.title = title
		if skipentries == 0:
			self.data = np.array(data)
		else:
			self.data = np.array(data)[skipentries:,:]
		self.joins = joins

	def _doskip(self,skips=1):
		self.data = np.array(self.data)[skips:,:]

	def xdata(self):
		return self.data[:,0]

	def ydata(self):
		return self.data[:,1]

	def plot(self,**kwargs):
		plot.data(self.xdata(),self.ydata() ,fmt="-",grid=False,**kwargs)
		plot.title(self.title.text)
		for join in self.joins:
			plot.plot(*join.as_arrays(),color='k',alpha=0.3,linewidth=0.5)
	
	def show(self,**kwargs):
		self.plot(init=True,**kwargs)
		plot.show()



