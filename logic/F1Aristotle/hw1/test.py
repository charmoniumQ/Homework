
print truthtable(
[('A', 'You are ambitious.'), ('G', 'You will achieve your goals.'), ('M',  'Your life has meaning.')],
[(r'A \rightarrow \neg G', lambda A, G, M: not A or not G), (r'M \rightarrow A', lambda A, G, M: not M or A)],
(r'G \rightarrow \neg M', lambda A, G, M: not G or not M))

