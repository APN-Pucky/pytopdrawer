import pytopdrawer

def test_read():
	pytopdrawer.read("test.top")

def test_read_show():
	tps = pytopdrawer.read("test.top")
	for tp in tps:
		print(tp.title.text)
		tp.show()
