from typing import List, Tuple
from syllables import estimate
from phonemizer import phonemize
import re


consonnes = ['ks', 'b', 'd','f', 'ɡ', 'k', 'l', 'ʎ', 'm', 'n', 'p', 'r', 'ɹ', 'ɾ', 'ʁ', 's', 't', 'v', 'z', 'ʃ', 'ʒ', 'ɲ']
voyelles = ['weɪŋ', 'wɐ̃ŋ', 'ɐ̃ʊ̃', 'wa', 'aʊ', 'ua', 'ue', 'õj', 'eɪŋ', 'ɐ̃j', 'aɪ', 'oɪ', 'ɔɪ', 'iɔ', 'eɪ', 'oŋ', 'ɐ̃m', 'ɐ̃ŋ', 'ũm', 'ũŋ', 'eɪm', 'eɪŋ', 'iŋ', 'ɐ', 'ɑ', 'a', 'ɛ', 'e', 'ɨ', 'i', 'o', 'ɔ', 'ʊ', 'u']

mot = input('Entrez un mot en portugais : ')


# phn is a list of 190 phonemized sentences
phn = phonemize(
    mot,
    language='pt',
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


def extract_voyelles_v2(mot: str):
    phn_voyelles= []
    for phoneme in voyelles:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_voyelles.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_voyelles, mot


def extract_consonnes_voyelles(mot: str) -> Tuple:
    liste_voyelles, reste = extract_voyelles_v2(mot)
    liste_consonnes = extract_consonnes(reste)
    return liste_consonnes, liste_voyelles


# phn_consonnes = extract_consonnes(phn)
# phn_voyelles = extract_voyelles(phn)
phn_consonnes, phn_voyelles = extract_consonnes_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')

