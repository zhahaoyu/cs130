'''
fetch all news article with a given name

from pymongo import MongoClient

class fetcher:
    def __init__(self):
        self.client = MongoClient('ds015953.mlab.com', 15953)
        self.db = self.client['stock_advisor']
        self.db.authenticate('simon','123')

    def fetchTickers(self, companyName):
        collection = self.db['ticker']
        prices = collection.find({'company':companyName})
        return prices

    def preprocessedTermMatrix(self, prices, companyName):
        collection = self.db['news']
        objIds = list()
        contents = list()
        priceChanges = list()

        for item in prices:
            time = item['date']
            articles = collection.find({'query': companyName, 'time': time})
            for article in articles:
                objId = article['_id']
                content = article['content']
                priceChange = (item['close'] - item['open'])/item['open']

                objIds.append(objId)
                contents.append(content)
                priceChanges.append(priceChange)

        return objIds, contents, priceChanges
