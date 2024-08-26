# -*- coding: UTF-8 -*-
from datasets import *
from oxfords import *
import time
import re
import shutil
from datetime import datetime

a1count = 0
a2count = 0
b1count = 0
b2count = 0
c1count = 0
othercount = 0
verbcount = 0
nouncount = 0
adjcount = 0
phrverbcount = 0
undefcount = 0

def clearTenses(word):
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
    global verbcount,nouncount,adjcount,phrverbcount,undefcount
    if word in verbs:
        verbcount+=1
        return "verb"
    elif word in adjectives:
        adjcount+=1
        return "adj"
    elif word in nouns:
        nouncount+=1
        return "noun"
    elif word in phrasalverbs:
        phrverbcount+=1
        return "phrverb"
    else:
        undefcount+=1
        return "undef"

def oxford(word):
    global a1count, a2count, b1count, b2count, c1count, othercount
    if word in a1:
        a1count+=1
        return "a1"
    elif word in a2:
        a2count+=1
        return "a2"
    elif word in b1:
        b1count+=1
        return "b1"
    elif word in b2:
        b2count+=1
        return "b2"
    elif word in c1:
        c1count+=1
        return "c1"
    else:
        othercount+=1
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
    for n in range(len(lst)-1):  # added -1 to avoid index out of range error
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

def wordlister(coType=None,content=None):
    start_time = time.time()
    if coType == "file":
        with open('uploads/srt.txt', 'r', encoding='utf-8') as file:
            content = file.read().replace("\n", " ")
    raw_words = [f for s in sentencify(content) for f in wordify(s)]
    words = [regExpert(w) for w in raw_words]
    for w in words:
        if w.isalpha():
            word = clearTenses(w)
            words[words.index(w)] = word
    phrasalVerb(words)
    settedwords = list({ st for st in words if not len(st) == 0 and len(st) > 2 and st.replace(" ","").isalpha() and st not in stopwords})
    wordlist = []

    for w in settedwords:
        wType = wordType(w)
        if wType != "undef":
            wordlist.append({
                "word":w,
                "count":words.count(w),
                "type":wType,
                "oxford":oxford(w),
            })
    stats = {
        "ts": datetime.timestamp(datetime.now()),
        "date": datetime.now(),
        "oxford": {
            "a1": a1count,
            "a2": a2count,
            "b1": b1count,
            "b2": b2count,
            "c1": c1count,
            "other": othercount,
        },
        "type": {
            "verb": verbcount,
            "noun": nouncount,
            "adj": adjcount,
            "phrverb": phrverbcount,
            "undef": undefcount,
        },
        "count": {
            "raw": len(words),
            "total": len(wordlist),
            "typical": sum([wc for wc in [verbcount, nouncount, adjcount, phrverbcount]]),
            "oxford": sum([ox for ox in [a1count, a2count, b1count, b2count, c1count]]),
            "oxford_A": sum([ox for ox in [a1count, a2count]]),
            "oxford_B": sum([ox for ox in [b1count, b2count]]),
            "oxford_C": c1count,
        },
        "percentage": {
            "typical": round((len(wordlist) - undefcount) / len(wordlist) * 100, 2) if len(wordlist) > 0 else 0,
            "oxford": round((sum([ox for ox in [a1count, a2count, b1count, b2count, c1count]])) / max(sum([wc for wc in [verbcount, nouncount, adjcount, phrverbcount]]), 1) * 100, 2),
            "oxford_A": round((sum([ox for ox in [a1count, a2count]])) / max(sum([ox for ox in [a1count, a2count, b1count, b2count, c1count]]), 1) * 100, 2),
            "oxford_B": round((sum([ox for ox in [b1count, b2count]])) / max(sum([ox for ox in [a1count, a2count, b1count, b2count, c1count]]), 1) * 100, 2),
            "oxford_C": round((c1count) / max(sum([ox for ox in [a1count, a2count, b1count, b2count, c1count]]), 1) * 100, 2),
        },
        "wordlist": "wordlist"
    }

    elapsed_time = time.time() - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")

    # ARIZA -> CSV GENERATOR
    with open("uploads/generated.txt", "a", encoding="utf-8") as f:
        f.truncate(0)
        for w in wordlist:
            f.write( "{};{};{};{}".format(w[0],w[1][0],w[1][1],w[1][2]) )
            f.write("\n")
    shutil.copyfile('uploads/generated.txt', 'uploads/generated.csv')        
    
    return {"wordlist": wordlist, "stats":stats}

wordlister(coType="file")