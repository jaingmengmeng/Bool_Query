import os
import re
import string
import unicodedata

import jieba
from zhon.hanzi import punctuation


class Doc_List:
    def __init__(self, path=os.path.join(os.getcwd(), '..', 'Shakespeare_list.txt')):
        self.path = path
        self.doc_list = self.__get_doc_list(path)

    def __get_doc_list(self, path):
        result = [line.strip() for line in open(
            path, 'r', encoding='utf-8').readlines()]
        return result

    def get_doc_index(self, file_name):
        if file_name in self.doc_list:
            return self.doc_list.index(file_name)
        else:
            return None

    def get_doc_by_index(self, index):
        if index < len(self.doc_list):
            return self.doc_list[index]
        else:
            return None


class Word_Segment:
    def __init__(self, path=os.path.join(os.getcwd(), '..', 'cn_stopwords.txt')):
        # from nltk.corpus import stopwords
        # stop_words = stopwords.words('english')
        self.__stop_words = self.__get_stopwords(path)

    def __get_stopwords(self, file_name):
        result = [line.strip() for line in open(
            file_name, 'r', encoding='utf-8').readlines()]
        return result

    def word_segment(self, text):
        # word segment with jieba
        seg = jieba.lcut_for_search(text, HMM=True)
        result = []
        for word in seg:
            if word not in self.__stop_words and not self.__is_number(word) and not self.__has_punctuation(word):
                result.append(word)
        return result

    def __is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def __has_punctuation(self, s):
        try:
            if re.search(r'[%s]+' % (punctuation + string.punctuation), s) != None:
                return True
        except:
            pass
        return False
