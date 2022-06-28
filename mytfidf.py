from collections import Counter

import nltk
import math
import string
import jieba

from nltk import PorterStemmer
from nltk.corpus import stopwords

import fileRW
import file_getter

texts = []  #todo:修改文档读取路径
stopwords_list = fileRW.file_reader("cn_stopwords.txt")


text1 = u"草种业是草原生态修复与草业的“芯片”，是国家战略性、基础性核心产业。作为草原大国，我国草原面积近40" \
        u"亿亩，草种业健康发展是改善我国生态的基础保障，是推动我国草原与草业事业跨越式发展的重要引擎。从我国的粮食安全现状看，现阶段的粮食安全，事实上主要是饲料粮的安全、蛋白质供应的安全，而这些主要来源于草原，草原健康直接关乎优质安全食物的供给保障能力。 "
text2 = u"会议强调，草原是我国生态文明建设主战场，草原工作“重”在保护，“要”在修复，“核心”是质量，基础是草种，要把草种的种源安全提升到关系国家安全的战略高度，集中力量破难题、补短板、强优势、控风险，实现草种业种源自主可控、产业自立自强。 "
text3 = u"为保障我国草原生态建设和草业高质量发展重大科技需求提供强有力支撑，2019" \
        u"年，中国林科院在国家林草局的指导下，整合全院相关优势学科和团队资源，成立了国家林草局草原研究中心，组建了草地资源与利用、草原保护与生态修复、草原监测与评估、草原生态系统管理等研究团队。并与兰州大学、中国农业大学、中科院等国家知名高校及科研院所建立了不同形式的全面合作，草种质创新与育种团队和草原保护修复团队快速发展壮大，建立了覆盖全国不同气候区的草种质资源圃、育制种基地和生态适应性测试基地，育成的品种也同步转化，并在我国北方各类困难立地广泛应用，初步形成了“产学研用”全面发展新局面。 "

def get_tokens(text):
    #语料切片 + 清洗
    ret = []
    cut = jieba.cut_for_search(text)
    for i in cut:
        if i not in stopwords_list:
            ret.append(i)
    return ret


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list)) / (1 + n_containing(word, count_list))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


def count_term(text):
    tokens = get_tokens(text)
    count = Counter(tokens)
    return count


def main():
    texts = [file_getter.getfile("种草文章.txt")]
    countlist = []
    for text in texts:
        countlist.append(count_term(text))
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

    #bug:只有一篇text时会无法正常得到TFIDF


if __name__ == "__main__":
    main()
