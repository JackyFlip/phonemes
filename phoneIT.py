from pyphen import Pyphen
from phonemizer import phonemize
from syllables import estimate
from math import ceil
import re


consonnes = ['tʃ', 'dz', 'dʒ', 'ts', 'b', 'd', 'f', 'ɡ', 'ʎ', 'j', 'k', 'l', 'm', 'n', 'ɲ', 'p', 'r', 's', 'ʃ', 't', 'v', 'w', 'z']
voyelles = ['a', 'e', 'ɛ', 'i', 'ɪ', 'o', 'ɔ', 'u', 'ʊ']

mot = input('Entrez un mot en italien : ')


phn = phonemize(
    mot,
    language='it',
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
    dic = Pyphen(lang='it_IT', left=1, right=1)
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)

mot_split, nb_syllabes = compteur_syllabes(mot)
nb_syllables_old = estimate(mot)
nb_syllabes_rework = ceil((nb_syllabes + nb_syllables_old) /2)

print(f'Syllables [{nb_syllabes} {nb_syllables_old} {nb_syllabes_rework}]')
print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes_rework} syllabe(s)')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
