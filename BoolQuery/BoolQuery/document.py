import os

from django.shortcuts import render
from django.views.decorators import csrf

from .utils import Doc_List

DL = Doc_List()


def document(request, file):
    ctx = {}
    ctx['title'] = os.path.splitext(file)[0]
    url = DL.get_url_by_index(DL.get_doc_index(file))
    ctx['url'] = url
    content_list = []
    if os.path.exists(url):
        with open(url, 'r') as f:
            for line in f.readlines():
                content_list.append(line)
            ctx['content'] = content_list
    return render(request, 'document.html', ctx)
