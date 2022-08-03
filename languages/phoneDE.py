from pyphen import Pyphen
from phonemizer import phonemize
from syllables import estimate
from math import ceil
import re

consonnes = ['tsj', 'pf', 'ts', 'tʃ', 'dʒ', 'b', 'd', 'ɡ', 'm', 'n', 'ŋ', 'p', 't', 'k', 'f', 'v' ,'θ', 's', 'ʃ', 'ç', 'x', 'z', 'ʒ', 'ʁ', 'r', 'ɾ', 'ɐ', 'h', 'l']
voyelles = ['aː', 'aɪ', 'aʊ', 'a', 'ɛː', 'ɛ', 'eː', 'ə', 'ɪ', 'iː', 'ɔ', 'oː', 'œ', 'øː', 'ø', 'ʊ', 'uː', 'y', 'yː', 'j', 'ɑ̃', 'ɔ̃', 'ɑː']


def extract_consonnes(mot: str):
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes


def extract_consonnes_new(mot: str):
    phn_consonnes = []
    phn_distribution = []
    for lettre in mot:
        if lettre in consonnes:
            phn_consonnes.extend([lettre])
            phn_distribution.append(0)
        else:
            phn_distribution.append(1)
    return phn_consonnes,phn_distribution


def construction_liste_consonnes(phn: str) -> list[str]:
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in phn:
            phn_consonnes.extend([phoneme])
            phn.replace(phoneme, '', 1)
    print(f'Liste de consonnes: {phn_consonnes}')
    return phn_consonnes


def construction_liste_voyelles(phn: str) -> list[str]:
    phn_voyelles = []
    for phoneme in voyelles:
        if phoneme in phn:
            phn_voyelles.extend([phoneme])
            phn.replace(phoneme, '', 1)
    print(f'Liste de voyelles: {phn_voyelles}')
    return phn_voyelles




def extract_consonnes_voyelles_new(phn: str):
    phn_consonnes = []
    phn_voyelles = []
    phn_distribution = []

    for lettre in phn:
        if lettre in consonnes:
            phn_consonnes.extend([lettre])
            phn_distribution.append(0)
        elif lettre in voyelles:
            phn_voyelles.extend([lettre])
            phn_distribution.append(1)
    return phn_consonnes, phn_voyelles, phn_distribution


def extract_voyelles(mot: str):
    phn_voyelles = []
    for phoneme in voyelles:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_voyelles.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_voyelles


def extract_consonnes_v2(mot: str):
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes, mot


def extract_consonnes_voyelles(mot: str):
    liste_consonnes, reste = extract_consonnes_v2(mot)
    liste_voyelles = extract_voyelles(reste)
    return liste_consonnes, liste_voyelles


def compteur_syllabes(mot: str):
    dic = Pyphen(lang='de_DE')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


def process_data(mot: str):

    phn = phonemize(
        mot,
        language='de',
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        njobs=4)

    consonnes = extract_consonnes_new(phn)

    return extract_consonnes_voyelles_new(phn), phn, compteur_syllabes(mot)[1]


if __name__ == '__main__':
    mot = input('Entrez un mot en allemand : ')

    phn = phonemize(
        mot,
        language='de',
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        njobs=4)

    phn_consonnes = extract_consonnes(phn)
    phn_voyelles = extract_voyelles(phn)
    n_consonnes = len(phn_consonnes)
    n_voyelles = len(phn_voyelles)

    mot_split, nb_syllabes = compteur_syllabes(mot)

    print()
    print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes} syllabe(s)')
    print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
