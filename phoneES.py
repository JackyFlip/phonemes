from phonemizer import phonemize
from syltippy import syllabize
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
    syllables, _ = syllabize(mot)
    nb_syllabes = len(syllables)
    mot_split = '-'.join(s for s in syllables)
    return mot_split, nb_syllabes


phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)

mot_split, nb_syllabes = compteur_syllabes(mot)

print(f'{mot} / {mot_split} / {phn} contient {nb_syllabes} syllabe(s)')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')

