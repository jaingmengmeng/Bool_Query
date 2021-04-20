# -*- coding: UTF-8 -*-

import os
import sys
import time

from mrjob.job import MRJob
from mrjob.protocol import RawProtocol
from mrjob.step import MRStep

from utils import get_count, word_segment, doc_list


class MRInvertedIndex(MRJob):
    OUTPUT_PROTOCOL = RawProtocol
    FILES = ['cn_stopwords.txt', 'utils.py']

    def steps(self):
        return[
            MRStep(mapper=self.mapper, combiner=self.combiner,
                   reducer=self.reducer_1),
            MRStep(reducer=self.reducer_2)
        ]

    def mapper(self, _, line):
        # get file name
        file_name = os.path.split(os.environ["map_input_file"])[1]
        # split with space (for EN)
        # for word in line.split():
        # split with jieba (for ZH)
        for word in word_segment(line):
            # index = doc_list.index(file_name)
            index = file_name
            yield(word + ":" + index, 1)

    def combiner(self, key, values):
        yield(key, sum(values))

    def reducer_1(self, key, values):
        sum = 0
        for value in values:
            sum += value
        word = key.split(":")[0]
        index = key.split(":")[1]
        yield(word, index + ":" + str(sum))

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
