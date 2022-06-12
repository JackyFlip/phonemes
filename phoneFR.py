# need to pip install requests
import requests
from syllables import estimate
from phonemizer import phonemize
from phonemizer.separator import Separator
import re

# text is a list of 190 English sentences downloaded from github
# url = (
#     'https://gist.githubusercontent.com/CorentinJ/'
#     '0bc27814d93510ae8b6fe4516dc6981d/raw/'
#     'bb6e852b05f5bc918a9a3cb439afe7e2de570312/small_corpus.txt')
# text = requests.get(url).content.decode()
# text = [line.strip() for line in text.split('\n') if line]


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


def extract_consonnes(mot: str) -> List:
    phn_consonnes = []
    for phoneme in consonnes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - 1 if mot.find(phoneme*2) != - 1 else compte
            phn_consonnes.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_consonnes


def extract_voyelles(mot: str) -> List:
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


# phn is a list of 190 phonemized sentences
phn = phonemize(
    mot,
    language='fr-fr',
    backend='espeak',
    strip=True,
    preserve_punctuation=True,
    njobs=4)

# print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s)')
# print(f'consonne(s) : {compteur_consonnes(phn)} ; voyelle(s) : {compteur_voyelles(phn)}')

phn_consonnes = extract_consonnes(phn)
phn_voyelles = extract_voyelles(phn)
n_consonnes = len(phn_consonnes)
n_voyelles = len(phn_voyelles)


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
