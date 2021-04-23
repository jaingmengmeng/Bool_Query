import os
from functools import reduce

from django.shortcuts import render
from django.views.decorators import csrf

from .utils import Doc_List, Word_Segment

# Word_Segment & Doc_List
WS = Word_Segment()
DL = Doc_List()


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
                            'index': int(each.split(':')[0]),
                            'url': DL.get_url_by_index(int(each.split(':')[0])),
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


def get_count_dict(item):
    return item['count']


# get dictionary
dictionary_path = os.path.join(
    os.getcwd(), '..', 'Shakespeare.txt')
dictionary = get_dictionary(dictionary_path)


def search(request):
    ctx = {}
    if request.POST:
        # get parameters query and do word segment
        query = request.POST['query'].strip()
        query_list = WS.word_segment(query)

        # intersection
        dictionary_list = []
        for word in query_list:
            if word in dictionary.keys():
                dictionary_list.append(dictionary[word.strip()])
        dictionary_set = get_dictionary_set(dictionary_list)

        # result
        document_list = []
        for item in dictionary_set:
            document_list.append({
                'url': item['url'],
                'count': item['count'],
                'title': os.path.splitext(os.path.basename(item['url']))[0],
                'file': os.path.basename(item['url']),
            })

        # sort by count DESC
        document_list.sort(key=get_count_dict, reverse=True)
        ctx['query_list'] = query_list
        ctx['result'] = document_list
        ctx['query'] = query
    return render(request, 'search.html', ctx)
