from smallscheme.syntax import *

def test_symbol_set_value():
    # needs to be cleared -- can be a lot of garbage
    Symbol.table = []
    assert Symbol("'foo").value is Symbol.table[-1]
    assert Symbol("'bar").value is Symbol.table[-1]
    assert Symbol("'foo").value is Symbol.table[-2]
    assert "foo" == Symbol("'foo").value

    assert 123 is Symbol("'123").value
    assert False is Symbol("'#f").value
    assert True is Symbol("'#t").value

