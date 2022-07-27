from smallscheme.syntax import *

def test_bool_set_value():
    assert True is Bool('#t').value
    assert False is Bool('#f').value

def test_str():
    assert '#f' == str(Bool('#f'))
    assert '#t' == str(Bool('#t'))

