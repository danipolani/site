import pandas as pd
import re
import math

LETTERS_PATH = "../csv/lt/transliterations.csv"
VOC_PATH = "../csv/lt/vocabulary-source.csv"
RES_PATH_RU = "../csv/lt/vocabulary.ru.csv"
RES_PATH_EN = "../csv/lt/vocabulary.en.csv"
JSON_PATH = "../data/lt/vocabulary-pregen.json"


def _count_vowels(s):
    vowels = "aouie"
    c = 0
    for l in s:
        if l in vowels:
            c += 1
    return c


def _to_lat(s, letters):
    return letters["lat"][s]


def _word_to_lat(s, letters):
    return "".join([_to_lat(l, letters) for l in s])


def _to_ipa(s, letters):
    return letters['ipa'][s]


def _word_to_ipa(s, letters, stress=0):
    if math.isnan(stress):
        stress = 0
    stress_marker = "ˈ"
    if _count_vowels(s) < 2:
        stress_marker = ""
    res = ""
    for i, l in enumerate(s):
        if i == stress:
            res += stress_marker
        res += _to_ipa(l, letters)
    return "".join(res)


def _to_cyr(s, letters):
    return letters['cyr'][s]


def _word_to_cyr(s, letters):
    return "".join([_to_cyr(l, letters) for l in s])


def _finalize_lat(s):
    s = re.sub("mj$", "m'", s)
    s = re.sub("lj$", "l'", s)
    s = re.sub("nj$", "n'", s)
    return s


def _finalize_ipa(s):
    s = re.sub("mj", "mʲ", s)
    s = re.sub("lj", "ʎ", s)
    s = re.sub("nj", "ɲ", s)
    return s


def _finalize_cyr(s):
    s = re.sub("йа", "я", s)
    s = re.sub("мй$", "мь", s)
    s = re.sub("лй$", "ль", s)
    s = re.sub("нй$", "нь", s)
    s = re.sub("^е", "э", s)
    return s


def to_lat(s, letters):
    return _finalize_lat(_word_to_lat(s, letters))


def to_cyr(s, letters):
    return _finalize_cyr(_word_to_cyr(s, letters))


def to_ipa(s, letters, stress=0):
    return _finalize_ipa(_word_to_ipa(s, letters, stress))


if __name__ == "__main__":
    letters = pd.read_csv(LETTERS_PATH).set_index("letter").to_dict()
    voc = pd.read_csv(VOC_PATH)
    print(f"loaded {voc.shape[0]} words")

    print("starting generation")
    voc["ipa"] = voc.apply(lambda x: to_ipa(x.word, letters, x.stress), axis=1)
    voc["cyr"] = voc["word"].apply(lambda x: to_cyr(x, letters))
    voc["lat"] = voc["word"].apply(lambda x: to_lat(x, letters))
    voc["head_cyr"] = voc["cyr"].apply(lambda x: x[0])
    voc["head_lat"] = voc["lat"].apply(lambda x: x[0])
    voc = voc.sort_values(by=['cyr'])
    print("generation done")

    print(f"saving to csv: {RES_PATH_RU}")
    voc[["word", "pos", "ipa", "cyr", "head_cyr", "ru"]].sort_values(
        by=['cyr']).to_csv(RES_PATH_RU, index=False)

    print(f"saving to csv: {RES_PATH_EN}")
    voc[["word", "pos", "ipa", "lat", "head_lat", "en"]].sort_values(
        by=['lat']).to_csv(RES_PATH_EN, index=False)
    print("saving done")
