#!/usr/bin/env python
# -*- coding: utf-8 -*-


def by(x):
    def func(y):
        return x * y
    func.__name__ = "by_%d" % x
    func.__doc__ = "Multiply given number by %d" % x
    return func


three = by(3)
print help(three)
print three(4)