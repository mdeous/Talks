#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

CONSTANT_VAR = 'some constant value'


class SomeClass(object):
    class_attribute = 'attribute value'

    def __init__(self):
        self.instance_attribute = 'attribute value'

    def method(self):
        print "something"


def function(arg, named_arg='default value'):
    print "something else, much more interesting!"
