from typing import List, Tuple
from syllables import estimate
from phonemizer import phonemize
import re


consonnes = ['tʃ', 'dz', 'dʒ', 'ts', 'b', 'd', 'f', 'ɡ', 'ʎ', 'j', 'k', 'l', 'm', 'n', 'ɲ', 'p', 'r', 's', 'ʃ', 't', 'v', 'w', 'z']
voyelles = ['a', 'e', 'ɛ', 'i', 'ɪ', 'o', 'ɔ', 'u', 'ʊ']

mot = input('Entrez un mot en italien : ')


# phn is a list of 190 phonemized sentences
phn = phonemize(
    mot,
    language='it',
    backend='espeak',
    strip=True,
    preserve_punctuation=True,
    njobs=4)


def extract_consonnes(mot: str) -> List:
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes


def extract_voyelles(mot: str) -> List:
    phn_voyelles = []
    for phoneme in voyelles:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_voyelles.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_voyelles




phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')

