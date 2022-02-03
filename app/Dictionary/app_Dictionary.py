#!/usr/bin/python3 -B

import random
from SimpleDict import TLearnDict


def Learn():
    Dict = TLearnDict()
    #Dict.LoadFile('eng-ukr.dic')
    #Dict.LoadFile('eng-ukr-computer.dic')
    Dict.LoadFiles(['eng-ukr.dic', 'eng-ukr-computer.dic'])

    print()
    Dict.Info()

    Mode = bool(random.getrandbits(1))
    Dict.SetDict(Mode)

    print('Random words:')
    Dict.ShowRand(10)

    print()
    Dict.Learn()

Learn()
