import os
import struct
from typing import List, Dict

import mlconjug
import yaml

MANNER_MAP = {
    0: "plosive",
    1: "nasal",
    2: "trill",
    3: "taporflap",
    4: "fricative",
    5: "latfricative",
    6: "approximant",
    7: "latapproximant"
}


VOWEL_MAP = {
    0: "close",
    1: "closemid",
    2: "openmid",
    3: "open",
}
class Phoneme:
    manner: int # manner of articulation OR close/open
    place: int # place of articulation OR front/central/back 
    voiced: bool # voicedness OR rounded
    vowel: bool

    def __init__(self, manner = 0, place = 0, voiced = False, vowel = False):
        self.manner = manner
        self.place = place
        self.voiced = voiced
        self.vowel = vowel

    def __repr__(self):
        return self.char

    @staticmethod
    def from_code(code):
        vowel_voiced, manner, place = struct.unpack('BBB', code.to_bytes(3, byteorder = 'big'))

        return Phoneme(manner, place, bool(vowel_voiced & 2), bool(vowel_voiced & 1))

    @staticmethod
    def from_char(char):
        # Very slow
        # ugh
        with open('../data/lang/transliteration.yml') as f:
            trans_dict = yaml.load(f)
        for k, v in trans_dict.items():
            if k == 'vowel':
                continue
            for idx, j in enumerate(v):
                if j == char:
                    return Phoneme(
                        {k: v for v, k in MANNER_MAP.items()}[k],
                        idx // 2,
                        idx % 2,
                        False)

    @property
    def code(self): # Returns a unique number representing this phoneme
        return int.from_bytes(struct.pack('BBB', 
        self.vowel + (self.voiced << 1) ,
        self.manner,
        self.place), byteorder='big')


    @property
    def char(self):
        with open('../data/lang/transliteration.yml') as f:
            trans_dict = yaml.load(f)
        if self.vowel:
            mannerdict = trans_dict['vowel'][VOWEL_MAP[self.manner]]
            return mannerdict[(self.place << 1) + self.voiced]
        else:
            mannerdict = trans_dict[MANNER_MAP[self.manner]]
            if mannerdict == None:
                return None
            try:
                return mannerdict[(self.place << 1) + self.voiced]
            except IndexError:
                return None



with open('../data/lang/words/test.yml') as f:
    word_dict = yaml.load(f)