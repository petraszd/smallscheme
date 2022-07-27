from smallscheme import parser
from smallscheme.syntax import *
from smallscheme import SchemeError
import py

def test_minimize():
    src = """
        (define (foo\tparam)
          (1+ param))
        """
    assert parser.minimize(src) == "(define (foo param)(1+ param))"

def test_remove_shortcuts():
    src = "(start '(a b c (d e) f) middle '() end)"
    expected = "(start (quote a b c (d e) f) middle (list) end)"
    assert parser.remove_shortcuts(src) == expected

def test_parse():
    assert Tree == type(parser.parse('(a b c)'))

def test_remove_comments():
    src = """
(define foo var); comment
; comment
(+ 2 3)
"""
    expected = """
(define foo var)

(+ 2 3)
"""
    assert expected == parser.remove_comments(src)

def test_totree():
    src = '(a b c (d e) f g (h))'
    tree = parser.totree(src)

    # checks structure of tree
    assert len(tree.root.childs) == 1
    assert len(tree.root.childs[0].childs) == 7

    # checks members of ree
    assert tree.root.childs[0].childs[0].is_atom

def test_totree_bad_parens():
    src = '(a (b c)'
    with py.test.raises(SchemeError):
        parser.totree(src)

def test_analize():
    src = '(aa (b c) d)'
    iterator = parser.analize(src)

    assert parser.OPEN == next(iterator)
    assert "aa" == next(iterator)
    assert parser.OPEN == next(iterator)
    assert "b" == next(iterator)
    assert "c" == next(iterator)
    assert parser.CLOSE == next(iterator)
    assert "d" == next(iterator)
    assert parser.CLOSE == next(iterator)

def test_analize_with_string():
    src = 'a "foo" "one two" "with \\" quote"'
    iterator = parser.analize(src)
    assert "a" == next(iterator)
    assert '"foo"' == next(iterator)
    assert '"one two"' == next(iterator)
    assert '"with \\" quote"' == next(iterator)

def get_first(src):
    tree = parser.maketypes(parser.totree(src))
    return tree.root.childs[0]

def test_maketypes():
    # Complex
    assert Quote == type(get_first('(quote a b c)'))
    assert Set == type(get_first('(set! foo 1)'))
    assert Define == type(get_first('(define foo 1)'))
    assert If == type(get_first('(if #t 1 2)'))
    assert Lambda == type(get_first('(lambda (x) 1)'))
    assert Begin == type(get_first('(begin (quote a) (quote b))'))
    assert Cond == type(get_first('(cond (#t 1) (else 2))'))
    assert Cons == type(get_first('(cons 1 2)'))
    assert List == type(get_first('(list 1 2)'))
    assert And == type(get_first('(and #t #f)'))
    assert Or == type(get_first('(or #t #f)'))
    assert Call == type(get_first('(foo 1 2 3)'))
    assert Call == type(get_first('((if #t foo bar) 1 2 3)'))

    # Empty node
    assert Node == type(get_first('()'))

    # Atoms
    assert String == type(get_first('"foo bar"'))
    assert Number == type(get_first('123'))
    assert Number == type(get_first('-123'))
    assert Symbol == type(get_first("'foo-bar"))
    assert Variable == type(get_first("foo-bar"))
    assert Bool == type(get_first("#f"))
    assert Bool == type(get_first("#t"))


def test_maketypes_call_has_all_childs():
    call = get_first('(foo 1 2 3)')
    assert 4 == len(call.childs)

