from constants import *
from pyphen import Pyphen
from phonemizer import phonemize
from syltippy import syllabize
import re
import numpy as np

dictionnaire_consonnes = {
    'fr': CONSONNES_FR,
    'it': CONSONNES_IT,
    'de': CONSONNES_DE,
    'en': CONSONNES_EN,
    'pt': CONSONNES_PT,
    'es': CONSONNES_ES
}

dictionnaire_voyelles = {
    'fr': VOYELLES_FR,
    'it': VOYELLES_IT,
    'de': VOYELLES_DE,
    'en': VOYELLES_EN,
    'pt': VOYELLES_PT,
    'es': VOYELLES_ES
}

dictionnaire_transcription = {
    'fr': 'fr-fr',
    'it': 'it',
    'de': 'de',
    'en': 'en-gb',
    'pt': 'pt',
    'es': 'es'
}

dictionnaire_syllabes_defaut = {
    'fr': 'fr',
    'de': 'de_DE',
    'en': 'en_US'
}

dictionnaire_syllabes_specifique = {
    'it': 'it_IT',
    'pt': 'pt_PT'
}

dictionnaire_phonemes_identiques = {
    'ʁ': 'r',
    'ɹ': 'r',
    'ɾ': 'r',
    'i:': 'i',
    'o:': 'o',
    'a:': 'a',
    'ɑ:': 'ɑ',
    'e:': 'e',
    'ɛː': 'ɛ',
    'ø:': 'ø',
    'u:': 'u',
    'y:': 'y',
    'ɔ:': 'ɔ'
}

dictionnaire_paires_identiques = {
    'v': 'f',
    'ʒ': 'ʃ',
    'z': 's',
    'b': 'p',
    'd': 't',
    'ɡ': 'k'
}

class Cognat:
    def __init__(self):
        pass
