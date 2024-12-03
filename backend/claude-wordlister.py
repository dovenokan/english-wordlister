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

# Pre-compile regex patterns for better performance
BRACKETS_PATTERN = re.compile(r'\[.*?\]')
PUNCS_PATTERN = re.compile(r'[%s]' % re.escape(puncs))
DIGITS_PATTERN = re.compile(r'\w*\d\w*')

# Convert lists to sets for O(1) lookup
verbs_set = set(verbs)
adjectives_set = set(adjectives)
nouns_set = set(nouns)
phrasalverbs_set = set(phrasalverbs)
stopwords_set = set(stopwords)
a1_set = set(a1)
a2_set = set(a2)
b1_set = set(b1)
b2_set = set(b2)
c1_set = set(c1)

def clear_tenses(word):
    # First check irregular verbs using set operations
    for ir in irregularverbs:
        if word in {ir["v2"], ir["v3"]}:
            return ir["v1"]

    suffix_map = {
        "ies": (3, 'y'),
        "es": (2, ''),
        "s": (1, ''),
        "ied": (3, 'y'),
        "ed": (2, ''),
        "d": (1, ''),
        "ing": (3, '')
    }

    for suffix, (cut, add) in suffix_map.items():
        if word.endswith(suffix):
            base_word = word[:-cut] + add
            if base_word in verbs_set or base_word in nouns_set:
                return base_word
            base_word_e = base_word + 'e'
            if base_word_e in verbs_set or base_word_e in nouns_set:
                return base_word_e
    
    return word

def word_type(word):
    if word in verbs_set:
        counters['verb'] += 1
        return "verb"
    elif word in adjectives_set:
        counters['adj'] += 1
        return "adj"
    elif word in nouns_set:
        counters['noun'] += 1
        return "noun"
    elif word in phrasalverbs_set:
        counters['phrverb'] += 1
        return "phrverb"
    else:
        counters['undef'] += 1
        return "undef"

def oxford_level(word):
    if word in a1_set:
        counters['a1'] += 1
        return "a1"
    elif word in a2_set:
        counters['a2'] += 1
        return "a2"
    elif word in b1_set:
        counters['b1'] += 1
        return "b1"
    elif word in b2_set:
        counters['b2'] += 1
        return "b2"
    elif word in c1_set:
        counters['c1'] += 1
        return "c1"
    else:
        counters['other'] += 1
        return "other"

def clean_word(word):
    word = word.strip(puncs)
    word = BRACKETS_PATTERN.sub('', word)
    word = PUNCS_PATTERN.sub('', word)
    word = DIGITS_PATTERN.sub('', word)
    return word.lower()

def sentencify(paragraph):
    abbr = ["Mr.", "Mrs."]
    sentences = paragraph.split('. ')
    return [s.replace(".", "-.-") if not any(s.startswith(a) for a in abbr) else s for s in sentences]

def wordify(sentence):
    return sentence.replace("\n", "").split()

def phrasal_verbs(words):
    i = 0
    while i < len(words) - 1:
        phrase = f"{words[i]} {words[i + 1]}"
        if phrase in phrasalverbs_set:
            words.pop(i)  # Remove first word
            words.pop(i)  # Remove second word (now at index i)
            words.insert(i, phrase)
        else:
            i += 1

def wordlister(coType=None, content=None):
    start_time = time.time()

    if coType == "file":
        with open('uploads/srt.txt', 'r', encoding='utf-8') as file:
            content = file.read().replace("\n", " ")

    # Process sentences and words more efficiently
    sentences = sentencify(content)
    words = [word for sentence in sentences for word in wordify(sentence)]
    
    # Clean and process words in a single pass
    processed_words = []
    word_counts = {}
    
    for word in words:
        clean = clean_word(word)
        if clean:  # Skip empty strings
            processed = clear_tenses(clean) if clean.isalpha() else clean
            if processed:
                processed_words.append(processed)
                word_counts[processed] = word_counts.get(processed, 0) + 1

    phrasal_verbs(processed_words)
    
    # Use set comprehension for unique words
    unique_words = {word for word in processed_words 
                   if len(word) > 2 and word.isalpha() and word not in stopwords_set}

    # Create wordlist more efficiently
    wordlist = []
    for word in unique_words:
        word_t = word_type(word)
        if word_t != "undef":
            wordlist.append({
                "word": word,
                "count": word_counts.get(word, 0),
                "type": word_t,
                "oxford": oxford_level(word)
            })
    
    wordlist.sort(key=lambda x: x['count'], reverse=True)

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

    with open("uploads/stats.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        
        # Flatten and write oxford and type dictionaries
        for key, value in stats['oxford'].items():
            writer.writerow([f"oxford_{key}", value])
        for key, value in stats['type'].items():
            writer.writerow([f"type_{key}", value])

        # Write counts
        for key, value in stats['count'].items():
            writer.writerow([f"count_{key}", value])

        # Write percentages
        for key, value in stats['percentage'].items():
            writer.writerow([f"percentage_{key}", value])

    # Write wordlist to a CSV file
    with open("uploads/generated.csv", "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["word", "count", "type", "oxford"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for word in wordlist:
            writer.writerow(word)

    return {"wordlist": wordlist, "stats": stats}

wordlister(coType="file")