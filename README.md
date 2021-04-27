# Bool_Query

A simple search engine supports Boolean Query.

# Usage

```bash
# run word count
python word_count.py -r local docs/Shakespeare > word_count.txt

# run doc list, generate doc_list.txt
python utils -r docs/Shakespeare

# run inverted index, generate index_list.txt
python inverted_index.py -r local docs/Shakespeare > index_list.txt

# run django demo
cd BoolQuery
python manage.py runserver
python manage.py runserver 0.0.0.0:8000 (allow all hosts)
```

Browser open: http://127.0.0.1:8000/

# Reference

[中文停用词表](https://github.com/goto456/stopwords)
