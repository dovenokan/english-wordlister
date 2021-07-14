# -*- coding: UTF-8 -*-
import string
from datasets import *
from oxfords import *
import time
import re
import shutil

def clearTensesMAIN(word):
    
    # Irregular Verbs Kısmı 
    for ir in irregularverbs:
        if ir["v3"] == word or ir["v2"] == word:
            return ir["v1"]

    for end in suffix:
        if word.endswith(end):
            ends = [word.rstrip(end) for n in [0] if word.endswith(end)]
            wstr = ends[0]

            if end == "ies" and (wstr+"y" in nouns or wstr+"y" in verbs):
                word = wstr+"y"
                return word

            elif end == "es" and (wstr in nouns or wstr in verbs):
                word = wstr
                return word

            elif end == "es" and (wstr+"e" in nouns or wstr+"e" in verbs):
                word = wstr+"e"
                return word

            elif end == "s" and (wstr in nouns or wstr in verbs):
                word = wstr
                return word

            elif end == "ied" and wstr+"y" in verbs:
                word = wstr+"y"
                return word

            elif end == "ed" and wstr in verbs:
                word = wstr
                return word

            elif end == "ed" and word[:word.index("ed")-1] in verbs:
                word = word[:word.index("ed")-1]
                return word

            elif end == "d" and wstr in verbs:
                word = wstr
                return word

            elif end == "ing" and wstr in verbs:
                word = wstr
                return word

            elif end == "ing" and wstr+"e" in verbs:
                word = wstr+"e"
                return word

            elif end == "ing" and word[:word.index("ing")-1] in verbs:
                word = word[:word.index("ing")-1]
                return word
            
            else:
                for end in ["d","s"]:
                    if word.rstrip(end) in verbs or word.rstrip(end) in nouns:
                        word = word.rstrip(end)
                        return word
                return word
    return word

def clearTenses(word):
    
    # Irregular Verbs Kısmı 
    for ir in irregularverbs:
        if ir["v3"] == word or ir["v2"] == word:
            return ir["v1"]

    for end in suffix:
        if word.endswith(end):
            wstr = word[:-len(end)]

            if end == "ies" and (wstr+"y" in nouns or wstr+"y" in verbs):
                word = wstr+"y"
                return word

            elif end == "es" and (wstr in nouns or wstr in verbs):
                word = wstr
                return word

            elif end == "es" and (wstr+"e" in nouns or wstr+"e" in verbs):
                word = wstr+"e"
                return word

            elif end == "s" and (wstr in nouns or wstr in verbs):
                word = wstr
                return word

            elif end == "ied" and wstr+"y" in verbs:
                word = wstr+"y"
                return word

            elif end == "ed" and wstr in verbs:
                word = wstr
                return word

            elif end == "ed" and word[:word.index("ed")-1] in verbs:
                word = word[:word.index("ed")-1]
                return word

            elif end == "d" and wstr in verbs:
                word = wstr
                return word

            elif end == "ing" and wstr in verbs:
                word = wstr
                return word

            elif end == "ing" and wstr+"e" in verbs:
                word = wstr+"e"
                return word

            elif end == "ing" and word[:word.index("ing")-1] in verbs:
                word = word[:word.index("ing")-1]
                return word
            
            else:
                for end in ["d","s"]:
                    if word.rstrip(end) in verbs or word.rstrip(end) in nouns:
                        word = word.rstrip(end)
                        return word
                return word
    return word

def isCapitalized(word):
    capitals = list('ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if word[0] in capitals:
        return True
    else:
        return False

def wordType(word):
    if word in verbs:
        return "verb"
    elif word in adjectives:
        return "adj"
    elif word in nouns:
        return "noun"
    elif word in phrasalverbs:
        return "phrverb"
    return "undef"

def oxford(word):
    if word in a1:
        return "a1"
    elif word in a2:
        return "a2"
    elif word in b1:
        return "b1"
    elif word in b2:
        return "b2"
    elif word in c1:
        return "c1"
    else:
        return "other"   

def regStrip(word):
    if word[0] in puncs:
        word = word.replace(word[0],"")
    n=len(word)
    for p in word:
        if p in puncs:
            n = word.index(p)
            return word[:n]
    return word[:n]

def regExpert(text):
    text = text.lower()
    text = regStrip(text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(puncs), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def sentencify(paragraph):
    abbr = ["Mr.","Mrs."] # it will be moved to datasets
    spil = paragraph.split()
    for s in spil:
        if s[-1]=="." and s not in abbr:
            spil[spil.index(s)] = s.replace(".","-.-")
    sified = ' '.join(spil)
    return sified.split("-.-")

def wordify(sentence):
    return sentence.replace("\n","").split()

def phrasalVerb(lst):
    phrpre = []
    for n in range(len(lst)):
        try:
            phrtwo = ''.join("{} {}".format(lst[n],lst[n+1]))
            phrpre.append(phrtwo)
        except:
            pass
    for p in phrpre:
        spl = p.split()
        if p in phrasalverbs:
            lst.append(p)
            try:
                del lst[lst.index(spl[0])]
                del lst[lst.index(spl[1])]
            except:
                pass
        else:
            pass

def alphabet(word):
    q = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    for letter in word:
        if letter not in q:
            return False
    return True

def wordlister(coType="-",co="-"):
    if coType == "file":
        with open('uploads/srt.txt', 'r', encoding='utf-8') as file:
            content = file.read().replace("\n", " ")
    else:
        content = co

    wo = [f for s in sentencify(content) for f in wordify(s)]
    words = [regExpert(w) for w in wo]

    dc = dict()
    for w in words:
        if w.isalpha():
            word = clearTenses(w)
            words[words.index(w)] = word

    phrasalVerb(words)
    settedwords = list({ st for st in words if not len(st) == 0 and len(st) > 2 and st.replace(" ","").isalpha() and st not in stopwords})

    for w in settedwords:
        dc[w] = [words.count(w), wordType(w), oxford(w)] 

    wordlist = sorted(dc.items(), key=lambda kv: kv[1], reverse=True)
    
    with open("uploads/generated.txt", "a", encoding="utf-8") as f:
        f.truncate(0)
        for w in wordlist:
            f.write( "{},{},{}".format(w[0],w[1][0],w[1][2]) )
            f.write("\n")
    shutil.copyfile('uploads/generated.txt', 'uploads/generated.csv')        
            
    return wordlist

