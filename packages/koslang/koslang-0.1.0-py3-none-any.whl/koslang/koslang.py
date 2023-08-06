# koSlang/koslang/koslang.py
from eunjeon import Mecab
import os
import pandas as pd

base_path = os.path.dirname(os.path.realpath(__file__))

class koslang:
    def isSlang(self, sentence:str):
        '''
        :param
            sentence: Sentence with unspecified content.
        :return:
            Returns "True" if profanity is included, "False" otherwise.

        mecab.nouns()

        Explain to our algorithm.
        1. Import dataframe
        2. Parameter Sentence is divided into test cases using the following three functions.
            - mecab.nouns()
        3. Check the test cases divided according to each case belong to the DataFrame one by one.
        4. If at least one case is included, we return "True" value, otherwise return "False" value.
        '''
        dataset = pd.read_csv(f"{base_path}/data.csv", sep=',', encoding='cp949', index_col=0)

        mecab = Mecab()
        noun = mecab.morphs(sentence)

        for slang in dataset.index:
            if slang in noun:
                return True
        return False

    def analysis(self, sentence:str):
        mecab = Mecab()
        noun = mecab.morphs(sentence)
        return(print(noun))

    def showData(self):
        dataset = pd.read_csv(f"{base_path}/data.csv", sep=',', encoding='cp949', index_col=0)
        return(print(dataset))

