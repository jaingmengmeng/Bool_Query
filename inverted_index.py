# -*- coding: UTF-8 -*-

import os
import re
import string
import sys
import time
import unicodedata
from datetime import datetime

import jieba
from mrjob.job import MRJob
from mrjob.protocol import RawProtocol
from mrjob.step import MRStep
from zhon.hanzi import punctuation

# from nltk.corpus import stopwords


def get_stopwords(file_name):
    stopwords = [line.strip() for line in open(file_name, 'r', encoding='utf-8').readlines()]
    return stopwords

# stop_words = stopwords.words('english')
stop_words = get_stopwords("cn_stopwords.txt")

def is_number(s):
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

def has_punctuation(s):
    try:
        if re.search(r'[%s]+' % (punctuation + string.punctuation), s) != None:
            return True
    except:
        pass
    return False

def word_segment(text):
    # word segment with jieba
    seg = jieba.lcut_for_search(text, HMM=True)
    res = []
    for word in seg:
        if word not in stop_words and not is_number(word) and not has_punctuation(word):
            res.append(word)
    return res

def get_count(item):
    return item.split(":")[1]

class MRInvertedIndex(MRJob):
    OUTPUT_PROTOCOL = RawProtocol
    FILES = ['cn_stopwords.txt']

    def steps(self):
        return[
            MRStep(mapper = self.mapper, combiner = self.combiner, reducer = self.reducer_1),
            MRStep(reducer = self.reducer_2)
        ]

    def mapper(self, _, line):
        # get file name
        file_name = os.path.split(os.environ["map_input_file"])[1]
        # split with space (for EN)
        # for word in line.split():
        # split with jieba (for ZH)
        for word in word_segment(line):
            yield(word + ":" + file_name, 1)

    def combiner(self, key, values):
        yield(key, sum(values))

    def reducer_1(self, key, values):
        sum = 0
        for value in values:
            sum += value
        word = key.split(":")[0]
        file_name = key.split(":")[1]
        yield(word, file_name + ":" + str(sum))

    def reducer_2(self, word, values):
        # yield(word, ';'.join(values))
        # For a same word (key), sort by number of the word occurrences (value)
        yield(word, ';'.join(sorted(values, key=get_count, reverse=True)))

if __name__ == '__main__':
    start_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(start_time)
    MRInvertedIndex.run()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(end_time)
