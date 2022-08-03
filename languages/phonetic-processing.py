from constants import *
from pyphen import Pyphen
from phonemizer import phonemize
from syltippy import syllabize
import re

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


def transcription(mot: str, langue: str) -> str:
    return phonemize(
        mot,
        language=dictionnaire_transcription[langue],
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        njobs=4)


def compteur_syllabes_global(mot: str, langue: str) -> int:

    if langue == 'es':
        syllables, _ = syllabize(mot)
        return len(syllables)

    if langue in dictionnaire_syllabes_defaut.keys():
        lang = dictionnaire_syllabes_defaut[langue]
        left = 2
        right = 2
    elif langue in dictionnaire_syllabes_specifique.keys():
        lang = dictionnaire_syllabes_specifique[langue]
        left = 1
        right = 1

    dic = Pyphen(lang=lang, left=left, right=right)
    return len(dic.inserted(mot).split('-'))


def extraction_consonnes_voyelles(mot: str, langue: str) -> (list[str], list[str]):
    return (extraction_phonemes(transcription(mot, langue), dictionnaire_consonnes[langue]), 
    extraction_phonemes(transcription(mot, langue), dictionnaire_voyelles[langue]))


def extraction_phonemes(mot: str, liste_phonemes: list[str]) -> list[str]:
    phn_extr = []
    for phoneme in liste_phonemes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - \
                1 if mot.find(phoneme*2) != - 1 else compte
            phn_extr.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_extr


def main():
    pass


if __name__ == '__main__':
    main()
