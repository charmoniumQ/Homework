import itertools

# https://en.wikipedia.org/wiki/Variableic_formula
# <term> := <constant> | <variable> | f(<terms>)

class Term (object):
    pass

class Constant (Term):
    def __init__(self, value, latexvalue):
        self.value = value
        self.latexvalue = latexvalue

    def __eq__(self, other):
        return hasattr(other, 'value') and self.value == other.value

    def __hash__(self):
        return int(self.value)

    def __repr__(self):
        return 'Constant({self.value!r}, {self.latexvalue!r})'.format(**locals())

    def __str__(self):
        return str(self.latexvalue)

    def postfix(self, parens=True):
        return self.latexvalue

    def prefix(self, parens=True):
        return self.latexvalue

    def infix(self):
        return self.latexvalue
    
    def children(self):
        return []

    def evaluate(self, case):
        return self.value

    def get_variables(self):
        return set()

    def deepcopy(self):
        return Constant(self.value, self.latexvalue)

    def complexity(self):
        return 1

    def __cmp__(self):
        return self.complexity()

T = Constant(True, 'T')
F = Constant(False, 'F')

class Variable (Term):
    def __init__(self, latexname):
        self.latexname = latexname

    def __eq__(self, other):
        return hasattr(other, 'latexname') and self.latexname == other.latexname

    def __hash__(self):
        return hash(self.latexname)

    def __repr__(self):
        return 'Variable({self.latexname!r})'.format(**locals())

    def __str__(self):
        return self.latexname

    def postfix(self, parens=True):
        return str(self)

    def prefix(self, parens=True):
        return str(self)

    def infix(self):
        return str(self)
    
    def children(self):
        return []

    def evaluate(self, case):
        return case[self]

    def get_variables(self):
        return set([self])

    def deepcopy(self):
        return Variable(self.latexname)

    def complexity(self):
        return 1

    def __cmp__(self):
        return self.complexity()

def eq_array(a, b):
    return len(a) == len(b) and all(ai == bi for ai, bi in zip(a, b))

class FunctionTerm (Term):
    def __init__(self, f, args, latexf, truthtable):
        self.f = f
        self.args = args
        self.latexf = latexf
        self.truthtable = truthtable

    def __eq__(self, other):
        return hasattr(other, 'f') and hasattr(other, 'args') and self.f == other.f and eq_array(self.args, other.args)

    def infix(self):
        if len(self.args) == 1:
            return '{self.latexf} {self.args[0]}'.format(**locals())
        else:
            inbetween = ' {self.latexf} '.format(**locals())
            return '(' + inbetween.join(arg.infix() for arg in self.args) + ')'

    def prefix(self, parens=True):
        latexf = self.latexf
        if parens:
            arglist = ', '.join(arg.prefix(parens) for arg in self.args)
            return '{latexf}({arglist})'.format(**locals())
        else:
            arglist = ' '.join(arg.prefix(parens) for arg in self.args)
            return '{latexf} {arglist}'.format(**locals())

    def postfix(self, parens=True):
        latexf = self.latexf
        if parens:
            arglist = ', '.join(arg.postfix(parens) for arg in self.args)
            return '({arglist}){latexf}'.format(**locals())
        else:
            arglist = ' '.join(arg.postfix(parens) for arg in self.args)
            return '{arglist} {latexf}'.format(**locals())

    def __str__(self):
        if len(self.args) == 1:
            return '{self.f} {self.args[0]}'.format(**locals())
        else:
            inbetween = ' {self.f} '.format(**locals())
            return '(' + inbetween.join(str(arg) for arg in self.args) + ')'

    def __repr__(self):
        return 'FunctionTerm({self.f!r}, {self.args!r}, {self.latexf!r}, {self.truthtable!r})'.format(**locals())

    def __hash__(self):
        hash_ = hash(self.f)
        for child in self.children():
            hash_ ^= hash(child)
        return hash_

    def children(self):
        return self.args

    def evaluate(self, case):
        arglist = tuple([arg.evaluate(case) for arg in self.args])
        return self.truthtable[arglist]

    def get_variables(self):
        return set(itertools.chain(*[child.get_variables() for child in self.children()]))

    def deepcopy(self):
        f = self.f
        args = [arg.deepcopy() for arg in self.args]
        latexf = self.f
        truthtable = {tuple(value.deepcopy() for value in case): result.deepcopy() for case, result in self.truthtable.items()}
        return FunctionTerm(f, args, latexf, truthtable)

    def complexity(self):
        return 1 + sum([arg.complexity() for arg in self.args])

    def __cmp__(self):
        return self.complexity()
