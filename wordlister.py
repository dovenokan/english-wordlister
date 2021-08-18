# -*- coding: UTF-8 -*-
import string
from datasets import *
from oxfords import *
import time
import re
import shutil

a1countq = []
a2countq = []
b1countq = []
b2countq = []
c1countq = []
undefcountq = []

verbcountq = []
adjcountq = []
nouncountq = []
phrverbcountq = []
othercountq = []

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
        verbcountq.append(word)
        return "verb"
    elif word in adjectives:
        adjcountq.append(word)
        return "adj"
    elif word in nouns:
        nouncountq.append(word)
        return "noun"
    elif word in phrasalverbs:
        phrverbcountq.append(word)
        return "phrverb"
    else:
        undefcountq.append(word)
        return "undef"

def oxford(word):
    if word in a1:
        a1countq.append(word)
        return "a1"
    elif word in a2:
        a2countq.append(word)
        return "a2"
    elif word in b1:
        b1countq.append(word)
        return "b1"
    elif word in b2:
        b2countq.append(word)
        return "b2"
    elif word in c1:
        c1countq.append(word)
        return "c1"
    else:
        othercountq.append(word)
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
    settedwords = list({ st for st in words if not len(st) == 0 and len(st) > 2 and st.replace(" ","").isalpha() and st not in stopwords and st not in whatiknow})

    for w in settedwords:
        dc[w] = [words.count(w), wordType(w), oxford(w)] 

    wordlist = sorted(dc.items(), key=lambda kv: kv[0], reverse=False) # 0 False letter 1 True count


    a1count = list(set(a1countq))
    a2count = list(set(a2countq))
    b1count = list(set(b1countq))
    b2count = list(set(b2countq))
    c1count = list(set(c1countq))
    undefcount = list(set(undefcountq))

    verbcount = list(set(verbcountq))
    adjcount = list(set(adjcountq))
    nouncount = list(set(nouncountq))
    phrverbcount = list(set(phrverbcountq))
    othercount = list(set(othercountq))

    stats = {
        "a1":len(a1count),
        "a2":len(a2count),
        "b1":len(b1count),
        "b2":len(b2count),
        "c1":len(c1count),
        "other":len(othercount),
        "verb":len(verbcount),
        "noun":len(nouncount),
        "adj":len(adjcount),
        "phrverb":len(phrverbcount),
        "undef":len(undefcount),
        "total":len(wordlist),
        "typical":len(wordlist)-len(undefcount),
        "oxford":len(a1count)+len(a2count)+len(b1count)+len(b2count)+len(c1count),
        "oxA":len(a1count)+len(a2count),
        "oxB":len(b1count)+len(b2count),
        "oxC":len(c1count),
        "percentage": {
            "Typical%": round((len(wordlist)-len(undefcount)) / len(wordlist) * 100,2),
            "oxford%": round((len(a1count)+len(a2count)+len(b1count)+len(b2count)+len(c1count)) / (len(wordlist)-len(undefcount)) * 100,2),
            "oxA%": round((len(a1count)+len(a2count)) / (len(a1count)+len(a2count)+len(b1count)+len(b2count)+len(c1count)) * 100,2),
            "oxB%": round((len(b1count)+len(b2count)) / (len(a1count)+len(a2count)+len(b1count)+len(b2count)+len(c1count)) * 100,2),
            "oxC%": round((len(c1count)) / (len(a1count)+len(a2count)+len(b1count)+len(b2count)+len(c1count)) * 100,2)
        }
    }
    
    with open("uploads/generated.txt", "a", encoding="utf-8") as f:
        f.truncate(0)
        for w in wordlist:
            f.write( "{};{};{}".format(w[0],w[1][0],w[1][2]) )
            f.write("\n")
    shutil.copyfile('uploads/generated.txt', 'uploads/generated.csv')        
            
    return wordlist , stats

