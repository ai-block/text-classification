import json
import config
from requests_oauthlib import OAuth1Session
import re


class TweetExtractor:

    def __init__(self):
        f = open('./config/config.json','r')
        self.config = json.load(f)
        self.CK = self.config['CONSUMER_KEY']
        self.CS = self.config['CONSUMER_SECRET']
        self.AT = self.config['ACCESS_TOKEN']
        self.ATS = self.config['ACCESS_TOKEN_SECRET']
        self.session = OAuth1Session(self.CK, self.CS, self.AT, self.ATS)

    texts = {}

    def extract(self):
        response = self.session.get(self.config.URL, params = self.config.PARAMS)
        f_out = open('./texts/tweets.txt','w')
        for j in range(10):
            response = self.session.get(self.config.URL, params = self.config.PARAMS)
            if response.status_code == 200:
                limit = response.headers['x-rate-limit-remaining']
                print (" the number of requests left for the 15 minute window: " + limit)
                if limit == 1:
                    sleep(60*15)
                n = 0
                timeline = json.loads(response.text)
                for i in range(len(timeline)):
                    self.texts[j] = timeline[i]['text']
                    if i != len(timeline)-1:
                        f_out.write(timeline[i]['text'] + '\n')
                    else:
                        f_out.write(timeline[i]['text'] + '\n')
                        self.config.PARAMS['max_id'] = timeline[i]['id']-1
        f_out.close()

    def getTextsTdDic(self):
        te = TweetExtractor()
        te.extract()
        return self.texts

    # def extractText(self):
    #     response = self.session.get(config.URL, params = config.PARAMS)
    #     texts = {}
    #     for i in range(10):
    #         response = self.session.get(config.URL, params = config.PARAMS)
    #         if response.status_code == 200:
    #             limit = response.headers['x-rate-limit-remaining']
    #             print (" the number of requests left for the 15 minute window: " + limit)
    #             if limit == 1:
    #                 sleep(60*15)
    #             n = 0
    #             timeline = json.loads(response.text)
    #             for j in range(len(timeline)):
    #                 texts[i] = timeline[0]['text']
    #     return texts
    #
    # def writeToTxt(self,texts):
    #     with open('./texts/tweets.txt','w') as f:
    #         for text in texts.values():
    #             f.write(text + '\n')
    #         f.close()

if __name__ == "__main__":
    te = TweetExtractor()
    te.extract()
    print({k:v for k,v in te.texts.items()})
