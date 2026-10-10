# -*- coding: UTF-8 -*-
"""Local word analysis engine.

Pipeline: tokenise -> clean -> lemmatise -> merge phrasal verbs -> classify.

All state lives inside each call, so results never leak between requests, and
every lookup goes through a set or dict instead of a linear list scan.
"""
import re
import time
from collections import Counter

from datasets import (
    adjectives,
    irregularverbs,
    nouns,
    phrasalverbs,
    puncs,
    stopwords,
    suffix,
    verbs,
)
from oxfords import a1, a2, b1, b2, c1

ABBREVIATIONS = frozenset({"Mr.", "Mrs."})
PUNCS = frozenset(puncs)
VERBS = frozenset(verbs)
NOUNS = frozenset(nouns)
STOPWORDS = frozenset(stopwords)
PHRASAL = frozenset(phrasalverbs)
SUFFIXES = tuple(suffix)

# Priority mirrors the original if/elif chains: the earlier-checked category wins,
# so later assignments below are applied in reverse priority order.
TYPE_OF = {}
for _word in phrasalverbs:
    TYPE_OF[_word] = "phrverb"
for _word in nouns:
    TYPE_OF[_word] = "noun"
for _word in adjectives:
    TYPE_OF[_word] = "adj"
for _word in verbs:
    TYPE_OF[_word] = "verb"

LEVEL_OF = {}
for _levels, _name in ((c1, "c1"), (b2, "b2"), (b1, "b1"), (a2, "a2"), (a1, "a1")):
    for _word in _levels:
        LEVEL_OF[_word] = _name

# Irregular forms map to their base verb; the first matching entry wins.
IRREGULAR = {}
for _entry in irregularverbs:
    IRREGULAR.setdefault(_entry["v2"], _entry["v1"])
    IRREGULAR.setdefault(_entry["v3"], _entry["v1"])

BRACKETS = re.compile(r"\[.*?\]")
PUNCT = re.compile("[%s]" % re.escape(puncs))
DIGIT_WORD = re.compile(r"\w*\d\w*")

LEVELS = ("a1", "a2", "b1", "b2", "c1", "other")
TYPES = ("verb", "noun", "adj", "phrverb")


def strip_edges(word):
    """Drop a leading punctuation character, then cut the word at the next one."""
    if word and word[0] in PUNCS:
        word = word.replace(word[0], "")
    for i, ch in enumerate(word):
        if ch in PUNCS:
            return word[:i]
    return word


def clean(raw):
    text = raw.lower()
    text = strip_edges(text)
    text = BRACKETS.sub("", text)
    text = PUNCT.sub("", text)
    return DIGIT_WORD.sub("", text)


def _strip_suffix(word, end):
    stem = word[:-len(end)]
    if end == "ies" and (stem + "y" in NOUNS or stem + "y" in VERBS):
        return stem + "y"
    if end == "es" and (stem in NOUNS or stem in VERBS):
        return stem
    if end == "es" and (stem + "e" in NOUNS or stem + "e" in VERBS):
        return stem + "e"
    if end == "s" and (stem in NOUNS or stem in VERBS):
        return stem
    if end == "ied" and stem + "y" in VERBS:
        return stem + "y"
    if end == "ed" and stem in VERBS:
        return stem
    if end == "ed" and word[:word.index("ed") - 1] in VERBS:
        return word[:word.index("ed") - 1]
    if end == "d" and stem in VERBS:
        return stem
    if end == "ing" and stem in VERBS:
        return stem
    if end == "ing" and stem + "e" in VERBS:
        return stem + "e"
    if end == "ing" and word[:word.index("ing") - 1] in VERBS:
        return word[:word.index("ing") - 1]
    for alt in ("d", "s"):
        if word.rstrip(alt) in VERBS or word.rstrip(alt) in NOUNS:
            return word.rstrip(alt)
    return word


def lemma(word):
    if word in IRREGULAR:
        return IRREGULAR[word]
    for end in SUFFIXES:
        if word.endswith(end):
            return _strip_suffix(word, end)
    return word


def tokenise(text):
    """Split on whitespace; a sentence-final period splits the chunk at every dot.

    Abbreviations such as "Mr." keep their period. Empty pieces are dropped.
    """
    tokens = []
    for chunk in text.split():
        if chunk.endswith(".") and chunk not in ABBREVIATIONS:
            tokens.extend(part for part in chunk.split(".") if part)
        else:
            tokens.append(chunk)
    return tokens


def normalise(raw):
    cleaned = clean(raw)
    return lemma(cleaned) if cleaned.isalpha() else cleaned


def merge_phrasal_verbs(words):
    """Count tokens and fold two-word phrasal verbs into single entries.

    Each matched phrase removes one occurrence of each of its parts, the same
    as the original list-based version, but on a Counter so it stays linear.
    """
    counts = Counter(words)
    for left, right in zip(words, words[1:]):
        phrase = f"{left} {right}"
        if phrase not in PHRASAL:
            continue
        counts[phrase] += 1
        first, second = phrase.split()[:2]
        if counts[first] > 0:
            counts[first] -= 1
            if counts[second] > 0:
                counts[second] -= 1
    return counts


def _pct(part, whole, digits=2):
    return round(part / whole * 100, digits) if whole else 0


def analyse(text):
    """Analyse plain text and return the word list plus summary statistics."""
    started = time.perf_counter()

    memo = {}
    words = []
    for raw in tokenise(text):
        value = memo.get(raw)
        if value is None:
            value = memo[raw] = normalise(raw)
        words.append(value)

    counts = merge_phrasal_verbs(words)
    raw_total = sum(counts.values())

    wordlist = []
    undefined = 0
    level_counts = Counter({level: 0 for level in LEVELS})
    type_counts = Counter({kind: 0 for kind in TYPES})

    for word, count in counts.items():
        if count <= 0 or len(word) <= 2 or word in STOPWORDS:
            continue
        if not word.replace(" ", "").isalpha():
            continue
        kind = TYPE_OF.get(word)
        if kind is None:
            undefined += 1
            continue
        level = LEVEL_OF.get(word, "other")
        type_counts[kind] += 1
        level_counts[level] += 1
        wordlist.append({"word": word, "count": count, "type": kind, "oxford": level})

    wordlist.sort(key=lambda entry: (-entry["count"], entry["word"]))

    defined = len(wordlist)
    leveled = defined - level_counts["other"]
    level_a = level_counts["a1"] + level_counts["a2"]
    level_b = level_counts["b1"] + level_counts["b2"]
    level_c = level_counts["c1"]

    stats = {
        "oxford": dict(level_counts),
        "type": {**dict(type_counts), "undef": undefined},
        "count": {
            "raw": raw_total,
            "total": defined,
            "typical": defined,
            "oxford": leveled,
            "oxford_A": level_a,
            "oxford_B": level_b,
            "oxford_C": level_c,
        },
        "percentage": {
            "typical": _pct(defined, defined + undefined),
            "oxford": _pct(leveled, defined),
            "oxford_A": _pct(level_a, leveled),
            "oxford_B": _pct(level_b, leveled),
            "oxford_C": _pct(level_c, leveled),
        },
    }

    return {
        "wordlist": wordlist,
        "stats": stats,
        "elapsed": time.perf_counter() - started,
    }
