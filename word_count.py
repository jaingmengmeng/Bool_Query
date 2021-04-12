# -*- coding: UTF-8 -*-

import os
import sys
import time
import jieba
from datetime import datetime
from nltk.corpus import stopwords
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawProtocol

def get_stopwords(file_name):
    stopwords = [line.strip() for line in open(file_name, 'r', encoding='utf-8').readlines()]
    return stopwords

# stop_words = stopwords.words('english')
stop_words = get_stopwords("/Users/youngjiang/Young/Course/2021-Spring/IIR-XuJun/Bool_Query/cn_stopwords.txt")
# stop_words = get_stopwords("/home/jly/Bool_Query/cn_stopwords.txt")
# stop_words = get_stopwords(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cn_stopwords.txt"))

def word_segment(text):
    # word segment with jieba
    seg = jieba.lcut_for_search(text, HMM=True)
    res = []
    for word in seg:
        if word not in stop_words:
            res.append(word)
    return res

class MRWordCount(MRJob):
    OUTPUT_PROTOCOL = RawProtocol

    def mapper(self, _, line):
        for word in word_segment(line):
            yield(word, 1)

    def reducer(self, word, counts):
        yield(word, str(sum(counts)))

if __name__ == '__main__':
    start_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(start_time)
    MRWordCount.run()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(end_time)