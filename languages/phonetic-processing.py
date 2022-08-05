from constants import *
from pyphen import Pyphen
from phonemizer import phonemize
from syltippy import syllabize
# from unidecode import unidecode
import re
import numpy as np

dictionnaire_consonnes = {
    'fr': CONSONNES_FR,
    'it': CONSONNES_IT,
    'de': CONSONNES_DE,
    'en': CONSONNES_EN,
    'pt': CONSONNES_PT,
    'es': CONSONNES_ES
}

dictionnaire_voyelles = {
    'fr': VOYELLES_FR,
    'it': VOYELLES_IT,
    'de': VOYELLES_DE,
    'en': VOYELLES_EN,
    'pt': VOYELLES_PT,
    'es': VOYELLES_ES
}

dictionnaire_transcription = {
    'fr': 'fr-fr',
    'it': 'it',
    'de': 'de',
    'en': 'en-gb',
    'pt': 'pt',
    'es': 'es'
}

dictionnaire_syllabes_defaut = {
    'fr': 'fr',
    'de': 'de_DE',
    'en': 'en_US'
}

dictionnaire_syllabes_specifique = {
    'it': 'it_IT',
    'pt': 'pt_PT'
}

dictionnaire_phonemes_identiques = {
    'ʁ': 'r',
    'ɹ': 'r',
    'ɾ': 'r',
    'i:': 'i',
    'o:': 'o',
    'a:': 'a',
    'ɑ:': 'ɑ',
    'e:': 'e',
    'ɛː': 'ɛ',
    'ø:': 'ø',
    'u:': 'u',
    'y:': 'y',
    'ɔ:': 'ɔ'
}

dictionnaire_paires_identiques = {
    'v': 'f',
    'ʒ': 'ʃ',
    'z': 's',
    'b': 'p',
    'd': 't',
    'ɡ': 'k'
}


def remplacement_phonemes_identiques(liste_phn: list[str]) -> list[str]:
    for key in dictionnaire_phonemes_identiques.keys():
        liste_phn = [phn.replace(key, dictionnaire_phonemes_identiques[key]) for phn in liste_phn]
    return liste_phn


def remplacement_paires_identiques(liste_phn: list[str]) -> list[str]:
    for key in dictionnaire_paires_identiques.keys():
        liste_phn = [phn.replace(key, dictionnaire_paires_identiques[key]) for phn in liste_phn]
    return liste_phn


def transcription(mot: str, langue: str) -> str:
    return phonemize(
        mot,
        language=dictionnaire_transcription[langue],
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        njobs=4)


def compteur_syllabes(mot: str, langue: str) -> int:

    if langue == 'es':
        syllables, _ = syllabize(mot)
        return len(syllables)

    if langue in dictionnaire_syllabes_defaut.keys():
        lang = dictionnaire_syllabes_defaut[langue]
        left = 2
        right = 2
    elif langue in dictionnaire_syllabes_specifique.keys():
        lang = dictionnaire_syllabes_specifique[langue]
        left = 1
        right = 1

    dic = Pyphen(lang=lang, left=left, right=right)
    return len(dic.inserted(mot).split('-'))


def extraction_consonnes_voyelles(mot_transcrit: str, langue: str) -> (list[str], list[str]):
    return (extraction_phonemes(mot_transcrit, dictionnaire_consonnes[langue]), 
    extraction_phonemes(mot_transcrit, dictionnaire_voyelles[langue]))


def extraction_phonemes(mot: str, liste_phonemes: list[str]) -> list[str]:
    phn_extr = []
    mot_base = mot
    for phoneme in liste_phonemes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - \
                1 if mot.find(phoneme*2) != - 1 else compte
            phn_extr.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    phn_extr_ord = rangement_liste_phonemes(mot_base, phn_extr)
    return phn_extr_ord


def rangement_liste_phonemes(mot: str, phn_extr: list[str]) -> list[str]:
    ordre = []
    for phn in phn_extr:
        ordre.append(mot.find(phn))
        mot = mot.replace(phn, ' ', 1)
    
    phn_zip = list(zip(ordre, phn_extr))
    phn_zip.sort()

    return list(list(zip(*phn_zip))[1])


def score_son_initial(mot_transcrit_0: str, mot_transcrit_1: str, langue_0: str, langue_1: str): 
    
    liste_consonnes_voyelles_0 = dictionnaire_consonnes[langue_0] + dictionnaire_voyelles[langue_0]
    liste_consonnes_voyelles_1 = dictionnaire_consonnes[langue_1] + dictionnaire_voyelles[langue_1]

    liste_0 = extraction_phonemes(mot_transcrit_0, liste_consonnes_voyelles_0)[:2]
    liste_1 = extraction_phonemes(mot_transcrit_1, liste_consonnes_voyelles_1)[:2]

    liste_0_prep = remplacement_phonemes_identiques(remplacement_paires_identiques(liste_0))
    liste_1_prep = remplacement_phonemes_identiques(remplacement_paires_identiques(liste_1))

    liste_son_initial_0 = [dictionnaire_voyelles[langue_0].count(voyelle) for voyelle in liste_0]
    liste_son_initial_1 = [dictionnaire_voyelles[langue_1].count(voyelle) for voyelle in liste_1]

    meme_lettre = liste_0_prep[0] == liste_1_prep[0]
    meme_groupe = liste_0_prep == liste_1_prep

    groupe_consonantique = sum(liste_son_initial_0 + liste_son_initial_1) == 0
    commence_voyelle = liste_son_initial_0[0] == 1

    if groupe_consonantique:
        if meme_groupe:
            return 3
        elif meme_lettre:
            return 1
    elif meme_lettre:
        if commence_voyelle:
            return 2
        else:
            return 3
    else:
        return 0


def pourcentage_chevauchement(liste_phn_0: list[str], liste_phn_1: list[str]) -> float:
    taille_liste_phn_0 = len(liste_phn_0)
    taille_liste_phn_1 = len(liste_phn_1)

    reference = max(taille_liste_phn_0, taille_liste_phn_1)

    liste_phn_0_identiques = np.array(remplacement_phonemes_identiques(liste_phn_0))
    liste_phn_1_identiques = np.array(remplacement_phonemes_identiques(liste_phn_1))

    nb_chevauchements = np.intersect1d(liste_phn_0_identiques, liste_phn_1_identiques).size

    return nb_chevauchements / reference


def score_syllabes(nb_syllabes_mot_0: int, nb_syllabes_mot_1: int) -> int:
    difference = abs(nb_syllabes_mot_0 - nb_syllabes_mot_1)

    if difference > 1:
        return 0
    if difference == 1:
        return 1
    return 2


def score_chevauchement_consonnes(pourcentage: float) -> int:
    if pourcentage > .7:
        return 3
    if pourcentage > .5:
        return 2
    if pourcentage > 0:
        return 1
    return 0


def score_chevauchement_voyelles(pourcentage: float) -> int:
    if pourcentage >= .8:
        return 2
    elif pourcentage >= .5:
        return 1
    return 0


def main():
    # mot = input('Mot: ')
    # langue = input('Langue: ')

    # mot_transcrit = transcription(mot, langue)
    # nb_syllabes = compteur_syllabes(mot, langue)
    # liste_consonnes, liste_voyelles = extraction_consonnes_voyelles(mot_transcrit, langue)

    # print(f'Le mot {mot}({mot_transcrit}) contient {nb_syllabes} syllabes')
    # print(f'Consonnes: {liste_consonnes}')
    # print(f'Voyelles: {liste_voyelles}')

    mot_0 = 'brouette'
    langue_0 = 'fr'

    mot_1 = 'blate'
    langue_1 = 'fr'

    mot_transcrit_0 = transcription(mot_0, langue_0)
    mot_transcrit_1 = transcription(mot_1, langue_1)

    print(mot_transcrit_0, mot_transcrit_1)
    score_son_initial = son_initial_origine(mot_transcrit_0, mot_transcrit_1, langue_0, langue_1)
    print(score_son_initial)


if __name__ == '__main__':
    main()
