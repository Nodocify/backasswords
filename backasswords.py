#!/usr/bin/env python

"""
Author: Nodocify

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

def gen_num(s):
    codes = [ord(c) for c in s]
    return sum(codes[i] * 256 ** i for i in range(len(codes)))

def gen_str(num):
    return """(lambda _, __, ___, ____, _____, ______, _______, ________:
    getattr(
        __builtins__, (lambda _, __: _(_, __))(lambda _, __:
            chr(__ %% ((lambda _: _).__code__.co_nlocals << (lambda _, __, ___, ____, _____, ______, _______, ________: _).__code__.co_nlocals)) + _(_, __ // ((lambda _: _).__code__.co_nlocals << (lambda _, __, ___, ____, _____, ______, _______, ________: _).__code__.co_nlocals)) if __ else (lambda: _).__code__.co_lnotab.decode(),
            (((___ << ___) + _) << ((((___ << __) + _) << _))) - (((_____ << ___) - _) << (((((_ << ___) + _)) << _))) + (___ << ((_ << ____) - _)) - (((_ << ____) - _) << _______) - (_______ << __) + _)
    )(
         (lambda _, __: _(_, __))(lambda _, __:
            chr(__ %% ((lambda _: _).__code__.co_nlocals << (lambda _, __, ___, ____, _____, ______, _______, ________: _).__code__.co_nlocals)) + _(_, __ // ((lambda _: _).__code__.co_nlocals << (lambda _, __, ___, ____, _____, ______, _______, ________: _).__code__.co_nlocals)) if __ else (lambda: _).__code__.co_lnotab.decode(),
            %s)
    )
)(
    *(lambda _, __, ___: _(_, __, ___))(
        (lambda _, __, ___:
            [__(___[(lambda: _).__code__.co_nlocals])] +
            _(_, __, ___[(lambda _: _).__code__.co_nlocals:]) if ___ else []
        ),
        lambda _: _.__code__.co_argcount,
        (
            lambda _: _,
            lambda _, __: _,
            lambda _, __, ___: _,
            lambda _, __, ___, ____: _,
            lambda _, __, ___, ____, _____: _,
            lambda _, __, ___, ____, _____, ______: _,
            lambda _, __, ___, ____, _____, ______, _______: _,
            lambda _, __, ___, ____, _____, ______, _______, ________: _
        )
    )
)
""" % convert(num)

def encode(num, depth):
    if num == 0:
        return "_ - _"
    if num <= 8:
        return "_" * num
    return "(" + convert(num, depth + 1) + ")"

def convert(num, depth=0):
    from math import ceil, log
    result = ""
    while num:
        base = shift = 0
        diff = num
        span = int(ceil(log(abs(num), 1.5))) + (16 >> depth)
        for test_base in range(span):
            for test_shift in range(span):
                test_diff = abs(num) - (test_base << test_shift)
                if abs(test_diff) < abs(diff):
                    diff = test_diff
                    base = test_base
                    shift = test_shift
        if result:
            result += " + " if num > 0 else " - "
        elif num < 0:
            base = -base
        if shift == 0:
            result += encode(base, depth)
        else:
            result += "(%s << %s)" % (encode(base, depth),
                                      encode(shift, depth))
        num = diff if num > 0 else -diff
    return result

if __name__ == '__main__':
    import sys
    try:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
        y = gen_str(gen_num(data))
        print(y)
    except:
        print('Usage: python3 backasswords.py <script>')
