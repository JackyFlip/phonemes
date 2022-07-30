from pyphen import Pyphen
from phonemizer import phonemize
from syllables import estimate
from math import ceil
import re


consonnes = ['ks', 'b', 'd','f', 'ɡ', 'k', 'l', 'ʎ', 'm', 'n', 'p', 'ɾ', 'ɹ', 'ʁ', 's', 't', 'v', 'z', 'ʃ', 'ʒ', 'ɲ']
voyelles = ['weɪŋ', 'wɐ̃ŋ', 'ɐ̃ʊ̃', 'wa', 'aʊ', 'ua', 'ue', 'õj', 'eɪŋ', 'ɐ̃j', 'aɪ', 'oɪ', 'ɔɪ', 'iɔ', 'eɪ', 'oŋ', 'ɐ̃m', 'ɐ̃ŋ', 'ũm', 'ũŋ', 'eɪm', 'eɪŋ', 'iŋ', 'ə', 'ɐ', 'ɑ', 'ɐ̃', 'ũ', 'a', 'ɛ', 'e', 'ɨ', 'i', 'o', 'ɔ', 'ʊ', 'u']

mot = input('Entrez un mot en portugais : ')


phn = phonemize(
    mot,
    language='pt',
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


def extract_voyelles_v2(mot: str):
    phn_voyelles= []
    for phoneme in voyelles:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_voyelles.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_voyelles, mot


def extract_consonnes_voyelles(mot: str):
    liste_voyelles, reste = extract_voyelles_v2(mot)
    liste_consonnes = extract_consonnes(reste)
    return liste_consonnes, liste_voyelles


def compteur_syllabes(mot: str):
    dic = Pyphen(lang='pt_PT', left=1, right=1)
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


phn_consonnes, phn_voyelles = extract_consonnes_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)

mot_split, nb_syllabes = compteur_syllabes(mot)
nb_syllables_old = estimate(mot)
nb_syllabes_rework = ceil((nb_syllabes + nb_syllables_old) /2)

print(f'Syllables [{nb_syllabes} {nb_syllables_old} {nb_syllabes_rework}]')
print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes_rework} syllabe(s)')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
