from smallscheme import SchemeError
from smallscheme import datatypes

__all__ = [
    "Tree", "Node", "Quote", "Set",
    "Cons", "List", "Define", "If",
    "Lambda", "Begin", "Cond", "Call",
    "Atom", "String", "Number", "Symbol",
    "Variable", "Bool", "And", "Or",
    "ProcBody",
]

class Tree(object):
    def __init__(self):
        self.root = Node()

    def evaluate(self, env):
        return self.root.evaluate(env)

class Node(object):
    def __init__(self, parent=None):
        self.is_atom = False
        self.childs = []
        self.parent = parent

    def add_child(self, child):
        self.childs.append(child)

    def evaluate(self, env):
        if not self.childs:
            raise SchemeError("None.evaluate: can't evaluate empty Node")
        for c in self.childs[:-1]:
            c.evaluate(env)
        return self.childs[-1].evaluate(env)

# Complex
class Quote(Node):
    def evaluate(self, env):
        def construct(childs):
            p = datatypes.Null
            for c in reversed(childs):
                if c.is_atom:
                    p = datatypes.Pair(Symbol("'" + str(c.value)), p)
                else:
                    p = datatypes.Pair(construct(c.childs), p)
            return p
        return construct(self.childs)

class Set(Node):
    def evaluate(self, env):
        if len(self.childs) != 2:
            raise SchemeError('Set.evaluate: must contain two params')
        env.set(self.childs[0], self.childs[1].evaluate(env))
        return datatypes.Null

class And(Node):
    def evaluate(self, env):
        for c in self.childs:
            result = c.evaluate(env)
            if not isinstance(c, Bool):
                raise SchemeError("And.evaluate: not boolean")
            if not result.value:
                return Bool('#f')
        return Bool('#t')

class Or(Node):
    def evaluate(self, env):
        for c in self.childs:
            result = c.evaluate(env)
            if not isinstance(result, Bool):
                raise SchemeError("Or.evaluate: not boolean")
            if result.value:
                return Bool('#t')
        return Bool('#f')

class Cons(Node):
    def evaluate(self, env):
        if len(self.childs) != 2:
            raise SchemeError("Cons.evaluate: wrong number of params")
        return datatypes.Pair(self.childs[0].evaluate(env),
                              self.childs[1].evaluate(env))

class List(Node):
    def evaluate(self, env):
        if not self.childs:
            return datatypes.Null
        childs = [x.evaluate(env) for x in self.childs]
        pair = datatypes.Pair(childs[-1], datatypes.Null)
        for c in reversed(childs[:-1]):
            pair = datatypes.Pair(c, pair)
        return pair

class Define(Node):
    def evaluate(self, env):
        if len(self.childs) != 2:
            raise SchemeError("Define.evaluate: wrong number of params")
        env.define(self.childs[0], self.childs[1].evaluate(env))
        return datatypes.Null

class If(Node):
    def evaluate(self, env):
        return self.evaluate_till_last(env).evaluate(env)

    def evaluate_till_last(self, env):
        if_stmt = self.childs[0].evaluate(env).value
        if if_stmt is True:
            return self.childs[1]
        elif if_stmt is False:
            if len(self.childs) > 2:
                return self.childs[2]
            else:
                return Bool('#f')
        raise SchemeError("If.evaluate condition is not bool")


class ProcBody(Node):
    def evaluate_till_last(self, env):
        if not self.childs:
            raise SchemeError("ProcBody: must have expresions")
        for c in self.childs[:-1]:
            c.evaluate(env)
        last = self.childs[-1]
        if hasattr(last, 'evaluate_till_last'):
            return last.evaluate_till_last(env)
        else:
            return last

class Lambda(Node):
    def evaluate(self, env):
        variables = self.childs[0].childs
        body = ProcBody()
        body.childs = self.childs[1:]
        return datatypes.Proc(variables, body, env.copy())

class Begin(Node):
    pass

class Cond(Node):
    def evaluate(self, env):
        return self.evaluate_till_last(env).evaluate(env)

    def evaluate_till_last(self, env):
        error_msg = "Cond.evaluate: cond doesn't have else block"
        if not self.childs:
            raise SchemeError(error_msg)
        last = self.childs[-1]
        if last.childs[0].value != "else":
            raise SchemeError(error_msg)
        last_stmt = last.childs[1]

        for test in self.childs[:-1]:
            if test.childs[0].evaluate(env).value:
                return test.childs[1]
        return last_stmt

class Call(Node):
    def evaluate(self, env):
        first = self.childs[0]
        if first.is_atom:
            name = first.value
        else:
            name = None
        proc = first.evaluate(env)
        return proc.call(self.get_arguments(env), name)

    def get_arguments(self, env):
        return [x.evaluate(env) for x in self.childs[1:]]

# Atom
class Atom(Node):
    def __init__(self, string, parent=None):
        Node.__init__(self, parent=parent)
        self.is_atom = True
        self.set_value(string)

    def set_value(self, string):
        self.value = string

    def evaluate(self, env):
        return self

    def __str__(self):
        return str(self.value)

class String(Atom):
    def set_value(self, string):
        self.value = string[1:-1].replace('\\"', '"') \
                                 .replace('\\\\', '\\') \
                                 .replace('\\n', '\n') \
                                 .replace('\\t', '\t')

class Number(Atom):
    def set_value(self, string):
        self.value = int(string)

class Symbol(Atom):
    table = []

    def set_value(self, string):
        symbol_val = string[1:]
        try:
            self.index = Symbol.table.index(symbol_val)
        except ValueError:
            self.index = len(Symbol.table)
            Symbol.table.append(symbol_val)

    @property
    def value(self):
        result = Symbol.table[self.index]
        if result == '#t' or result == '#f':
            return Bool(result).value
        elif result.isdigit():
            return Number(result).value
        return result

class Variable(Atom):
    def evaluate(self, env):
        return env.lookup(self)

class Bool(Atom):
    def set_value(self, string):
        self.value = string == '#t'

    def __str__(self):
        if self.value:
            return '#t'
        return '#f'

