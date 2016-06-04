from fetch_news import *
from termMatrix import *
from alchemyApi import *
from sklearn import linear_model
import numpy as np
import json

fet = fetcher()
tickers = fet.fetchTickers('microsoft')
objIds, contents, priceChanges = fet.preprocessedTermMatrix(tickers, 'microsoft')


'''
count = 0
for content in contents:
    if content == '':
        continue

    kw = json.loads(alc.keywords(content))
    words =[item['text'].lower() for item in kw['keywords']]
    content = ' '.join(words)
    count = count+1
'''


tdm = termMatrix()
tdm.createTermMatrix(contents)

factors = list()
clf = linear_model.BayesianRidge()


wordMat, dataMat = tdm.getDiffCutoff(15)

print(dataMat)

num_articles = dataMat.shape[1]
trainSplit = int(num_articles * 0.7)

trainData = dataMat[:,:trainSplit]
testData = dataMat[:,trainSplit:num_articles]

trainRes = priceChanges[:trainSplit]
testRes = priceChanges[trainSplit:num_articles]

print('number of articles: %s' %num_articles)
print('trainSplit: %d' %trainSplit)
print('trainData size: %s trainRes size: %d' %(trainData.shape, len(trainRes)))

clf.fit(trainData.T, trainRes)
predictRes = clf.predict(testData.T)

diff = (predictRes- testRes)/testRes
neg = np.where(diff<1)

print(clf.coef_)
print(len(neg[0]))

def aggregateWeight(textualWeight, votes, bounceTime):
    return textualWeight*0.5 + 0.5*(votes*bounceTime)
