T = 'T'
I = 'I'
F = 'F'

def lnot(a):
    if a == T:
        return F
    if a == I:
        return I
    return T

def lor(a, b):
    if a == T or b == T:
        return T
    if a == I or b == I:
        return I
    return F

def land(a, b):
    if a == F or b == F:
        return F
    if a == I or b == I:
        return I
    return T

def truth_seq(size):
    if size - 1 == -1:
        yield ()
    else:
        for val in [T, I, F]:
            sub = truth_seq(size - 1)
            for sub_val in sub:
                yield (val, ) + sub_val

def nth_term(seq, idx):
    return [elem[idx] for elem in seq]

first_term = lambda seq: nth_term(seq, 0)
second_term = lambda seq: nth_term(seq, 1)

def truthtable(vars, funcs, conclusion):
    output = ''
    
    lVars = len(vars)
    lFuncs = len(funcs)
    output += r'\begin{array}[t]{' + '|'.join(['c']*lVars) + '||' + '|'.join(['c']*lFuncs) + '||cl}' + '\n'

    labels = vars + first_term(funcs) + first_term([conclusion])
    output += ' & '.join(labels) + r' \\'
    output += '\n\\hline\n\\hline\n'

    for tf in truth_seq(len(vars)):
        # fill in elements of table horizontally
        values = [val for val in tf]
        values += [func[1](*tf) for func in funcs]
        values += [conclusion[1](*tf)]
        values += [('*' if conclusion[1](*tf) == T else '*\ !') if all([func[1](*tf) == T for func in funcs]) else '']
        output += ' & '.join(values) + '\\\\\n'

    output += r'\end{array}'

    return output

print (truthtable(
    ['H', 'T', 'M'],
    [
        ('(H \land M) \lor (\lnot H \land T)', lambda H, M, Th: lor(land(H, M), land(lnot(H), Th))),
        ('(M \land T) \lor \lnot (M \lor T)', lambda H, M, Th: lor(land(M, Th), lor(lnot(M), Th)))
    ],
    ('T', lambda H, M, Th: Th)
))
