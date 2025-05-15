#!/usr/bin/python3
import argparse
from itertools import chain
import math
import pytopdrawer
import matplotlib.pyplot as plt


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("topfile", type=str,help="url/file/string")
	parser.add_argument("-ns", "--noshow", action="store_true",help="do not show the plot")
	parser.add_argument("-ho", "--horizontal", action="store_true",help="horizontal layout")
	parser.add_argument("-v", "--vertical", action="store_true",help="vertical layout")
	parser.add_argument("-s", "--size", type=int,help="size of the plot", default=4)
	parser.add_argument("-o", "--output", help="output file", type=str, default=None)
	#parser.add_argument("-p", "--powheg", action="store_true",help="add powheg lines")
	parser.add_argument("-m","--mcfm", action="store_true",help="add mcfm lines")
	args = parser.parse_args()
	tops = pytopdrawer.read(args.topfile,not args.mcfm,args.mcfm)
	N = len(tops)
	cols = math.ceil(math.sqrt(N))   # Round up to ensure enough space
	rows = math.ceil(N / cols)       # Calculate rows based on columns
	if args.horizontal:
		rows = 1
		cols = N
	if args.vertical:
		rows = N
		cols = 1
	fig, axes = plt.subplots(rows,cols,  figsize=( cols*args.size,rows*args.size))
	for t,a in zip(tops,list(chain.from_iterable(axes))):
		t.plot(axes=a)
	if not args.noshow:
		plt.show()
	if args.output is not None:
		plt.savefig(args.output)
