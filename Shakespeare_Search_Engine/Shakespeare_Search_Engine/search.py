from django.shortcuts import render
from django.views.decorators import csrf
from SearchEngineModel.models import Dictionary, Document


def search(request):
    ctx = {}
    if request.POST:
        query = request.POST['query']
        dictionary_list = Dictionary.objects.filter(word=query).order_by('-count')
        document_list = []
        for item in dictionary_list:
            document_list.append({
                    'document_id' : item.document_id, 
                    'url' : item.document.url,
                    'count' : item.count,
                    'title' : item.document.title,
                })
        ctx['result'] = document_list
        ctx['query'] = query
    return render(request, 'search.html', ctx)
