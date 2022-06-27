from pyphen import Pyphen
from phonemizer import phonemize
from syllables import estimate
from math import ceil
import re


def compteur_consonnes(mot: str): 
    elements = [mot.count(phoneme) for phoneme in consonnes]
    phonemes = [consonnes[i] for i, x in enumerate(elements) if x != 0]
    print('Consonnes :', phonemes)
    return sum([mot.count(phoneme) for phoneme in consonnes])

def compteur_voyelles(mot: str):
    elements = [mot.count(phoneme) for phoneme in voyelles]
    phonemes = [voyelles[i] for i, x in enumerate(elements) if x != 0]
    print('Voyelles :', phonemes)
    return sum([mot.count(phoneme) for phoneme in voyelles])


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
    dic = Pyphen(lang='fr')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


consonnes = ['ks', 'b', 'd', 'f', 'ɡ', 'k', 'l', 'm', 'n', 'ŋ', 'ɲ', 'p', 'ʁ', 's', 'ʃ', 't', 'v', 'z', 'ʒ']
voyelles = ['ɑ̃', 'a', 'ɑ', 'e', 'ɛː', 'ɛ̃', 'ɛ', 'ə', 'i', 'œ̃', 'œ', 'ø', 'o', 'ɔ̃', 'ɔ', 'u', 'y', 'j', 'w', 'ɥ']

mot = input('Entrez un mot en français : ')


phn = phonemize(
    mot,
    language='fr-fr',
    backend='espeak',
    strip=True,
    preserve_punctuation=True,
    njobs=4)

phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)

mot_split, nb_syllabes = compteur_syllabes(mot)
nb_syllabes_rework = ceil((nb_syllabes + estimate(mot)) /2)

print()
print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes_rework} syllabe(s)')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
