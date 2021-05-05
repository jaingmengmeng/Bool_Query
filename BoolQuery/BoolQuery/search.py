import os
import re
from functools import reduce

import jieba
from django.shortcuts import render
from django.views.decorators import csrf

from .utils import Doc_List, Word_Segment


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


class Bool_Query:
    def __init__(self):
        self.operators = ['OR', 'AND', 'NOT', 'XOR', '(', ')']
        # get dictionary
        self.dictionary_path = os.path.join(
            os.getcwd(), '..', 'index_list.txt')
        self.dictionary = self.get_dictionary(self.dictionary_path)

    def get_dictionary(self, path):
        dictionary = {}
        if os.path.exists(path):
            file = open(path)
            for line in file:
                if line != '\n':
                    word = line.split('\t')[0]
                    if word != '' and word != ' ':
                        try:
                            file_list = [int(each) for each in line.split('\t')
                                         [1].split(',')]
                            dictionary[word] = file_list
                        except:
                            pass
        return dictionary

    def get_index_list(self, word):
        if word.strip() in BQ.dictionary.keys():
            return self.dictionary[word.strip()]
        else:
            return []

    def AND(self, list1, list2):
        result = []
        p1 = 0
        p2 = 0
        while p1 < len(list1) and p2 < len(list2):
            if list1[p1] == list2[p2]:
                result.append(list1[p1])
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                p1 += 1
            else:
                p2 += 1
        return result

    def OR(self, list1, list2):
        result = []
        p1 = 0
        p2 = 0
        while p1 < len(list1) and p2 < len(list2):
            if list1[p1] == list2[p2]:
                result.append(list1[p1])
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                result.append(list1[p1])
                p1 += 1
            else:
                result.append(list2[p2])
                p2 += 1
        if p1 < len(list1):
            result.extend(list1[p1:])
        if p2 < len(list2):
            result.extend(list2[p2:])
        return result

    def NOT(self, list1, list2):
        result = []
        p1 = 0
        p2 = 0
        while p1 < len(list1) and p2 < len(list2):
            if list1[p1] == list2[p2]:
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                result.append(list1[p1])
                p1 += 1
            else:
                p2 += 1
        if p1 < len(list1):
            result.extend(list1[p1:])
        return result

    def XOR(self, list1, list2):
        result = []
        p1 = 0
        p2 = 0
        while p1 < len(list1) and p2 < len(list2):
            if list1[p1] == list2[p2]:
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                result.append(list1[p1])
                p1 += 1
            else:
                result.append(list1[p1])
                p2 += 1
        if p1 < len(list1):
            result.extend(list1[p1:])
        if p2 < len(list2):
            result.extend(list2[p2:])
        return result

    def __calculate(self, op, list1, list2):
        if op == 'AND':
            return self.AND(list1, list2)
        elif op == 'OR':
            return self.OR(list1, list2)
        elif op == 'NOT':
            return self.NOT(list1, list2)
        elif op == 'XOR':
            return self.XOR(list1, list2)

    def __parser(self, query):
        result = []
        pattern = re.compile(
            r'|'.join([each if each not in ['(', ')'] else '\%s' % (each) for each in self.operators]))
        operators_list = pattern.findall(query)
        start = 0
        for operator in operators_list:
            pos = query.find(operator, start)
            if query[start:pos].strip() != '':
                keyword = query[start:pos].strip()
                result = result + self.__split(keyword)
            result.append(operator)
            start = pos + len(operator)
        if start < len(query):
            keyword = query[start:].strip()
            result = result + self.__split(keyword)
        return result

    def __split(self, keyword):
        result = []
        keyword_list = keyword.split(' ')
        if len(keyword_list) == 1:
            result.append(keyword)
        else:
            result.append('(')
            for i in range(len(keyword_list)):
                if i > 0:
                    result.append('AND')
                result.append(keyword_list[i])
            result.append(')')
        return result

    def solve(self, query):
        parser_result = self.__parser(query)
        print(parser_result)
        operators_stack = Stack()
        operands_stack = Stack()
        for token in parser_result:
            if token in self.operators[0:4]:
                if operators_stack.is_empty():
                    operators_stack.push(token)
                else:
                    if operators_stack.peek() != "(":
                        op = operators_stack.pop()
                        op2 = operands_stack.pop()
                        op1 = operands_stack.pop()
                        result = self.__calculate(op, op1, op2)
                        operands_stack.push(result)
                    operators_stack.push(token)
            elif token == "(":
                operators_stack.push(token)
            elif token == ")":
                while operators_stack.peek() != "(":
                    op = operators_stack.pop()
                    op2 = operands_stack.pop()
                    op1 = operands_stack.pop()
                    result = self.__calculate(op, op1, op2)
                    if result != None:
                        operands_stack.push(result)
                operators_stack.pop()
            else:
                operands_stack.push(self.get_index_list(token))
        while operands_stack.size() > 1:
            op = operators_stack.pop()
            op2 = operands_stack.pop()
            op1 = operands_stack.pop()
            result = self.__calculate(op, op1, op2)
            operands_stack.push(result)
        if operands_stack.size() > 0:
            return parser_result, operands_stack.pop()
        else:
            return parser_result, []


DL = Doc_List()
BQ = Bool_Query()


def search(request):
    ctx = {}
    if request.POST:
        # get parameters query and do word segment
        query = request.POST['query'].strip()
        # result
        document_list = []
        if query != '':
            parser_result, bool_query_result = BQ.solve(query)
            print(bool_query_result)
            for item in bool_query_result:
                document_list.append({
                    'index': item,
                    'url': DL.get_url_by_index(item),
                    'title': os.path.splitext(os.path.basename(DL.get_url_by_index(item)))[0],
                    'file': os.path.basename(DL.get_url_by_index(item)),
                })
            # sort by count DESC
            document_list.sort(key=lambda item: item['index'], reverse=False)
            ctx['parser_result'] = parser_result
            ctx['result'] = document_list
            ctx['query'] = query
    return render(request, 'search.html', ctx)
