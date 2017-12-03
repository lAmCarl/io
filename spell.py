import re
import redis
from itertools import izip_longest
from collections import Counter


ignored_words = set([
    'the', 'of', 'at', 'on', 'in', 'is', 'it', 'and', 'or',
])

def words(text): return re.findall(r'\w+', text.lower())


r_server = redis.Redis(host="localhost", port=6379)
WORDS = {}
# iterate a list in batches of size n
def batcher(iterable, n):
    args = [iter(iterable)] * n
    return izip_longest(*args)

# in batches of 500 delete keys matching user:*
for keybatch in batcher(r_server.scan_iter('word:*:word_count'),500):
    for k in keybatch:
        if k:
            w = str(k).split(':')[1]
            count = int(r_server.get(k))
            WORDS[w] = count

for w in ignored_words:
    WORDS[w] = 1

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    cands = candidates(word)
    if cands:
        return max(candidates(word), key=P)
    else:
        return None

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)))

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
