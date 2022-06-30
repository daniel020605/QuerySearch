
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


import jieba.posseg as pseg
import re
import os
from gensim.summarization import bm25
from gensim import corpora
import codecs
import math
from six import iteritems
from six.moves import xrange
import xmnlp
import Pinyin2Hanzi


# BM25 parameters.
PARAM_K1 = 1.5
PARAM_B = 0.75
EPSILON = 0.25
xmnlp.set_model('xmnlp-onnx-models')

class BM25(object):

    def __init__(self, corpus):
        self.corpus_size = len(corpus)
        self.avgdl = sum(map(lambda x: float(len(x)), corpus)
                         ) / self.corpus_size
        self.corpus = corpus
        self.f = []
        self.df = {}
        self.idf = {}
        self.initialize()

    def initialize(self):
        for document in self.corpus:
            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.f.append(frequencies)

            for word, freq in iteritems(frequencies):
                if word not in self.df:
                    self.df[word] = 0
                self.df[word] += 1

        for word, freq in iteritems(self.df):
            self.idf[word] = math.log(
                self.corpus_size - freq + 0.5) - math.log(freq + 0.5)

    def get_score(self, document, index, average_idf):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            idf = self.idf[word] if self.idf[word] >= 0 else EPSILON * average_idf
            score += (idf * self.f[index][word] * (PARAM_K1 + 1)
                      / (self.f[index][word] + PARAM_K1 * (1 - PARAM_B + PARAM_B * self.corpus_size / self.avgdl)))
        return score

    def get_scores(self, document, average_idf):
        scores = []
        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, average_idf)
            scores.append(score)
        return scores


def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag

    dagParams = DefaultDagParams()
    # path_num：候选值，可设置一个或多个
    result = dag(dagParams, pinyinList, path_num=10, log=True)
    for item in result:
        # socre = item.score # 得分
        res = item.path # 转换结果
        return res


def get_bm25_weights(corpus):
    bm25 = BM25(corpus)
    average_idf = sum(
        map(lambda k: float(bm25.idf[k]), bm25.idf.keys())) / len(bm25.idf.keys())

    weights = []
    for doc in corpus:
        scores = bm25.get_scores(doc, average_idf)
        weights.append(scores)

    return weights


  # TODO停词表地址
stopwords = codecs.open(
    'stopwords-master\\baidu_stopwords.txt', 'r', encoding='utf8').readlines()
stopwords = [w.strip() for w in stopwords]
stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']


# def unshell(string):
#
def check(str):
  my_re = re.compile(r'[A-Za-z]',re.S)
  res = re.findall(my_re,str)
  if len(res):
      return True
  else:
      return False

def tokenization(filename):
    result = []
    with open('corpus/'+filename, 'r',encoding='utf-8') as f:
        text = f.read()
        words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result
corpus = []
dirname = 'corpus'
filenames = []
for root,dirs,files in os.walk(dirname):
    for f in files:
        if re.match(r'[\u4e00-\u9fa5]*.txt', f):
            corpus.append(tokenization(f))
            filenames.append(f)

dictionary = corpora.Dictionary(corpus)

doc_vectors = [dictionary.doc2bow(text) for text in corpus]

vec1 = doc_vectors[0]
vec1_sorted = sorted(vec1, key=lambda x: x[1], reverse=True)

# print (len(vec1_sorted))
# for term, freq in vec1_sorted[:5]:
#     print (dictionary[term])



bm25Model = BM25(corpus)
average_idf = sum(map(lambda k: float(
    bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
query_str = input('请输入query:')
import synonyms

query_synonyms = synonyms.nearby(query_str)
# print(synonyms.nearby(query_str))
query_Synonyms = []
if re.match(r'[\u4e00-\u9fa5]*' , query_str):
    query = []
    for word in query_str.split(' '):
        query.append(word)
    scores_list = []
    for i in query:
        for j in range(0,1):
            query_Synonyms.append(synonyms.nearby(i)[0][j])
    scores = bm25Model.get_scores(query_Synonyms,average_idf=average_idf)
    # scores = bm25Model.get_scores(query)
# scores.sort(reverse=True)
    print(scores)
    idx = scores.index(max(scores))


    fname = filenames[idx]
    fname = fname.split('.')[0]

    print ("您可能想看的是:"+fname)


if sum(scores) == 0:
    if check(query_str):
        piny = xmnlp.pinyin(query_str)
        hanzilsit = pinyin_2_hanzi(piny)
        query_str = hanzilsit[0]
        query = []
        for word in query_str.split(' '):
            query.append(word)

    else:
        wrong_word = xmnlp.checker(query_str)
        index = wrong_word.keys().__str__()[9:].lstrip("(").rstrip(")").lstrip("[").rstrip("]").lstrip("(").rstrip(")").split(",")
        index[1] = list(index[1])[2]
        substitute = wrong_word.values().__str__()[11:]
        query_str = query_str.replace(index[1], substitute[5])
    print("您可能想找的是:"+query_str)
    for word in query_str.split(' '):
        query.append(word)
    scores = bm25Model.get_scores(query)

print (scores)
idx = scores.index(max(scores))
print (idx)
fname = filenames[idx]
fname = fname.split('.')[0]
print (fname)



