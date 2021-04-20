# -*- coding: UTF-8 -*-

import os
import sys
import time

from mrjob.job import MRJob
from mrjob.protocol import RawProtocol
from mrjob.step import MRStep

from utils import get_count, word_segment


class MRWordCount(MRJob):
    OUTPUT_PROTOCOL = RawProtocol
    FILES = ['cn_stopwords.txt', 'utils.py']

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
