from smallscheme import SchemeError
from smallscheme.buildins import buildins
from smallscheme.syntax import Variable
from smallscheme import parser
import sys

__all__ = ["Frame", "Environment", "Runner"]

class Runner(object):
    def __init__(self, out=None):
        self.environment = Environment(out)
        env = self.environment
        for name, class_ in buildins.iteritems():
            env.define(Variable(name), class_(env))
        env.enter()

    # TODO: error reporting
    def run(self, src):
        return parser.parse(src).evaluate(self.environment)

class Frame(object):
    def __init__(self):
        self.stack = {}

    def define(self, variable, expresion):
        self.stack[variable.value] = expresion

    def get(self, variable):
        return self.stack[variable.value]

    def has(self, variable):
        return self.stack.has_key(variable.value)

class Environment(object):
    def __init__(self, output=None):
        if output:
            self.output = output
        else:
            self.output = sys.stdout
        self.frames = [Frame()] # global frame

    def write(self, string):
        self.output.write(string)

    def enter(self):
        self.frames.append(Frame())

    def copy(self):
        copy = Environment(self.output)
        copy.frames = self.frames[:]
        return copy

    def exit(self):
        self.frames.pop()

    def define(self, variable, expresion):
        self.frames[-1].define(variable, expresion)

    def lookup(self, variable):
        for fr in reversed(self.frames):
            if fr.has(variable):
                return fr.get(variable)
        raise SchemeError("Environment.lookup: variable '%s' is not defined" % str(variable.value))

    def set(self, variable, expresion):
        for fr in reversed(self.frames):
            if fr.has(variable):
                fr.define(variable, expresion)
                return
        raise SchemeError("Environment.set: variable '%s' could not be found" % (variable.value))

