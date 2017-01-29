import numpy as np
import csv
from watson_developer_cloud import AlchemyLanguageV1
import numpy as np
import json

API_KEY = '8ec5577c2b7c730ac56243dc6c717dee9e93f372'
bqFile = 'results500.csv'

#filters posts with a link but no text: data will be more consistent, 
# no error from sentiment analysis of post text and link text
# also filters down to only to techcrunch articles 
# to control for type of content (blog articles)

def filterPosts(file):
	arr = []
	with open (file,'rb') as results:
	    resultsReader = csv.reader(results)
	    for row in resultsReader:
	        arr.append(row)
	titles = arr[0]
	articles = arr
	articles = arr[1:]
	filteredArticles = [article for article in articles if article[2] == '' and articles[4] != '']
	# 'techcrunch' in article[4]
	return filteredArticles

def query(articles): 
	emotionArr  = []
	for article in articles[:100]: 
	    alchemy_language = AlchemyLanguageV1(api_key=API_KEY)
	    theUrl = article[4]
	    print 'ye'
	    if theUrl:
	        try:
	            emotion = json.dumps(alchemy_language.emotion(url=theUrl),indent=2)
	            emotionArr.append(json.loads(emotion))
	        except : 
	            emotionArr.append(None)
	return emotionArr

def save(emotionArr):
	anger,disgust,fear,joy,sadness,score, comments = [],[],[],[],[],[],[]
	for i in range(len(emotionArr)):
	    entry = []
	    if emotionArr[i]:
	            angerEntry = emotionArr[i]['docEmotions']['anger']
	            disgustEntry = emotionArr[i]['docEmotions']['disgust']
	            fearEntry = emotionArr[i]['docEmotions']['fear']
	            joyEntry = emotionArr[i]['docEmotions']['joy']
	            sadnessEntry = emotionArr[i]['docEmotions']['sadness']
	            
	            anger.append(float(angerEntry))
	            disgust.append(float(disgustEntry))
	            fear.append(float(fearEntry))
	            joy.append(float(joyEntry))
	            sadness.append(float(sadnessEntry))
	            
	            score.append(int(articles[i][1]))
	            comments.append(int(articles[i][3]))

	np.savetxt('anger.txt', anger, delimiter=',')   
	np.savetxt('disgust.txt', disgust, delimiter=',')   
	np.savetxt('fear.txt', fear, delimiter=',')   
	np.savetxt('joy.txt', joy, delimiter=',')   
	np.savetxt('sadness.txt', sadness, delimiter=',')  
	np.savetxt('score.txt', score, delimiter=',') 
	np.savetxt('comments.txt', comments, delimiter=',')  
	
'''	anger = np.array(anger)
	disgust = np.array(disgust)
	fear = np.array(fear)
	joy = np.array(joy)
	sadness = np.array(sadness)
	comments = np.array(comments)
	score = np.array(score)
'''

articles = filterPosts(bqFile)
emotionArr = query(articles)
save(emotionArr)





