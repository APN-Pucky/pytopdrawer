import pytopdrawer


def test_terminal_plot():
    pytopdrawer.TopPlot(data=[[0, 0], [1, 1]]).terminal_plot(
        title="test", width=20, height=8
    )


def test_terminal_plot_str():
    pytopdrawer.TopPlot(data=[[0, 0], [1, 1]]).terminal_plot_str(
        title="test", width=20, height=8
    )


def test_read():
    pytopdrawer.read("tests/test.top")


def test_read_show():
    tps = pytopdrawer.read("tests/test.top")
    for tp in tps:
        print(tp.title.text)
        tp.show()
