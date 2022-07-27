__all__ = ["Pair", "Null", "Proc"]

class Pair(object):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def islist(self):
        if self.cdr is Null:
            return True
        if isinstance(self.cdr, Pair):
            return self.cdr.islist()
        return False

    def __str__(self):
        if not self.islist():
            return '(%s . %s)' % (str(self.car), str(self.cdr))
        out = []
        pair = self
        while pair.cdr is not Null:
            out.append(str(pair.car))
            pair = pair.cdr
        out.append(str(pair.car))
        return '(%s)' % (' '.join(out))

class _Null(object):
    def __str__(self):
        return "()"
Null = _Null()

class Proc(object):
    def __init__(self, variables, body, environment):
        self.variables = variables
        self.body = body
        self.environment = environment

    def call(self, arguments, name=None):
        self.environment.enter()

        while 1:
            for var, val in zip(self.variables, arguments):
                self.environment.define(var, val)

            last = self.body.evaluate_till_last(self.environment)
            if hasattr(last, 'get_arguments') and \
               last.childs[0].is_atom and \
               last.childs[0].value == name:
                arguments = last.get_arguments(self.environment)
            else:
                result = last.evaluate(self.environment)
                break
        self.environment.exit()
        return result

    def __str__(self):
        if not self.variables:
            return '<#proc (lambda)>'
        return '<#proc (lambda %s)>' % (' '.join([x.value for x in self.variables]))

