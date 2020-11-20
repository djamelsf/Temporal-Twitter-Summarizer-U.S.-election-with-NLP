from wordcloud import WordCloud, STOPWORDS 
from nltk.stem import WordNetLemmatizer
import fileinput
import json
import spacy

import nltk
from nltk.corpus import wordnet


#fonction qui permet de recuperer wordnet_pos
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)



#creation d'un Dictionnaire qui va enregister les deux dates avec leurs mots
dict_g={}
dict_g['2020-07-29']=[]
dict_g['2020-07-30']=[]


lemmatizer = WordNetLemmatizer()
list_lemma=[]
with open("/Users/mac/Desktop/us_election_splitte/2.json") as json_file:
    for line in json_file:
        tweet_dict = json.loads(line)
        #recuprer seulement la date
        date=tweet_dict['created_at'][0:10]
        list_w=tweet_dict['text'].split()
        for j in list_w:
            list_lemma.append(lemmatizer.lemmatize(j, get_wordnet_pos(j)))
        stopwords = set(STOPWORDS)
        set2={'rt',':','$'}
        set3 = stopwords.union(set2)
        filtered_words = [word for word in list_lemma if word not in set3]
        dict_g[date].extend(filtered_words)
        list_lemma.clear()
        

            
with open('/Users/mac/Desktop/json-2.json', 'w') as outfile:
    json.dump(dict_g, outfile)

#j'ai fait cette operation 20 fois avec les 20 fichiers json.

