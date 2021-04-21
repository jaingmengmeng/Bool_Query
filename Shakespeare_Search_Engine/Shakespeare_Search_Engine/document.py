import os

from django.shortcuts import render
from django.views.decorators import csrf


def document(request, url):
    ctx = {}
    ctx['title'] = os.path.splitext(url)[0]
    ctx['url'] = url
    file_path = os.path.join(
        os.getcwd(), '..', 'docs', 'Shakespeare', url)
    content_list = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                content_list.append(line)
            ctx['content'] = content_list
    return render(request, 'document.html', ctx)
