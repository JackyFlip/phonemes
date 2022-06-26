from syllables import estimate
from phonemizer import phonemize
import re

consonnes = ['b', 'tʃ', 'd', 'ð','f', 'ɡ', 'ɣ', 'x', 'θ', 'k', 'l', 'ʎ', 'm', 'n', 'ɲ', 'p', 'r', 'ɾ', 's', 't', 'β']
voyelles = ['aɪ', 'aʊ', 'eɪ', 'eʊ', 'oɪ', 'ow', 'ja', 'wa', 'je', 'jɛ', 'we', 'jo', 'wo', 'ju', 'wi', 'a', 'e', 'i', 'o', 'u', 'j']

mot = input('Entrez un mot en espagnol : ')


phn = phonemize(
    mot,
    language='es',
    backend='espeak',
    strip=True,
    preserve_punctuation=True,
    njobs=4)


def extract_consonnes(mot: str):
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes


def extract_voyelles(mot: str):
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

