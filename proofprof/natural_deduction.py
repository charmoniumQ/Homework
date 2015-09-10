import itertools
import heapq
from tree import *

def land(arg1, arg2):
    truthtable = {
        (T, T): T,
        (T, F): F,
        (F, T): F,
        (F, F): F,
    }
    return FunctionTerm('and', (arg1, arg2), r'\wedge', truthtable)

def lor(arg1, arg2):
    truthtable = {
        (T, T): T,
        (T, F): T,
        (F, T): T,
        (F, F): F,
    }
    return FunctionTerm('or', (arg1, arg2), r'\vee', truthtable)

def lif(premise, conclusion):
    truthtable = {
        (T, T): T,
        (T, F): F,
        (F, T): T,
        (F, F): T,
    }
    m = FunctionTerm('if', (premise, conclusion), r'\rightarrow', truthtable)
    m.premise = premise # extra attributes
    m.conclusion = conclusion
    return m

def liff(arg1, arg2):
    truthtable = {
        (T, T): T,
        (T, F): F,
        (F, T): F,
        (F, F): T,
    }
    return FunctionTerm('iff', (arg1, arg2), r'\leftrightarrow', truthtable)

def lnot(arg):
    truthtable = {
        (T, ): F,
        (F, ): T,
    }
    m = FunctionTerm('not', (arg,), r'\neg', truthtable)
    m.complement = arg
    return m

def rules_():
    # I want the following variables to be inside a namespace
    # that is insulated from the module-level namespace
    p = Variable('p')
    q = Variable('q')
    r = Variable('r')

    equivalent_rules = [
        (lor(p, T), T, 'Domination for "or"'),
        (land(p, F), F, 'Domination for "and"'),
        (lor(p, q), lor(q, p), 'Commutativity of "or"'),
        (land(p, q), land(q, p), 'Commutativity of "and"'),
        (lor(p, lor(q, r)), lor(lor(p, q), r), 'Associativity of "or"'),
        (land(p, land(q, r)), land(land(p, q), r), 'Associativity of "and"'),
        (land(p, lor(q, r)), lor(land(p, q), land(p, r)), 'Distributivity of "or" over "and"'),
        (lor(p, land(q, r)), land(lor(p, q), lor(p, r)), 'Distributivity of "and" over "or"'),
        (lnot(land(p, q)), lor(lnot(p), lnot(q)), "DeMorgan's law (1)"),
        (lnot(lor(p, q)), land(lnot(p), lnot(q)), "DeMorgan's law (2)"),
        (lif(p, q), lor(lnot(p), q), 'Conditional Disjunction'),
        (liff(p, q), land(lif(p, q), lif(q, p)), 'Definition of Biconditional'),
        (lif(p, q), lif(lnot(q), lnot(p)), 'Contraposition'),
        (land(lif(p, q), lif(p, r)), lif(p, land(q, r)), 'Page 28'),
        (land(lif(p, r), lif(q, r)), lif(land(p, q), r), 'Page 28'),
        (lor(lif(p, q), lif(p, r)), lif(p, lor(q, r)), 'Page 28'),
        (lor(lif(p, r), lif(q, r)), lif(lor(p, q), r), 'Page 28'),
        (liff(p, q), liff(lnot(p), lnot(q)), 'Page 28'),
        (liff(p, q), lor(land(p, q), land(lnot(p), lnot(q))), 'Page 28'),
        (lnot(liff(p, q)), liff(lnot(p), q), 'Page28'),
        (lor(p, land(p, q)), p, 'Absorption of "or" over "and"'),
        (land(p, lor(p, q)), p, 'Absoprtion of "and" over "or"'),
    ] + \
    [
        (lnot(lnot(p)), p, 'Double negation'),
        (lor(p, F), p, 'Identity property for "or"'),
        (land(p, T), p, 'Identity property for "and"'),
        (lor(p, p), p, 'Idempotence for "or"'),
        (land(p, p), p, 'Idempotence for "and"'),
        (lor(p, lnot(p)), p, 'Negation law for "and"'),
        (land(p, lnot(p)), p, 'Negation law for "or"'),
    ]

    inference_rules = [
        (land(lif(p, q), p), q, 'Modus Ponens'),
        (land(lif(p, q), lnot(q)), lnot(p), 'Modus Tollens'),
        (land(lif(p, q), lif(q, r)), lif(p, r), 'Hypothetical Syllogism'),
        (land(lor(p, q), lnot(p)), q, 'Disjunctive Syllogism'),
        (land(p, q), p, 'Simplification'),
        (p, lor(p, q), 'Addition'),
        (land(lor(p, q), lor(lnot(p), r)), lor(q, r), 'Resolution'),
    ]

    equivalent_rules += [(q, p, reason) for p, q, reason in equivalent_rules]

    inference_rules += equivalent_rules
    return equivalent_rules, inference_rules

equivalent_rules, inference_rules = rules_()

def str_dict(dict_):
    return {str(k): str(v) for k, v in dict_.items()}

def fit_pattern(rule, term, rule_to_term=None):
    if not rule_to_term: rule_to_term = {}
    if isinstance(rule, Constant):
        return rule_to_term if rule == term else False
    if isinstance(rule, Variable):
        if rule not in rule_to_term:
            # first occurence of this variable in the rule
            # in which case that defines the variable to schema translation
            # and the rule matches the pattern
            rule_to_term[rule] = term
            return rule_to_term
        else:
            # on subsequent occurences, the schema must
            # match whatever expression it matched earlier
            return rule_to_term if rule_to_term[rule] == term else False
    if isinstance(rule, FunctionTerm):
        if len(rule.children()) != len(term.children()) or rule.f != term.f:
            return False
        for rule_child, term_child in zip(rule.children(), term.children()):
            rule_to_term = fit_pattern(rule_child, term_child, rule_to_term)
            if not rule_to_term:
                return False
        return rule_to_term

def replace(schema, replace_map):
    if isinstance(schema, Variable):
        return replace_map[schema]
    if isinstance(schema, Constant):
        return schema
    if isinstance(schema, FunctionTerm):
        new_args = []
        for arg in schema.args:
            new_args.append(replace(arg, replace_map))
        replaced = schema.deepcopy()
        replaced.args = new_args
        return replaced

class ProvenTerm (Term):
    def __init__(self, conclusion, premise, reason, fit):
        # inherits all data from conclusion
        # unless overriden below.
        self.conclusion = conclusion
        self.premise = premise
        self.reason = reason
        self.fit = fit

    def argument_str(self):
        out = ''
        if isinstance(self.premise, ProvenTerm):
            # continuation of a proof
            # here is the previous part of the proof:
            out = self.premise.argument_str() + '\n'
        else:
            # begining of a proof
            # here is the initial part of the proof:
            out = str(self.premise) + '\n' + '-' * 40 + '\n'
        return out + '{self.conclusion!s}  (by {self.reason})'.format(**locals())

    def __repr__(self):
        return 'ProvenTerm({0!r}, {1!r}, {2!r}, {3!r})'.format(self.conclusion, self.premise, self.reason, self.fit)

    def __getattr__(self, name):
        # if unable to find self.name,
        # look up self.conclusion.name
        return getattr(self.conclusion, name)

    # i have to manually reference the parent object
    # otherwise python automatically (?) defines a different __hash__ and __str__

    def __hash__(self):
        return hash(self.conclusion)

    def __str__(self):
        return '{self.conclusion!s}  (by {self.reason})'.format(**locals())

def could_imply(a, b):
    variables = list(term.get_variables())
    for truths in itertools.product([T, F], repeat=len(variables)):
        case = dict(zip(variables, truths))
        # Tell me if:
        # not (a -> b)
        # not (not a or b)
        # not not a and not b
        # a and not b
        if a.evaluate(case) and not b.evaluate(case):
            return False
    return True

import collections
c = collections.Counter()
def proove(claims, goal, rules, steps=100):
    claimshp = heapq.heapify(claims)
    claimsst = set(claims)
    for hypothesis, conclusion, name in inference_rules:
        if set(hypothesis.get_variables()) < set(conclusion.get_variables()):
            continue
        while steps > 0:
            premise = heapq.heappop(heaphp)
            fit = fit_pattern(hypothesis, premise)
            if fit:
                deduction = ProvenTerm(replace(conclusion, fit), premise, name, fit)
                if deduction not in claims and could_imply(deduction, goal) and not fit_pattern(lnot(lnot(lnot(lnot(Variable('p'))))), deduction):
                    heapq.heappush(claimshp, deduction)
                    claimsst.add(deduction)
                    c[name] += 1

    #print('\n'.join(map(str, c.most_common(10))))
    return claims

def proove_breadth(premises, rules):
    p = Variable('p')
    claims = set(premises)
    for hypothesis, conclusion, name in inference_rules:
        if set(hypothesis.get_variables()) < set(conclusion.get_variables()):
            continue
        for premise in premises:
            fit = fit_pattern(hypothesis, premise)
            if fit:
                deduction = replace(conclusion, fit)
                if deduction not in claims and not fit_pattern(lnot(lnot(lnot(lnot(p)))), deduction):
                    claims.add(ProvenTerm(deduction, premise, name, fit))
                    c[name] += 1
    for premise in premises:
        if isinstance(premise, FunctionTerm):
            # arg_eqs = [[arg1, arg1_eq1, arg1_eq2, ...], [arg2, arg2_eq1, arg2_eq2, ...], ...]
            arg_eqs = [[arg.deepcopy()] for arg in premise.args]
            for i, arg in enumerate(premise.args):
                arg_eqs[i].extend(proove_breadth([arg], equivalent_rules))
            args_deductions = itertools.product(*arg_eqs)
            for args_deduction in args_deductions:
                deduction = premise.deepcopy()
                deduction.args = args_deduction
                if deduction not in claims and not fit_pattern(lnot(lnot(lnot(lnot(p)))), deduction):
                    claims.add(deduction)

    #print('\n'.join(map(str, c.most_common(10))))
    return claims

def proove_depth(premises, conclusion, rules, steps=2):
    if steps <= 0:
        return False
    if conclusion in premises:
        return [premise for premise in premises if premise == conclusion][0]
    print('-----------------', steps, len(premises))
    print('\n'.join(map(str, premises)))
    premises.add(T)
    premises = proove_breadth(premises, rules)
    return proove_depth(premises, conclusion, rules, steps - 1)
