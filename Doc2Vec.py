# ref: https://deepage.net/machine_learning/2017/01/08/doc2vec.html
import sys
from os import listdir, path

from gensim import models
from gensim.models.doc2vec import LabeledSentence

import MorphologyAnalyzer
import TweetExtractor
import util.Formatter

class Doc2Vec:
    def __init__(self):
        self.ma = MorphologyAnalyzer.MorphologyAnalyzer()
        self.formatter = util.Formatter.Formatter()

    def getLabaledSentence(self, words, index) -> list:
        return LabeledSentence(words=words, tags=[index])

    def getSentences(self) -> list:
        f = open('./twitterApi/texts/tweets.txt', 'r')
        texts = f.read()
        f.close()
        lines = texts.split('\n')
        sentences = []
        i = 0
        for line in lines:
            line = self.formatter.formatText(line)
            words = self.ma.extractWord(line)
            index = 'sent_{id}'.format(id=i)
            sentences.append(self.getLabaledSentence(words, index))
            i += 1
        return sentences

    def train(self):
        sentences = self.getSentences()
        print([i for i in sentences])
        '''
        modesl.Doc2Vec([LabeledSentence(words, index),LabeledSentence(words,index),...)
        '''
        model = models.Doc2Vec(sentences,
                               dm=0,
                               size=300,
                               window=15,
                               alpha=.025,
                               min_alpha=.025,
                               min_count=1,
                               sample=1e-6
                               )
        print('training start')
        for epoch in range(20):
            print('Epoch: {}'.format(epoch + 1))
            model.train(sentences, total_examples=len(sentences), epochs=30)
            model.alpha -= (0.025 - 0.0001) / 19
            model.min_alpha = model.alpha
        print('training end')
        model.save('doc2vec.model')

if __name__ == "__main__":
    te = TweetExtractor.TweetExtractor()
    d2v = Doc2Vec()
    d2v.train()
    model = models.Doc2Vec.load('./models/doc2vec.model')
    print(model.docvecs.most_similar(['sent_1']))
