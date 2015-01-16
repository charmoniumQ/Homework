
funcs = [
    lambda A,B: (A and B) == (not (not A or not B)),
    lambda A,B: lif(A, B) == (not A or B),
    lambda A,B: (A == B) ==  (not (not (not A or B) or not (not B or A)))
]
tfText = {True:'T', False:'F'}
output = []
for tf in tfSeq(2):
    values = [tfText[val] for val in tf]
    values += [tfText[func(*tf)] for func in funcs]
    output.append(' & '.join(values))
output = (' \\\\\n'.join(output))
print '''
\\(
\\begin{array}[t]{c|c||c||c||c}
A & B &
(A \land B) \liff \lnot (\lnot A \lor \lnot B) &
(A \lif B) \liff (\lnot A \lor B) &
(A \liff B) \liff \lnot (\lnot (\lnot A \lor B) \lor \lnot (\lnot B \lor A)) \\\\
\\hline
\\hline
'''
print output
print '''
\\end{array}
\\)
'''

