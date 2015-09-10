from __future__ import print_function

# MetaMath system overview
# http://us.metamath.org/mpegif/mmset.html#scaxioms

# Barnes's logic texbook
# https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxiYXJuZXNsb2dpY2YxM3xneDo2NjBjYjQ2ZWQwMTZiNDI1

# Soundness and completeness
# https://en.wikipedia.org/wiki/Propositional_calculus#Soundness_and_completeness_of_the_rules
# https://en.wikipedia.org/wiki/Completeness_(logic)

# Davis-Putnam algorithm
# https://www.cs.cmu.edu/~emc/15414-f12/lecture/propositional_logic.pdf

# Stuff
# https://en.wikipedia.org/wiki/Resolution_(logic)
# https://en.wikipedia.org/wiki/Substitution_(logic)
# https://en.wikipedia.org/wiki/Unification_(computer_science)

# Logical systems
# https://en.wikipedia.org/wiki/List_of_logic_systems
# http://home.utah.edu/~nahaj/logic/systems/

from tree import *
from natural_deduction import *
from truthtable import *

p = Variable('p')
q = Variable('q')
r = Variable('r')
s = Variable('s')
t = Variable('t')

myterm = lif(p, land(lor(q, r), liff(s, lnot(t))))
print(str(myterm) == '(p if ((q or r) and (s iff not t)))')

print(myterm.prefix(parens=True) == r'\rightarrow(p, \wedge(\vee(q, r), \leftrightarrow(s, \neg(t))))')
print(myterm.prefix(parens=False) == r'\rightarrow p \wedge \vee q r \leftrightarrow s \neg t')
print(myterm.infix() == r'(p \rightarrow ((q \vee r) \wedge (s \leftrightarrow \neg t)))')
print(myterm.postfix(parens=False) == r'p q r \vee s t \neg \leftrightarrow \wedge \rightarrow')
print(myterm.postfix(parens=True) == r'(p, ((q, r)\vee, (s, (t)\neg)\leftrightarrow)\wedge)\rightarrow')
print(myterm.get_variables() == set([p, q, r, s, t]))
print(eval(repr(myterm)) == myterm)

mytermcopy = myterm.deepcopy()
print(mytermcopy == myterm)
print(mytermcopy is not myterm)

mytermcopy.args[0] = lnot(t)
print(mytermcopy != myterm)

case1 = {p: T, q: T, r: T, s: T, t: T}
print(myterm.evaluate(case1) == F)

case2 = {p: T, q: T, r: T, s: T, t: F}
print(myterm.evaluate(case2) == T)

a = Variable('a')
b = Variable('b')
c = Variable('c')

def str_dict(dict_):
    return {str(k): str(v) for k, v in dict_.items()}

myrule = lif(a, land(b, c))

#print(str_dict(fit_pattern(myrule, myterm)))
print(fit_pattern(myrule, myterm) == {a: p, b: lor(q, r), c: liff(s, lnot(t))})

# rule with back references
# as in 'a' is used twice
myrule = land(a, lor(a, b))
myterm2 = land(lif(p, q), lor(lif(p, q), lif(r, s)))
print(fit_pattern(myrule, myterm2) == {a: lif(p, q), b: lif(r, s)})
fit = fit_pattern(myrule, myterm2)

print(replace(myrule, fit) == myterm2)

print(pretty_print_truth_table(myrule) ==
r'''\begin{array}{c|c||l}
a & b & (a \wedge (a \vee b)) \\
\hline
T & T & T \\
T & F & T \\
F & T & F \\
F & F & F \\
\end{array}''')

mypterm = ProvenTerm(myterm, myterm2, 'Law of Trying To Test Software', {})
print(myterm == mypterm)
# proventerms and other terms need to be interchangeable in a dictionary
# I assert that {myterm: 'hi'}[mypterm] == 'hi'
print(hash(myterm) == hash(mypterm))
print(mypterm.argument_str() ==
'''((p if q) and ((p if q) or (r if s)))
----------------------------------------
(p if ((q or r) and (s iff not t)))  (by Law of Trying To Test Software)''')

mypterm2 = ProvenTerm(land(p, q), mypterm, 'Law of still trying to test software', {})
print(mypterm2.argument_str() ==
'''((p if q) and ((p if q) or (r if s)))
----------------------------------------
(p if ((q or r) and (s iff not t)))  (by Law of Trying To Test Software)
(p and q)  (by Law of still trying to test software)''')

print()
print(pretty_print_truth_table(lif(land(lnot(p), lor(p, q)), q)))

#print('\n'.join(map(str, proove_breadth([lor(p, q)], equivalent_rules))))
#print(proove_depth([land(lor(p, q), lor(lnot(p), q))], q, inference_rules).argument_str())
print(proove_depth(set([lnot(lif(p, q))]), land(p, lnot(q)), equivalent_rules))
#not (p if q)
#not (not p or q)
#not not p and not q
#p and not q

#print(proove_depth(set([land(lor(land(p, q), r), lif(r, s))]), lor(p, s), inference_rules))


# Bad things:
# may not halt
# from [a, b] deduce land(a, b)
# from [a] deduce lor(a, b)
# and other rules with a free variable in the conclusion
