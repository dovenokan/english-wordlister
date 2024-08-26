# -*- coding: UTF-8 -*-
import time
import re
import shutil
import csv
from datetime import datetime
from datasets import *
from oxfords import *

# Initialize counters
counters = {
    'a1': 0, 'a2': 0, 'b1': 0, 'b2': 0, 'c1': 0, 'other': 0,
    'verb': 0, 'noun': 0, 'adj': 0, 'phrverb': 0, 'undef': 0
}

def clear_tenses(word):
    for ir in irregularverbs:
        if word in (ir["v2"], ir["v3"]):
            return ir["v1"]

    suffix_map = {
        "ies": lambda w: w[:-3] + 'y',
        "es": lambda w: w[:-2],
        "s": lambda w: w[:-1],
        "ied": lambda w: w[:-3] + 'y',
        "ed": lambda w: w[:-2],
        "d": lambda w: w[:-1],
        "ing": lambda w: w[:-3]
    }

    for suffix, action in suffix_map.items():
        if word.endswith(suffix):
            base_word = action(word)
            if base_word in nouns or base_word in verbs:
                return base_word
            if base_word + 'e' in nouns or base_word + 'e' in verbs:
                return base_word + 'e'

    return word

def is_capitalized(word):
    return word[0].isupper()

def word_type(word):
    if word in verbs:
        counters['verb'] += 1
        return "verb"
    elif word in adjectives:
        counters['adj'] += 1
        return "adj"
    elif word in nouns:
        counters['noun'] += 1
        return "noun"
    elif word in phrasalverbs:
        counters['phrverb'] += 1
        return "phrverb"
    else:
        counters['undef'] += 1
        return "undef"

def oxford_level(word):
    if word in a1:
        counters['a1'] += 1
        return "a1"
    elif word in a2:
        counters['a2'] += 1
        return "a2"
    elif word in b1:
        counters['b1'] += 1
        return "b1"
    elif word in b2:
        counters['b2'] += 1
        return "b2"
    elif word in c1:
        counters['c1'] += 1
        return "c1"
    else:
        counters['other'] += 1
        return "other"

def clean_word(word):
    word = word.strip(puncs)
    word = re.sub(r'\[.*?\]', '', word)
    word = re.sub(r'[%s]' % re.escape(puncs), '', word)
    word = re.sub(r'\w*\d\w*', '', word)
    return word.lower()

def sentencify(paragraph):
    abbr = ["Mr.", "Mrs."]
    sentences = paragraph.split('. ')
    return [s.replace(".", "-.-") if not any(s.startswith(a) for a in abbr) else s for s in sentences]

def wordify(sentence):
    return sentence.replace("\n", "").split()

def phrasal_verbs(words):
    phrases = []
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i + 1]}"
        if phrase in phrasalverbs:
            phrases.append(phrase)
    for phrase in phrases:
        words.remove(phrase.split()[0])
        words.remove(phrase.split()[1])
        words.append(phrase)

def wordlister(coType=None, content=None):
    start_time = time.time()  # Start the timer

    if coType == "file":
        with open('uploads/srt.txt', 'r', encoding='utf-8') as file:
            content = file.read().replace("\n", " ")

    raw_words = [clean_word(word) for sentence in sentencify(content) for word in wordify(sentence)]
    words = [clear_tenses(word) if word.isalpha() else word for word in raw_words]

    phrasal_verbs(words)
    unique_words = {word for word in words if len(word) > 2 and word.isalpha() and word not in stopwords}

    wordlist = [{
        "word": word,
        "count": words.count(word),
        "type": word_type(word),
        "oxford": oxford_level(word)
    } for word in unique_words if word_type(word) != "undef"]

    total_words = len(wordlist)
    typical_count = sum(counters[t] for t in ['verb', 'noun', 'adj', 'phrverb'])
    oxford_count = sum(counters[ox] for ox in ['a1', 'a2', 'b1', 'b2', 'c1'])
    stats = {
        "ts": datetime.timestamp(datetime.now()),
        "date": datetime.now(),
        "oxford": {level: counters[level] for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'other']},
        "type": {typ: counters[typ] for typ in ['verb', 'noun', 'adj', 'phrverb', 'undef']},
        "count": {
            "raw": len(words),
            "total": total_words,
            "typical": typical_count,
            "oxford": oxford_count,
            "oxford_A": counters['a1'] + counters['a2'],
            "oxford_B": counters['b1'] + counters['b2'],
            "oxford_C": counters['c1']
        },
        "percentage": {
            "typical": round(100 * (total_words - counters['undef']) / total_words, 2) if total_words > 0 else 0,
            "oxford": round(100 * oxford_count / max(typical_count, 1), 2),
            "oxford_A": round(100 * (counters['a1'] + counters['a2']) / max(oxford_count, 1), 2),
            "oxford_B": round(100 * (counters['b1'] + counters['b2']) / max(oxford_count, 1), 2),
            "oxford_C": round(100 * counters['c1'] / max(oxford_count, 1), 2)
        },
        "wordlist": "wordlist"
    }

    # End the timer and calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")

    # Write wordlist to a CSV file
    with open("uploads/generated.csv", "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["word", "count", "type", "oxford"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for word in wordlist:
            writer.writerow(word)

    return {"wordlist": wordlist, "stats": stats}


wordlister(coType="file")