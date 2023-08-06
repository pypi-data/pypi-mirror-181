from testerinopepperino.testerinopepperino import TesterinoPepperino


def test_print():
    x = TesterinoPepperino()
    x.hello_world()
    assert x.x == 3

def test_lol():
    assert 1 == 1
