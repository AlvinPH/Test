
# coding: utf-8

# In[105]:


def ngram_probs(filename='raw_sentences.txt'):
    file = open(filename,"r")
    raw = file.read()
    target = raw.lower().replace("\n", " ")
    from collections import Counter
    split_result = [x for x in target.split(" ") if len(x)>0]
    
    # Bigram
    bigrams = [b for b in zip(split_result[:-1], split_result[1:])]
    cnt = Counter(bigrams)
    keys = list(cnt.keys())
    value = list(cnt.values())
    bigram_probs = {}
    for idx in range(len(keys)):
        bigram_probs[keys[idx]] = value[idx]/sum(value)
    # Trigram
    trigrams = [b for b in zip(split_result[:-2], split_result[1:-1], split_result[2:])]
    cnt = Counter(trigrams)
    keys = list(cnt.keys())
    value = list(cnt.values())
    trigram_probs = {}
    for idx in range(len(keys)):
        trigram_probs[keys[idx]] = value[idx]/sum(value)
        
    return bigram_probs, trigram_probs


# In[ ]:


cnt2, cnt3 = ngram_probs()

print(cnt2[('we', 'are')])


# In[ ]:


def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    from math import log
    trigrams = list(cnt3.keys())
    prob = {}
    for trigram in trigrams:
        if trigram[:2] == bigram:
            prob[trigram[2]] = log(cnt3[trigram])+log(cnt2[bigram])
    return prob


# In[ ]:


p = prob3(('we', 'are'))
print(p['family'])


# In[ ]:


def predict_max(starting, cnt2=cnt2, cnt3=cnt3):
    list_of_words = list(starting)
    while len(list_of_words) <= 15:
        p = prob3(starting)
        max_prob = max(p.values())
        for i in p.keys():
            if p[i] == max_prob:
                max_key = i
                break
        starting = (starting[1],max_key)
        list_of_words.append(max_key)
        if max_key == '.':
            break
    return list_of_words


# In[ ]:


sent = predict_max(('we', 'are'))
assert sent[-1] == '.' or len(sent) <= 15
print(' '.join(sent))

