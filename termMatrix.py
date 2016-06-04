import re
import textmining
from nltk.corpus import stopwords
import numpy as np

class termMatrix:
    tdm = textmining.TermDocumentMatrix()

    def removeNonAsciiFromString(self, string):
        return re.sub(r'[^\x00-\x7F]+',' ', string)

    def returnUsefulwordsIndices(self, targetList, stopwordsList):
        stopwordsIndices =  [targetList.index(item) for item in targetList if item in stopwordsList]
        return [item for item in range(len(targetList)) if item not in stopwordsIndices]

    def createTermMatrix(self, contentOnly, cutoff = 15):
        for item in contentOnly:
            cleanContent = self.removeNonAsciiFromString(item)
            self.tdm.add_doc(cleanContent)
        termMat = self.tdm.rows(cutoff)

        words = termMat.next()
        wordMat = np.array(words)
        dataMat = np.array([item for item in termMat]).T

        usefulwordsIndices = self.returnUsefulwordsIndices(words,stopwords.words('english'))

        wordMat = wordMat[usefulwordsIndices]
        dataMat = dataMat[usefulwordsIndices]

        return wordMat, dataMat

    def getDiffCutoff(self, cutoff):
        termMat = self.tdm.rows(cutoff)

        words = termMat.next()
        wordMat = np.array(words)
        dataMat = np.array([item for item in termMat]).T

        usefulwordsIndices = self.returnUsefulwordsIndices(words,stopwords.words('english'))

        wordMat = wordMat[usefulwordsIndices]
        dataMat = dataMat[usefulwordsIndices]

        return wordMat, dataMat
