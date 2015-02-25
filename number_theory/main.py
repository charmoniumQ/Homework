
output = r'$\{$'
for x in range(2, 101):
    if is_prime(x):
        output += r'$\circled{{{x}}}$, '.format(**locals())
    else:
        output += r'$\cancel{{{x}}}$, '.format(**locals())
output = output[:-2]
output += r'$\}$'
print output

