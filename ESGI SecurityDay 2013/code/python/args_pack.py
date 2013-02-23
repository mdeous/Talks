#!/usr/bin/env python
# -*- coding: utf-8 -*-


def func(i, j, first=None, other=None, last=None):
    print i, j
    print first, other, last

args = ('foo', 'bar')
kwargs = {'first': 'baz', 'other': 'blah'}
func(*args, **kwargs)
