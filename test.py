import pytopdrawer

tps = pytopdrawer.read("test.top")
for tp in tps:
	print(tp.title.text)
	tp.show()
