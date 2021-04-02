# -*- coding: UTF-8 -*-
import os
import jieba
from nltk.corpus import stopwords
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawProtocol

def get_stopwords(file_name):
    stopwords = [line.strip() for line in open(file_name, 'r', encoding='utf-8').readlines()]
    return stopwords

# stop_words = stopwords.words('english')
stop_words = get_stopwords("/Users/youngjiang/Young/Course/IIR-XuJun/Bool_Query/cn_stopwords.txt")

def word_segment(text):
    # word segment with jieba
    seg = jieba.lcut_for_search(text, HMM=True)
    res = []
    for word in seg:
        if word not in stop_words:
            res.append(word)
    return res

class MRInvertedIndex(MRJob):
    OUTPUT_PROTOCOL = RawProtocol

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
        for word in word_segment(line.replace('\t', '')):
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
        yield(word, ';'.join(values))

if __name__ == '__main__':
    MRInvertedIndex.run()