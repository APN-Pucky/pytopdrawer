import pytopdrawer
from pytopdrawer import topplot


def test_clear_plotext(monkeypatch):
    clear_names = ("clear_figure", "clf", "clear_data")
    for clear_name in clear_names:
        for name in clear_names:
            monkeypatch.setattr(topplot.plt, name, None, raising=False)
        monkeypatch.setattr(topplot.plt, clear_name, lambda: None)
        topplot._clear_plotext()


def test_read():
    pytopdrawer.read("tests/test.top")


def test_read_show():
    tps = pytopdrawer.read("tests/test.top")
    for tp in tps:
        print(tp.title.text)
        tp.show()
