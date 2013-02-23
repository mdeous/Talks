#!/usr/bin/env python
# -*- coding: utf-8 -*-


def func(*args, **kwargs):
    print args
    print kwargs

func('foo', 'bar', first="baz", other="blah")
