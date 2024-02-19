import pytopdrawer

def test_read():
	pytopdrawer.read("tests/test.top")

def test_read_show():
	tps = pytopdrawer.read("tests/test.top")
	for tp in tps:
		print(tp.title.text)
		tp.show()
