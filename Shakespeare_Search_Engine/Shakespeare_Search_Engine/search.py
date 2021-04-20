import os
from functools import reduce

from django.shortcuts import render
from django.views.decorators import csrf

from . import utils


def search(request):
    ctx = {}
    if request.POST:
        # get parameters query and do word segment
        query = request.POST['query'].strip()
        query_list = utils.word_segment(query)

        # get dictionary
        dictionary_path = os.path.join(
            os.getcwd(), '..', 'output', 'Shakespeare.txt')
        dictionary = utils.get_dictionary(dictionary_path)

        # intersection
        dictionary_list = []
        for word in query_list:
            if word in dictionary.keys():
                dictionary_list.append(dictionary[word.strip()])
        dictionary_set = utils.get_dictionary_set(dictionary_list)

        # result
        document_list = []
        for item in dictionary_set:
            document_list.append({
                'url': item['url'],
                'count': item['count'],
                'title': os.path.splitext(item['url'])[0],
            })

        # sort by count DESC
        document_list.sort(key=utils.get_count_dict, reverse=True)
        ctx['query_list'] = query_list
        ctx['result'] = document_list
        ctx['query'] = query
    return render(request, 'search.html', ctx)
