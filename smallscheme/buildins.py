from smallscheme import SchemeError
from smallscheme.datatypes import Proc, Null, Pair
from smallscheme.syntax import Number, Bool
import operator

__all__ = [
    "buildins",
    "Car",
    "Cdr",
    "Plus",
    "Minus",
    "Multiply",
    "Divide",
    "AddOne",
    "MinusOne",
    "IsZero",
    "IsNull",
    "NumberEqual",
    "NumberLess",
    "NumberMore",
    "NumberLessEqual",
    "NumberMoreEqual",
    "IsNumber",
    "SymbolEqual",
    "Display",
    "Newline",
    "IsList",
    "Not",
    "IsAtom",
    "Modulo",
]

# abstract
class Buildin(Proc):
    def __init__(self, environment):
        pass

    def __str__(self):
        for key, class_ in buildins.iteritems():
            if class_ == type(self):
                return "<#proc-buildin %s>" % key
        return "<#proc-buildin>"

    def call(self, args, name=None):
        return self._call(args)

class Car(Buildin):
    def _call(self, args):
        return args[0].car

class Cdr(Buildin):
    def _call(self, args):
        return args[0].cdr

class Plus(Buildin):
    def _call(self, args):
        return Number(sum((x.value for x in args)))

class Minus(Buildin):
    def _call(self, args):
        if len(args) == 1:
            return Number(-args[0].value)
        return Number(args[0].value - sum((x.value for x in args[1:])))

class Multiply(Buildin):
    def _call(self, args):
        return Number(reduce(operator.mul, (x.value for x in args), 1))

class Divide(Buildin):
    def _call(self, args):
        try:
            return Number(reduce(
                operator.div,
                (x.value for x in args[1:]),
                args[0].value
            ))
        except ZeroDivisionError:
            raise SchemeError("Zero division error")

class AddOne(Buildin):
    def _call(self, args):
        return Number(args[0].value + 1)

class MinusOne(Buildin):
    def _call(self, args):
        return Number(args[0].value - 1)

# abstract
class BoolResult(Buildin):
    def _call(self, args):
        if self.condition(args):
            return Bool('#t')
        return Bool('#f')

class IsZero(BoolResult):
    def condition(self, args):
        return args[0].value is 0

class IsNull(BoolResult):
    def condition(self, args):
        return args[0] is Null

class NumberEqual(BoolResult):
    def condition(self, args):
        return args[0].value == args[1].value

class NumberLess(BoolResult):
    def condition(self, args):
        return args[0].value < args[1].value

class NumberMore(BoolResult):
    def condition(self, args):
        return args[0].value > args[1].value

class NumberLessEqual(BoolResult):
    def condition(self, args):
        return args[0].value <= args[1].value

class NumberMoreEqual(BoolResult):
    def condition(self, args):
        return args[0].value >= args[1].value

class IsNumber(BoolResult):
    def condition(self, args):
        return type(args[0].value) == int

class SymbolEqual(BoolResult):
    def condition(self, args):
        return args[0].index == args[1].index

# abstract
class Output(Buildin):
    def __init__(self, environment):
        self.environment = environment

    def _call(self, args):
        self.environment.write(self.out(args))
        return Null

class Display(Output):
    def out(self, args):
        return str(args[0])

class Newline(Output):
    def out(self, args):
        return "\n"

class IsList(BoolResult):
    def condition(self, args):
        item = args[0]
        if item is Null:
            return True
        if isinstance(item, Pair):
            return item.islist()
        return False

class Not(BoolResult):
    def condition(self, args):
        if not isinstance(args[0], Bool):
            raise SchemeError("Not.call: not param must be bool")
        return not args[0].value

class IsAtom(BoolResult):
    def condition(self, args):
        return getattr(args[0], 'is_atom', False)

class Modulo(Buildin):
    def _call(self, args):
        return Number(args[0].value % args[1].value)

buildins = {
    "car": Car,
    "cdr": Cdr,
    "+": Plus,
    "-": Minus,
    "*": Multiply,
    "/": Divide,
    "1+": AddOne,
    "1-": MinusOne,
    "zero?": IsZero,
    "null?": IsNull,
    "=": NumberEqual,
    "<": NumberLess,
    ">": NumberMore,
    "<=": NumberLessEqual,
    ">=": NumberMoreEqual,
    "eq?": SymbolEqual,
    "display": Display,
    "newline": Newline,
    "list?": IsList,
    "not": Not,
    "atom?": IsAtom,
    "modulo": Modulo,
}

