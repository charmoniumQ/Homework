import itertools

from tree import *

def all_cases(term):
    variables = sorted(list(term.get_variables()), key=str)
    for truths in itertools.product([T, F], repeat=len(variables)):
        case = dict(zip(variables, truths))
        case[term] = term.evaluate(case)
        yield case

def pretty_print_case(case):
    output = r'\begin{array}' + '\n'
    string_case = [(atom.latexname, value.latexvalue) for atom, value in case.items()]
    for atom, value in sorted(string_case):
        output += r'{atom} & {value} \\'.format(**locals()) + '\n'
    output += '\end{array}'
    return output

def pretty_print_truth_table(term):
    truth_table = all_cases(term)
    variables = sorted(map(str, term.get_variables()))
    column_spec = '|'.join(['c']*len(variables)) + '||' + 'l'

    output = ''
    output += r'\begin{array}{' + column_spec + '}' + '\n'
    output += ' & '.join(variables) + r' & ' + term.infix() + r' \\' + '\n'
    output += r'\hline' + '\n'
    for case in truth_table:
        values = [str(case[Variable(variable)]) for variable in variables]
        output += ' & '.join(values) + ' & ' + str(case[term]) + r' \\' + '\n'
    output += r'\end{array}'
    return output
