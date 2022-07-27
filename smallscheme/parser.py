import syntax
import re
from smallscheme import SchemeError

__all__ = [
    "OPEN", "CLOSE", "parse", "remove_shortcuts",
    "minimize", "totree", "analize", "convert_childs",
    "maketypes",
]

OPEN = 1
CLOSE = 2

def parse(src):
    return maketypes(totree(remove_shortcuts(minimize(remove_comments(src)))))

def remove_shortcuts(src):
    return src.replace("'()", "(list)").replace("'(", "(quote ")

def minimize(src):
    return ''.join([x.strip() for x in src.splitlines()]).replace('\t', ' ')

def remove_comments(src):
    pattern = re.compile(r'^(.*);.*$', re.M)
    return pattern.sub(r'\1', src)

def totree(src):
    tree = syntax.Tree()
    node = tree.root

    open_count = 0
    close_count = 0

    for item in analize(src):
        if item == OPEN:
            open_count += 1
            new_node = ComplexNode(parent=node)
            node.add_child(new_node)
            node = new_node
        elif item == CLOSE:
            close_count += 1
            node = node.parent
        else:
            node.add_child(SimpleNode(item, parent=node))
    if open_count != close_count:
        raise SchemeError("Syntax Error: too few parentheses...")
    return tree

def analize(src):
    accum = []

    def close_quote(src):
        from_ = 1
        while True:
            close = src[from_:].find('"')
            if src[from_ + close - 1] == '\\':
                from_ = from_ + close + 1
                continue
            return src[:(from_+close+1)], src[(from_+close+1):]

    while len(src) > 0:
        letter = src[0]
        if letter == "(" or letter == ")":
            if accum:
                yield ''.join(accum)
                accum = []
            if letter == "(":
                yield OPEN
            else:
                yield CLOSE
        elif letter == '"':
            smallscheme_str, src = close_quote(src)
            yield smallscheme_str
            src = " " + src # for last while's command
        elif letter == ' ' and len(accum) != 0:
            yield ''.join(accum)
            accum = []
        elif letter != ' ':
            accum.append(letter)
        src = src[1:]

    if accum:
        yield ''.join(accum)

class ComplexNode(syntax.Node):
    def simplify(self):
        convert_childs(self)

        if not self.childs:
            return self.to_new_type(syntax.Node, start=0)

        first = self.childs[0]
        if not first.is_atom:
            return self.to_new_type(syntax.Call, start=0)

        type_map = {
            'quote': syntax.Quote,
            'set!': syntax.Set,
            'define': syntax.Define,
            'if': syntax.If,
            'lambda': syntax.Lambda,
            'begin': syntax.Begin,
            'cond': syntax.Cond,
            'cons': syntax.Cons,
            'list': syntax.List,
            'and': syntax.And,
            'or': syntax.Or,
        }
        for val, class_ in type_map.iteritems():
            if first.value == val:
                return self.to_new_type(class_)
        return self.to_new_type(syntax.Call, start=0)

    def to_new_type(self, new_type, start=1):
        node = new_type(parent=self.parent)
        node.childs = self.childs[start:]
        return node

class SimpleNode(syntax.Atom):
    def simplify(self):
        val = self.value
        if val.startswith('"'):
            return syntax.String(val)
        elif val.startswith("'"):
            return syntax.Symbol(val)
        elif val.isdigit() or (val[1:].isdigit() and val[0] == "-"):
            return syntax.Number(val)
        elif val == '#f' or val == '#t':
            return syntax.Bool(val)
        return syntax.Variable(val)

def convert_childs(node):
    node.childs = [x.simplify() for x in node.childs]

def maketypes(tree):
    convert_childs(tree.root)
    return tree

