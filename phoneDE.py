from syllables import estimate
from phonemizer import phonemize
import re

consonnes = ['tsj', 'ən', 'əm', 'əl', 'ər', 'ɜ', 'pf', 'ts', 'tʃ', 'dʒ', 'ʃt', 'b', 'd', 'ɡ', 'm', 'n', 'ŋ', 'p', 't', 'k', 'f', 'θ', 's', 'ʃ', 'ç', 'x', 'z', 'ʒ', 'j', 'ʝ', 'ʁ', 'r', 'ɾ', 'ɐ', 'ʀ', 'h', 'l', ]
voyelles = ['aː', 'ɑː', 'aɪ', 'aʊ', 'a', 'ɑ', 'ɛː', 'ɛ', 'ɔʏ', 'eː', 'ə', 'ɪ', 'iː', 'ɔ', 'oː', 'œ', 'øː', 'ʊ', 'uː', 'ʏ', 'yː']

mot = input('Entrez un mot en allemand : ')


phn = phonemize(
    mot,
    language='de',
    backend='espeak',
    strip=True,
    preserve_punctuation=True,
    njobs=4)


def extract_consonnes(mot: str) -> list[str]:
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes


def extract_voyelles(mot: str) -> list[str]:
    phn_voyelles = []
    for phoneme in voyelles:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_voyelles.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_voyelles


def extract_consonnes_v2(mot: str) -> tuple[list[str], str]:
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes, mot


def extract_consonnes_voyelles(mot: str) -> tuple[list[str], list[str]]:
    liste_consonnes, reste = extract_consonnes_v2(mot)
    liste_voyelles = extract_voyelles(reste)
    return liste_consonnes, liste_voyelles


phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
# phn_consonnes, phn_voyelles = extract_consonnes_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')

