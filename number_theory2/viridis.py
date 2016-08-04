#!/usr/bin/env python3

import sys
from matplotlib.cm import viridis, ScalarMappable
from matplotlib.colors import Normalize
import json

sc = ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap=viridis)

def value_to_color(value):
    r, g, b, a = map(lambda x: int(x*255), sc.to_rgba(value))
    return (r, g, b)

output = [[(0, 0, 0)]]
for d in range(1, int(sys.argv[1]) + 1):
    row = []
    for n in range(0, d+1):
        row.append(value_to_color(n/d))
    output.append(row)
print(json.dumps(output))
