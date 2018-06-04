# coding:utf-8
import re
import csv
import time
import pandas as pd
import MeCab
import random
import codecs
from statistics import mean

class MorphologyAnalyzer:
    '''
    形態素解析器
    '''
    def __init__(self):
        self.mecab = MeCab.Tagger(" -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd")
        self.pnDf = None

        # 極性辞書読み込み
        with codecs.open("src/dictionaries/PN_Table/pn_ja.dic.txt", "r", "shift-jis", "ignore") as file:
            pnDf = pd.read_csv(file,
                            sep=':',
                            encoding='utf-8',
                            names=('Word','Reading','POS', 'PN')
                           )

        # pandasのdataframeから辞書型への変換
        self.pnDfDictsList = pnDf.to_dict('records')

    # 形態素解析
    def performMorphologicalAnalysis(self,text):
        """
        :param text: string
        :return result: list
        """
        result = []
        result = self.mecab.parse(text).splitlines()[:-1]
        return result

    # 構文解析
    def performSyntacticAnalysis(self,text):
        """
        :param text: string
        :return result:
        """
        pass


    # 形態素解析で分解された単語をリストにして返す
    def extractWord(self,text):
        """
        :param text: string
        :return words: list
        """
        words = []
        result = self.performMorphologicalAnalysis(text)
        for chunk in result:
            (word, feature) = chunk.split('\t')
            words.append(word)
        return words

    # 形態素解析で分解された単語と品詞（Part of Speech、 POS）のタプルをリストにして返す
    def extractWordAndPartOfSpeechDictsList(self,text):
        """
        :param text: string
        :return wordAndPartOfSpeechList: list
        """
        wordAndPartOfSpeechList = []
        for chunk in mecab.parse(text).splitlines()[:-1]:
            wordAndPartOfSpeechDict = {}
            (word, feature) = chunk.split('\t')
            wordAndPartOfSpeechDict["Word"] = word
            wordAndPartOfSpeechDict["POS"] = feature.split(",")[0]
            wordAndPartOfSpeechList.append(wordAndPartOfSpeechDict)
        return wordAndPartOfSpeechList

    # 名詞をリストにし返す
    def extractNoun(self,text):
        """
        Utility function.

        :param text: string
        :return nouns: list
        """
        nouns = []
        for chunk in mecab.parse(text).splitlines()[:-1]:
            (word, feature) = chunk.split('\t')
            if feature.startswith('名詞'):
                 nouns.append(word)
        return nouns

    # 形容詞をリストにし返す
    def extractAdjective(self,text):
        """
        Utility function.

        :param text: string
        :return adjectivs: list
        """
        adjectives = []
        for chunk in mecab.parse(text).splitlines()[:-1]:
            (word, feature) = chunk.split('\t')
            if feature.startswith('形容詞'):
                 adjectives.append(word)
        return adjectives

    # 副詞をリストにして返す
    def extractAdverb(self,text):
        """
        Utility function.

        :param text: string
        :return adverbs: list
        """
        adverbs = []
        for chunk in mecab.parse(text).splitlines()[:-1]:
            (word, feature) = chunk.split('\t')
            if feature.startswith('形容詞'):
                 adverbs.append(word)
        return adverbs

    # 極性辞書から単語の極性値（PN値）を取り出す
    def extractPnValue(self,word):
        """
        :param word: string
        :return pnValue: int
        """
        pnValue = 0
        # TODO: 漢字、ひらがな、カタカナ関係なくPN値を取れるようにする
        pnValue = [pnDfDict['PN'] for pnDfDict in self.pnDfDictsList if pnDfDict['Word'] == word]
        return pnValue

    def extractPnValue2(self,wordAndPartOfSpeechDict):
        """
        :param wordAndPartOfSpeechDict: dictionary
        :return pnValue: int
        """
        pnValue = 0
        # TODO: 漢字、ひらがな、カタカナ関係なくPN値を取れるようにする
        for pnDfDict in self.pnDfDictsList:
            if pnDfDict['Word'] == wordAndPartOfSpeechDict["Word"] and pnDfDict['POS'] == wordAndPartOfSpeechDict["POS"]:
                pnValue = pnDfDict["PN"]
        return pnValue


    # 単語とPN値がペアの辞書型を格納したリストを返す
    def extractWordPnDictsList(self,text):
        """
        Retun dictionaries in list of word and pn value pair.

        :param text: str
        :param wordPnDictsList: list
        """
        wordPnDictsList = []
        for word in self.extractWord(text):
            wordPnDict = {}
            wordPnDict["Word"] = word
            wordPnDict["PN"] = self.extractPnValue(word)
            wordPnDictsList.append(wordPnDict)
        return wordPnDictsList

    # 単語とPN値がペアの辞書型を格納したリストを返す
    def extractWordPnDictsList2(self,text):
        """
        Retun dictionaries in list of word and pn value pair.

        :param text: str
        :param wordPnDictsList: list
        """
        wordPnDictsList = []
        for wordAndPartOfSpeechDict in self.extractWordAndPartOfSpeechDictsList(text):
            wordPnDict = {}
            wordPnDict["Word"] = wordAndPartOfSpeechDict["Word"]
            wordPnDict["PN"] = self.extractPnValue2(wordAndPartOfSpeechDict)
            wordPnDictsList.append(wordPnDict)
        return wordPnDictsList

    # PN値の合計を返す
    def extractSumOfPnValues(self,wordPnDictsList):
        """
        :param wordPnDictsList: list
        :return sumOfPnValues: int
        """
        sumOfPnValues = 0
        for wordPnDict in wordPnDictsList:
            if wordPnDict["PN"]:
                 pnValue = wordPnDict["PN"]
                 # 一旦、PN値を複数持つ単語は平均を取っている ex) "ない"は助動詞と形容詞の両方がある。
                 if isinstance(pnValue, list):
                     sumOfPnValues += mean(pnValue)
                 else:
                     sumOfPnValues += pnValue
        return sumOfPnValues

    # 単語の極性値の平均値を返す
    def extractPnMean(self,wordPnDictsList):
        """
        :param wordPnDictsList: list
        :return pnMean: int
        """
        pnMean = 0
        sumOfPnValues = self.extractSumOfPnValues(wordPnDictsList)
        size = len([wordDict for wordDict in wordPnDictsList if wordDict["PN"]])
        try:
            pnMean = sumOfPnValues/size
        except ZeroDivisionError:
            # TODO:
            pass
        return pnMean

    # テキストの判定結果を返す
    def determiePositiveOrNegative(self,text):
        """
        Return how much posivity or negative a text is.

        :params text:
        :return result: "Very positive", "Somewhat positive", "A little positive",
                        "Neutral"
                        "Very negative", "Somewhat negative", "A little negative"
        """
        result = ""
        wordPnDictsList = self.extractWordPnDictsList(text)
        pnMean = self.extractPnMean(wordPnDictsList)
        if pnMean > 0.66:
            result = "Very positive"
        elif pnMean <= 0.66 and pnMean > 0.33:
            result = "Somewhat positive"
        elif pnMean <= 0.33 and pnMean > 0:
            result = "A little positive"
        elif pnMean ==  0:
            result = "Neutral"
        elif pnMean < 0 and pnMean > -0.33:
            result = "A little negative"
        elif pnMean <= -0.33 and pnMean > -0.66:
            result = "Somewhat negative"
        elif pnMean <= -0.66:
            result = "Very negative"
        return result

    # 単語の正規化
    # https://qiita.com/Hironsan/items/2466fe0f344115aff177
    ## 文字種の統一（e.g. 半角⇨全角）
    def generalizeLetter(self,word):
        pass

    ## 単語の統一（e.g. ソニー⇨Sony）
    def generalizeWord(self,word):
        pass

    ## 数字の置き換え
    def generalizeWord(self,word):
        pass

if __name__ == "__main__":
    # テキスト
    texts = [
            'アイドルAの話し方はきもい。',
            'アイドルAはうざい。',
            'アイドルAしね。',
            'アイドルAは嫌い。',
           'ドナルド・トランプの髪型はなんか変だ。'
           ]
    ma = MorphologyAnalyzer()
    print("========== 結果（形態素別PN値） ==========")
    for text in texts:
        print({text:ma.extractWordPnDictsList(text)})
    print("========== 判定結果 ==========")
    for text in texts:
        print({text:ma.determiePositiveOrNegative(text), "PN値合計":ma.extractSumOfPnValues(ma.extractWordPnDictsList(text))})
