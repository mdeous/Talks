#!/usr/bin/env python
# -*- coding: utf-8 -*-

for obj in ['foo', 42, [], {}]:
    print type(obj), isinstance(obj, object)
