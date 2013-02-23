#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Fonction décoratrice
def add_one(func):
    print "Decorator initialized"
    def fake_square(n):
        print "Before original function call"
        orig_result = func(n)
        print "After original function call"
        return orig_result + 1
    return fake_square

# Classe décoratrice
class add_one(object):
    def __init__(self, func):
        print "Decorating initial function"
        self.func = func

    def __call__(self, n):
        print "Before initial function call"
        orig_result = self.func(n)
        print "After initial function call"
        return orig_result + 1

# Utilisation
@add_one
def square(n):
    return n * n

# ou
def square(n):
    return n * n
square = add_one(square)

# Validation d'arguments
class validate_args(object):
    def __init__(self, *arg_types):
        print "Creating decorator"
        self.arg_types = arg_types
    def __call__(self, func):
        print "Decorating initial function"
        def wrapper(*args):
            print "Before initial function call (validating args)"
            for arg, arg_type in zip(args, self.arg_types):
                if not isinstance(arg, arg_type):
                    raise TypeError("Wrong argument type received")
            retval = func(*args)
            print "After initial function call"
            return retval
        return wrapper

@validate_args(int, list)
def some_function(i, l):
    print i, l

some_function(1, [1, 2])
some_function(1, 2)