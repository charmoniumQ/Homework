from __future__ import print_function
from itertools import tee

__all__ = ['memoize_iterator', 'memoize_generator']

class memoize_iterator(object):
    # one class for each original-iterator I source from
    def __init__(self, it):
        self.initial = it
        self.clear()
    def clear(self):
        self.initial, self.it = tee(iter(self.initial))
        self.cache = []
    def __call__(outside):
        class new_iterator(object):
            # one class for each memoized-iterator I create
            def __init__(self):
                self.outside = outside
                self.idx = 0
            def __iter__(self):
                return self
            def next(self):
                return self.__next__()
            def __next__(self):
                while self.idx >= len(outside.cache):
                    outside.cache.append(next(outside.it))
                self.idx += 1
                return outside.cache[self.idx - 1]
        return new_iterator()

class memoize_generator(object):
    def __init__(self, gen):
       self.gen = gen
       self.cache = {}
    def clear():
        self.cache = {}
    def __call__(self, *args):
        if args in self.cache:
            # make a new memoized iterator
            return self.cache[args]()
        else:
            value = memoize_iterator(self.gen(*args))
            self.cache[args] = value
            return value()

if __name__ == '__main__':
    def ranger(n):
        for i in range(n):
            yield i
    ranger = memoize_generator(ranger)

    print()
    list(ranger(10))
    print(ranger(10).outside.cache)
    ranger(10).outside.clear()
    list(zip(ranger(10), xrange(5)))
    print(ranger(10).outside.cache)
    list(ranger(20))
    print(ranger(20).outside.cache)
    print(ranger.cache)
    it = range(10)
    ngen = memoize_iterator(it)
    ngen.clear()
    a = ngen()
    b = ngen()
    print (zip(a, range(5)))
