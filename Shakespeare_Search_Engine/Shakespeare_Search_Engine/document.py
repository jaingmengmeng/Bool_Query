import os

from django.shortcuts import render
from django.views.decorators import csrf
from SearchEngineModel.models import Document


def document(request, document_id):
    ctx = {}
    document = Document.objects.get(document_id=document_id)
    ctx['title'] = document.title
    ctx['url'] = document.url
    file_path = os.path.join(os.path.abspath('.'), 'Shakespeare_Search_Engine', 'statics', 'docs', 'Shakespeare', document.url)
    content_list = []
    if os.path.exists(file_path):
        with open(file_path , 'r') as f:
            for line in f.readlines():
                content_list.append(line)
            ctx['content'] = content_list
    return render(request, 'document.html', ctx)
