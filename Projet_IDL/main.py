from flask import Flask, render_template, redirect, url_for, request, Response
from collections import OrderedDict
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import json
import requests
from PIL import Image
import  numpy as np
import matplotlib
import os
import time
matplotlib.use('Agg')

#une fonction que permet recuprer le fichier exacte d'une date
def getFileOfDay(date,files):
        switcher={
                '2020-07-27':files[0]['2020-07-27'],
                '2020-07-28':files[0]['2020-07-28'],
                '2020-07-29':files[0]['2020-07-29'],
                '2020-07-30':files[0]['2020-07-30'],
                '2020-07-31':files[0]['2020-07-31'],
                '2020-08-01':files[0]['2020-08-01'],
                '2020-08-02':files[0]['2020-08-02'],
                '2020-08-03':files[0]['2020-08-03'],
                '2020-08-04':files[0]['2020-08-04'],
                '2020-08-05':files[0]['2020-08-05'],
                '2020-08-07':files[0]['2020-08-07'],
                '2020-08-08':files[0]['2020-08-08'],
                '2020-08-09':files[0]['2020-08-09'],
                '2020-08-10':files[0]['2020-08-10'],
                '2020-08-11':files[0]['2020-08-11'],
                '2020-08-12':files[1]['2020-08-12'],
                '2020-08-13':files[1]['2020-08-13'],
                '2020-08-26':files[1]['2020-08-26'],
                '2020-08-27':files[1]['2020-08-27'],
                '2020-08-28':files[1]['2020-08-28'],
                '2020-08-29':files[1]['2020-08-29'],
                '2020-08-31':files[1]['2020-08-31'],
                '2020-09-01':files[1]['2020-09-01'],
                '2020-09-02':files[1]['2020-09-02'],
                '2020-09-03':files[1]['2020-09-03'],
                '2020-09-04':files[1]['2020-09-04'],
                '2020-09-05':files[1]['2020-09-05'],
                '2020-09-14':files[1]['2020-09-14'],
                '2020-09-15':files[1]['2020-09-15'],
                '2020-09-21':files[1]['2020-09-21'],
                '2020-09-22':files[1]['2020-09-22'],
                '2020-09-24':files[1]['2020-09-24'],
                '2020-09-29':files[1]['2020-09-29'],
                '2020-10-01':files[1]['2020-10-01'],
                '2020-10-02':files[1]['2020-10-02'],
                
             }
        return switcher.get(date,None)


#une fonction qui permet de recuprer la frequence d'un mot sur chaque date, 0 si il n'existe pas 
def getArrayOfFrequencyPerDay(files,word):
    dates=['2020-07-27','2020-07-28','2020-07-29','2020-07-30','2020-07-31','2020-08-01','2020-08-02','2020-08-03'
          ,'2020-08-04','2020-08-05','2020-08-07','2020-08-08','2020-08-09','2020-08-10','2020-08-11','2020-08-12'
          ,'2020-08-13','2020-08-26','2020-08-27','2020-08-28','2020-08-29','2020-08-31','2020-09-01'
          ,'2020-09-02','2020-09-03','2020-09-04','2020-09-05','2020-09-14','2020-09-15','2020-09-21','2020-09-22'
          ,'2020-09-24','2020-09-29','2020-10-01','2020-10-02']
    dict_word={}
    for i in dates:
        dict_word[i]=getFileOfDay(i,files).get(word,0)
    
    return dict_word
        



#une fonction qui permet d'afficher le WorldCloud d'une date 
def getImageLink(date,files):
    plt.close()
    pic = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png',stream=True).raw))
    od = OrderedDict(sorted(getFileOfDay(date,files).items(), key=lambda x:x[1], reverse=True))
    comment_words = ''
    comment_words += " ".join(list(od.keys()))+" "
    print(list(od.keys())[0:100])
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white', stopwords = ['RT','&amp'], mask = pic, min_font_size = 10).generate_from_frequencies(od)
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig('static/'+timestr)
    plt.close()
    return timestr+'.png'

#une fonction qui permet d'afficher les stat d'un mot par rapport a chaque date
def getImageLinkWord(word,files):
    plt.close()
    array=getArrayOfFrequencyPerDay(files,word)
    dates=list(array.keys())
    values=list(array.values())
    ypos=np.arange(len(dates))
    plt.xticks(rotation='vertical')
    plt.xticks(ypos,dates)
    plt.ylabel('Frequency')
    plt.title('the frequency of the word "'+word+'" per day')
    plt.xlabel('Day-Mouth in 2020')
    plt.bar(ypos,values,label=word)
    plt.legend()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig('static/'+timestr)
    plt.close()
    return timestr+'.png'

#une fonction qui permet de comparer deux mots chaque date
def getImageComparison(word1,word2,files):
    plt.close()
    array1=getArrayOfFrequencyPerDay(files,word1)
    dates1=list(array1.keys())
    values1=list(array1.values())
    array2=getArrayOfFrequencyPerDay(files,word2)
    dates2=list(array2.keys())
    values2=list(array2.values())
    ypos=np.arange(len(dates1))
    plt.xticks(rotation='vertical')
    plt.xticks(ypos,dates1)
    plt.ylabel('Frequency')
    plt.xlabel('Day-Mouth in 2020')
    plt.bar(ypos-0.2,values1,width=0.4,label=word1)
    plt.bar(ypos+0.2,values2,width=0.4,label=word2)
    plt.legend()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig('static/'+timestr)
    plt.close()
    return timestr+'.png'
    
    







app = Flask(__name__)

#page accueil
@app.route("/")
def home():
	return render_template("home.html")

#WordCloud d'une date
@app.route("/summ",methods=["POST","GET"])
def summ():
	if request.method == "POST":
		date=request.form["dateT"]
		return render_template("index.html", content=getImageLink(date,files),d=date)
	else:
		return render_template("summ.html")
    
#statistiques d'un mot
@app.route("/word",methods=["POST","GET"])
def word():
    if request.method == "POST":
        word=request.form['wordT']
        return render_template("ViewStat.html", content=getImageLinkWord(word,files))
    else:
        return render_template("word.html")

#comparaison entre deux mots.
@app.route("/compare",methods=["POST","GET"])
def compare():
    if request.method == "POST":
        word1=request.form['word1']
        word2=request.form['word2']
        return render_template("ViewComp.html", content=getImageComparison(word1,word2,files))
    else:
        return render_template("compare.html")



#lecture des deux fichiers JSON
if __name__ == "__main__":
    with open("json-final1-10.json") as json_file:
        for line in json_file:
            f1 = json.loads(line)

    with open("json-final11-20.json") as json_file:
        for line in json_file:
            f2 = json.loads(line)
    files=[f1,f2]
    app.run(debug=True)






