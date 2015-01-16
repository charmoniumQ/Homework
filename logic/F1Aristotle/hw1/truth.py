def tfSeq(size):
    ''' Generates a list of the given size containing all combinations
nn    of True and False.  Starts with all Trues and ends with all
    Falses.
    '''

    if size > 1:        
        for head in tfSeq(size-1):
            yield head + [True]
            yield head + [False]
    else:
        yield [True]
        yield [False]

def nth_term(seq, idx):
    return [elem[idx] for elem in seq]

first_term = lambda seq: nth_term(seq, 0)
second_term = lambda seq: nth_term(seq, 1)

def lif(a, b):
    return not a or b

def truthtable(vars, funcs, conclusion):
    output = ''
    output += '\\(\n'
    
    lVars = len(vars)
    lFuncs = len(funcs)
    output += r'\begin{array}[t]{' + '|'.join(['c']*lVars) + '||' + '|'.join(['c']*lFuncs) + '||cl}' + '\n'

    labels = first_term(vars) + first_term(funcs) + first_term([conclusion])
    output += ' & '.join(labels) + r' \\'
    output += '\n\\hline\n\\hline\n'

    tfText = {True:'T', False:'F'}

    for tf in tfSeq(len(vars)):
        values = [tfText[val] for val in tf]
        values += [tfText[func[1](*tf)] for func in funcs]
        values += [tfText[conclusion[1](*tf)]]
        values += [('*' if conclusion[1](*tf) else '*\ !') if all([func[1](*tf) for func in funcs]) else '']
        output += ' & '.join(values) + '\\\\\n'


    output += r'\end{array}'
    output += '\n\)\n'

    return output

def argument_summary(vars, funcs, conclusion):
    output  = '\\item\n'
    output += '{\n'
    output += '\n'.join(['$' + var + '$: ' + desc + '\\\\' for var, desc in vars]) + '\n'
    output += '\\(\n'
    output += '\n'.join([func[0] + ' \\\\' for func in funcs]) + '\n'
    output += '\\line \\\\ \n'
    output += conclusion[0] + '\n'
    output += '\\)\n'
    output += '}\n\n'
    output += '\\item\n'
    output += truthtable(vars, funcs, conclusion)

    return output
