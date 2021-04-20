import os
import re
import string
import unicodedata

import jieba
from zhon.hanzi import punctuation


def get_dictionary(path):
    dictionary = {}
    if os.path.exists(path):
        file = open(path)
        for line in file:
            if line != '\n':
                word = line.split('\t')[0]
                if word != '' and word != ' ':
                    try:
                        file_list = [{
                            'url': each.split(':')[0],
                            'count': int(each.split(':')[1])
                        } for each in line.split('\t')[1].split(';')]
                        dictionary[word] = file_list
                    except:
                        pass
    return dictionary


def get_dictionary_set(dictionary_list):
    res = []
    if len(dictionary_list) > 0:
        res = dictionary_list[0]
    if len(dictionary_list) > 1:
        for i in range(1, len(dictionary_list)):
            for each in res:
                if each not in dictionary_list[i]:
                    res.remove(each)
    return res


def get_stopwords(file_name):
    stopwords = [line.strip() for line in open(
        file_name, 'r', encoding='utf-8').readlines()]
    return stopwords


# from nltk.corpus import stopwords
# stop_words = stopwords.words('english')
stopwords_path = os.path.join(
    os.getcwd(), '..', 'cn_stopwords.txt')
stop_words = get_stopwords(stopwords_path)


def get_doc_list(dir):
    doc_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                doc_list.append(file)
    return doc_list


doc_list = get_doc_list('docs/Shakespeare')


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


def get_count_dict(item):
    return item['count']
