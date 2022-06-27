from pyphen import Pyphen
from phonemizer import phonemize
import re


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
    dic = Pyphen(lang='en_GB')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


consonnes = ['tʃ', 'dʒ', 'p', 't', 'k', 'f', 'θ', 's', 'z', 'ʃ', 'h', 'b', 'd', 'ɡ', 'v', 'ʒ', 'ŋ', 'l', 'm', 'n', 'ɹ', 'ð']
voyelles = ['iː', 'uː', 'ɜː', 'ɔː', 'ɑː', 'aʊ', 'eɪ', 'ɔɪ', 'əʊ', 'aɪ', 'ɪ', 'ʊ', 'ɛ', 'ɐ', 'a', 'ʌ', 'ɒ', 'ə', 'j', 'w']

mot = input('Entrez un mot en anglais : ')

phn = phonemize(
    mot,
    language='en-gb',
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
