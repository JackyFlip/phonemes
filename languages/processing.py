from constants import *
from pyphen import Pyphen
from phonemizer import phonemize
from syltippy import syllabize
import re
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import os

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
    if not phn_extr:
        return phn_extr
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
        else:
            return 0
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

    return nb_chevauchements / reference if reference != 0 else 0


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


def multi_mots(liste_mots_0, liste_mots_1):
    return [[i, j] for i in liste_mots_0 for j in liste_mots_1 if i != j] if liste_mots_0 != liste_mots_1 else [[i, j] for i in liste_mots_0 for j in liste_mots_1]


def pipeline(liste_mots_0: list[str], liste_mots_1: list[str], langue_0, langue_1):
    liste_a_traiter = multi_mots(liste_mots_0, liste_mots_1)
    # print(liste_mots_0, liste_mots_1, liste_a_traiter, len(liste_a_traiter))
    liste_score = []

    for couple in liste_a_traiter:

        # print(f'\nTranscription {couple}')

        mot_transcrit_0 = transcription(couple[0], langue_0)
        mot_transcrit_1 = transcription(couple[1], langue_1)

        # print(mot_transcrit_0, mot_transcrit_1)

        nb_syllabes_0 = compteur_syllabes(couple[0], langue_0)
        nb_syllabes_1 = compteur_syllabes(couple[1], langue_1)

        # print(f'Contiennent {nb_syllabes_0} et {nb_syllabes_1} syllabes')

        liste_consonnes_0, liste_voyelles_0 = extraction_consonnes_voyelles(mot_transcrit_0, langue_0)
        liste_consonnes_1, liste_voyelles_1 = extraction_consonnes_voyelles(mot_transcrit_1, langue_1)

        # print(liste_consonnes_0, liste_voyelles_0)
        # print(liste_consonnes_1, liste_voyelles_1)

        son_initial = score_son_initial(mot_transcrit_0, mot_transcrit_1, langue_0, langue_1)
        syllabes = score_syllabes(nb_syllabes_0, nb_syllabes_1)

        pourcentage_consonnes = pourcentage_chevauchement(liste_consonnes_0, liste_consonnes_1)
        pourcentage_voyelles = pourcentage_chevauchement(liste_voyelles_0, liste_voyelles_1)

        consonnes = score_chevauchement_consonnes(pourcentage_consonnes)
        voyelles = score_chevauchement_voyelles(pourcentage_voyelles)

        total = son_initial + syllabes + consonnes + voyelles

        liste_score.append(total)

        # print(liste_score)

        # print('\nScore son initial', son_initial)
        # print('Score syllabes', syllabes)
        # print(f'Score consonnes {consonnes} ({pourcentage_consonnes*100}%)')
        # print(f'Score voyelles {voyelles} ({pourcentage_voyelles*100}%)')

    final = np.array(liste_score).mean()
    # print('\nScore final', final)
    return final

        
def preparation_mot(mot: str) -> list[str]:
    liste_temp = mot.split('/')
    return [element.strip() for element in liste_temp]


def charger_donnees() -> pd.DataFrame:
    DATA_DIR = Path(Path.cwd()).parent
    DATA_PATH = os.path.join(DATA_DIR, 'data/CDI-mod.xlsx')
    df = pd.read_excel(DATA_PATH)
    return df

def sauver_donnes(df: pd.DataFrame, nom: str):
    DATA_DIR = Path(Path.cwd()).parent
    DATA_PATH = os.path.join(DATA_DIR, f'data/{nom}.xlsx')
    df.to_excel(DATA_PATH, index=False)


def calcul_score(liste_mots: list['str'], langues: list['str']) -> np.array:
    score_global = np.array([])

    for couple in tqdm(liste_mots):
        score = pipeline(preparation_mot(couple[0]), preparation_mot(couple[1]), langues[0], langues[1])
        score_arrondi = int(np.floor(score + 0.5))
        score_global = np.append(score_global, score_arrondi)
    
    return score_global


def main():

    df = charger_donnees()

    df_fr_it = df[['fr', 'it']]
    langues_fr_it = df_fr_it.columns.to_numpy()
    array_fr_it = df_fr_it.to_numpy()
    score_fr_it = calcul_score(array_fr_it, langues_fr_it)
    # df['score_fr_it'] = score_fr_it
    df_fr_it['score_fr_it'] = score_fr_it
    sauver_donnes(df_fr_it, 'CDI-fr-it')


    # df_fr_de = df[['fr', 'de']]
    # langues_fr_de = df_fr_de.columns.to_numpy()
    # array_fr_de = df_fr_de.to_numpy()
    # score_fr_de = calcul_score(array_fr_de, langues_fr_de)
    # # df['score_fr_de'] = score_fr_de
    # df_fr_de['score_fr_de'] = score_fr_de
    # sauver_donnes(df_fr_de, 'CDI-fr_de')


    # df_fr_en = df[['fr', 'en']]
    # langues_fr_en = df_fr_en.columns.to_numpy()
    # array_fr_en = df_fr_en.to_numpy()
    # score_fr_en = calcul_score(array_fr_en, langues_fr_en)
    # # df['score_fr_en'] = score_fr_en
    # df_fr_en['score_fr_en'] = score_fr_en
    # sauver_donnes(df_fr_en, 'CDI-fr-en')


    # df_fr_pt = df[['fr', 'pt']]
    # langues_fr_pt = df_fr_pt.columns.to_numpy()
    # array_fr_pt = df_fr_pt.to_numpy()
    # score_fr_pt = calcul_score(array_fr_pt, langues_fr_pt)
    # # df['score_fr_pt'] = score_fr_pt
    # df_fr_pt['score_fr_pt'] = score_fr_pt
    # sauver_donnes(df_fr_pt, 'CDI-fr-pt')


    # df_fr_es = df[['fr', 'es']]
    # langues_fr_es = df_fr_es.columns.to_numpy() 
    # array_fr_es = df_fr_es.to_numpy()
    # score_fr_es = calcul_score(array_fr_es, langues_fr_es)
    # # df['score_fr_es'] = score_fr_es
    # df_fr_es['score_fr_es'] = score_fr_es
    # sauver_donnes(df_fr_es, 'CDI-fr-es')


if __name__ == '__main__':
    main()
