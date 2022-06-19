from syllables import estimate
from phonemizer import phonemize
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


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
