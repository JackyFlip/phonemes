from constants import *

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
    'it': 'it_IT',
    'de': 'de_DE',
    'en': 'en_US',
    'pt': 'pt_PT',
}

dictionnaire_syllabes_specifique = {
    'fr': 'fr',
    'it': 'it_IT',
    'de': 'de_DE',
    'en': 'en_US',
    'pt': 'pt_PT',
}


def transcription(mot: str, langue: str) -> str:
    return phonemize(
        mot,
        language=dictionnaire_transcription[langue],
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        njobs=4)


def compteur_syllabes_defaut(mot: str, langue):
    dic = Pyphen(lang='fr')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


def compteur_syllabes_specifique(mot: str, langue):
    dic = Pyphen(lang='fr')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


def compteur_syllabes_espagnol(mot: str, langue):
    dic = Pyphen(lang='fr')
    mot_split = dic.inserted(mot)
    nb_syllabes = len(mot_split.split('-'))
    return mot_split, nb_syllabes


def extraction_phonemes(mot: str, liste_phonemes: list[str]) -> list[str]:
    phn_extr = []
    for phoneme in liste_phonemes:
        if phoneme in mot:
            compte = mot.count(phoneme)
            compte_correction = compte - \
                1 if mot.find(phoneme*2) != - 1 else compte
            phn_extr.extend([phoneme] * compte_correction)
            mot = re.sub(phoneme, '', mot)
    return phn_extr


def main():
    pass


if __name__ == '__main__':
    main()
