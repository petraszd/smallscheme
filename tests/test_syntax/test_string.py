from smallscheme.syntax import *

def test_string_set_value():
    assert "foo" == String('"foo"').value
    assert 'foo"bar' == String('"foo\\"bar"').value
    assert 'foo\nbar' == String('"foo\\nbar"').value
    assert 'foo\tbar' == String('"foo\\tbar"').value
    assert 'foo\\bar'== String('"foo\\\\bar"').value

