import os
import sys
import time

from mrjob.job import MRJob
from mrjob.protocol import RawProtocol
from mrjob.step import MRStep

from utils import Doc_List, Word_Segment


class MRInvertedIndex(MRJob):
    OUTPUT_PROTOCOL = RawProtocol
    FILES = ['cn_stopwords.txt', 'utils.py', 'doc_list.txt']

    def steps(self):
        return[
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]

    def mapper(self, _, line):
        WS = Word_Segment()
        DL = Doc_List()
        # get file name
        file_name = os.path.split(os.environ["map_input_file"])[1]
        # split with space (for EN)
        # for word in line.split():
        # split with jieba (for ZH)
        for word in WS.word_segment(line):
            index = DL.get_doc_index(file_name)
            yield(word, str(index))

    def reducer(self, key, values):
        yield(key, ','.join(sorted(set(values), key=self.__cmp, reverse=False)))

    def __cmp(self, index):
        return int(index)


if __name__ == '__main__':
    start_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(start_time)
    MRInvertedIndex.run()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    sys.stderr.write(end_time)
