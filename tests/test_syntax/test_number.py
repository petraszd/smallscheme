from smallscheme.syntax import *

def test_number_set_value():
    assert 123 is Number("123").value

