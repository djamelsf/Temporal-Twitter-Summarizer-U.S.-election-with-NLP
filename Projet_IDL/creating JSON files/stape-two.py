import json
import nltk
from wordcloud import WordCloud, STOPWORDS 

#fonction qui regroupe les mots et leurs frequences et enleve la redondance.
def getFrequencies(list_):
    frequencies = {}
    for item in list_:
        if item in frequencies:
            frequencies[item] += 1
        else:
            frequencies[item] = 1
    return frequencies



j1={}

#verifier encore une fois les stopwords
stopwords = set(STOPWORDS).union({"lol",":p","@","https","https://t.co/ytldsaonjx"})

#je parcoure le fichier json crée dans l'etape 1 et j'essaye de regrouper les mots par leurs fréquence.
with open("/Users/mac/Desktop/json-1.json") as json_file:
    for line in json_file:
        j1 = json.loads(line)
json_file.close()
g={}
g['2020-07-27']=getFrequencies([word for word in j1['2020-07-27'] if word.lower() not in stopwords])
g['2020-07-28']=getFrequencies([word for word in j1['2020-07-28'] if word.lower() not in stopwords])
j2={}
with open("/Users/mac/Desktop/json-2.json") as json_file2:
    for line in json_file2:
        j2 = json.loads(line)
json_file2.close()
j1['2020-07-29'].extend(j2['2020-07-29'])
g['2020-07-29']=getFrequencies([word for word in j1['2020-07-29'] if word.lower() not in stopwords])



#j'ai fait cette operation 20 fois avec les 20 fichiers crée dans l'etape 1
#maintement je stocke le dictionnaire g dans deux fichiers json-final1-10.json et json-final11-20.json