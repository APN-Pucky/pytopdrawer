import pytopdrawer

tps = pytopdrawer.read("test.top")
for tp in tps:
	tp.show()
