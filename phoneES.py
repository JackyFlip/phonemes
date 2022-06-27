from pyphen import Pyphen
from phonemizer import phonemize
from syllables import estimate
from math import ceil
import re

consonnes = ['b', 'tʃ', 'd', 'ð','f', 'ɡ', 'ɣ', 'x', 'θ', 'k', 'l', 'ʎ', 'm', 'n', 'ɲ', 'p', 'r', 'ɾ', 's', 't', 'β']
voyelles = ['w', 'a', 'e', 'i', 'o', 'u', 'j', 'ɛ']

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


def compteur_syllabes(mot: str):
    dic = Pyphen(lang='es')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)

mot_split, nb_syllabes = compteur_syllabes(mot)
nb_syllabes_rework = ceil((nb_syllabes + estimate(mot)) /2)

print()
print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes_rework} syllabe(s)')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')

