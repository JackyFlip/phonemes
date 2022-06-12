# need to pip install requests
import requests
from syllables import estimate
from phonemizer import phonemize
from phonemizer.separator import Separator
import re


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


consonnes = ['tʃ', 'dʒ', 'p', 't', 'k', 'f', 'θ', 's', 'ʃ', 'h', 'b', 'd', 'ɡ', 'v', 'ʒ', 'ŋ', 'l', 'm', 'n', 'ɹ', 'ð']
voyelles = ['iː', 'uː', 'ɜː', 'ɔː', 'ɑː', 'aʊ', 'iə', 'eɪ', 'ʊə', 'ɔɪ', 'əʊ', 'eə', 'aɪ', 'ɪ', 'ʊ', 'ɛ', 'ɐ', 'a', 'ʌ', 'ɒ', 'ə', 'j', 'w']

mot = input('Entrez un mot en anglais : ')


# phn is a list of 190 phonemized sentences
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


print(f'Mot : {mot} ({phn}) ; contient {estimate(mot)} syllabe(s) ;')
print(f'{n_consonnes} consonne(s) : {phn_consonnes} et {n_voyelles} voyelle(s) : {phn_voyelles}')
