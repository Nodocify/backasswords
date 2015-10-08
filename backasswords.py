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

class backasswords(object):
    def __init__(self, s, key_length=5, bit_shift=False, obfuscate=True, encrypt=True, single=False):
        import os
        self.s = s
        self.key_length = key_length
        self.bit_shift = bit_shift
        self.encrypt = encrypt
        self.obfuscate = obfuscate
        self.single = single
        self.check_opts()

    def check_opts(self):
        if self.bit_shift:
            self.obfuscate = True
        if self.single:
            self.obfuscate = True

    def run(self):
        if self.encrypt:
            self.s = self.gen_brute_wrapper(self.gen_enc(self.s, self.key_length), self.key_length)
        if self.obfuscate:
            num = self.gen_num(self.s)
            if self.bit_shift:
                con = self.bitshift(num)
                self.s = self.gen_str(con)
            else:
                self.s = self.gen_str(str(num))
            if self.single:
                self.s = self.gen_single(self.s)
        return self.s

    def gen_enc(self, s, key_length):
        from itertools import cycle
        import random
        key = ''.join(str(random.randint(0,9)) for x in range(key_length))
        data = bytearray(s.encode())
        x = cycle(key)
        for i in range(len(data)):
            data[i] ^= int(next(x), 16)
        return data

    def gen_single(self, s):
        return ' '.join([y.strip() for y in s.strip().split('\n')])

    def gen_brute_wrapper(self, s, key_length):
        return """____ = %s
___ = getattr(__import__('itertools'), 'product')('0123456789',repeat=%d)
while (lambda _: _).__code__.co_nlocals:
    __ = getattr(__import__('itertools'), 'cycle')(
        (lambda: _).__code__.co_lnotab.decode().join(next(___)))
    _ = ____[:]
    for _____ in range(len(_)):
        _[_____] ^= int(next(__), True.__class__.__name__.__len__() ** (lambda __, ___: __).__code__.co_nlocals)
    if ''.join([chr(_) for _ in [112,121,116,104,111,110]]) in _.decode():
        try:
            exec(_.decode())
            break
        except:
            continue
""" % (s, key_length)

    def gen_num(self, s):
        codes = [ord(c) for c in s]
        return sum(codes[i] * 256 ** i for i in range(len(codes)))

    def gen_str(self, num):
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
""" % num

    def encode(self, num, depth):
        if num == 0:
            return "_ - _"
        if num <= 8:
            return "_" * num
        return "(" + self.bitshift(num, depth + 1) + ")"

    def bitshift(self, num, depth=0):
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
                result += self.encode(base, depth)
            else:
                result += "(%s << %s)" % (self.encode(base, depth),
                                          self.encode(shift, depth))
            num = diff if num > 0 else -diff
        return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Backasswords, an obfuscation script that will hide your plain text without changing the functionality.')
    parser.add_argument('-o', '--obfuscate',
                        action="store_true",
                        default=False,
                        help='Enable obfuscation')
    parser.add_argument('-e', '--encrypt',
                        action="store_true",
                        default=False,
                        help='Enable self-brute-forcing encryption')
    parser.add_argument('-b', '--bitshift',
                        action="store_true",
                        default=False,
                        help='Enable bitshift obfuscation, Implies obfuscation (WARNING: Takes a very long time to generate)')
    parser.add_argument('-k', '--key',
                        action="store",
                        type=int,
                        default=5,
                        dest='length',
                        help='Specify encryption key length, default = 5, Irrelevant if encryption is not in use.')
    parser.add_argument('-s', '--single',
                        action="store_true",
                        default=False,
                        help='Return output on a single line.')
    parser.add_argument('--output', action="store",
                        default=None,
                        dest='outfile',
                        help='Specify output file. If not given writes to stdout.')
    parser.add_argument('infile',
                        action="store",
                        help='Input python file to be obfuscated.')
    r = parser.parse_args()
    with open(r.infile, 'r') as f:
        data = f.read()
    y = backasswords(data, key_length=r.length, bit_shift=r.bitshift, obfuscate=r.obfuscate, encrypt=r.encrypt, single=r.single)
    fin = y.run()
    if r.outfile:
        with open(r.outfile, 'w') as f:
            f.write(fin)
    else:
        print(fin)
