import pandas as pd
import re
import math

LETTERS_PATH = "../csv/lt/transliterations.csv"
VOC_PATH = "../csv/lt/vocabulary.csv"
RES_PATH = "../csv/lt/vocabulary-pregen.csv"
JSON_PATH = "../data/lt/vocabulary-pregen.json"


def _to_ipa(s, letters):
    return letters['ipa'][s]


def _count_vowels(s):
    vowels = "aouie"
    c = 0
    for l in s:
        if l in vowels:
            c += 1
    return c


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
    voc["head"] = voc["cyr"].apply(lambda x: x[0])
    voc = voc.sort_values(by=['cyr'])
    print("generation done")

    print(f"saving to csv: {RES_PATH}")
    voc.to_csv(RES_PATH, index=False)
    print("saving done")

    # print(f"saving to json: {JSON_PATH}")
    # voc.to_json(JSON_PATH, orient="records", force_ascii=False, indent=2)
    # print("saving done")
