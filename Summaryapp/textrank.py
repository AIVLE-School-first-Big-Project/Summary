from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
# import pandas as pd

def textrank(text):
    text = str(text)
    kkma = Kkma()

    def text2sentences(text):
        sentences = kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    # 텍스트를 입력받아 문장 단위로 나눔
    sentences = text2sentences(text)

    twitter = Twitter()

    file_path = 'Summaryapp\\word.txt'

    with open(file_path, encoding = 'UTF8') as f:
        lines = f.readlines()
        
    lines = [line.rstrip('\n') for line in lines]
    stopwords = lines

    def get_nouns(sentences):
        nouns = []
        for sentence in sentences:
            nouns.append(' '.join([noun for noun in twitter.nouns(str(sentence))
                                if noun not in stopwords and len(noun) > 1]))
        return nouns

    # 불용어 제거
    nouns = get_nouns(sentences)

    tfidf = TfidfVectorizer()
    cnt_vec = CountVectorizer()
    # graph_sentence = []

    def build_sent_graph(sentence):
        tfidf_mat = tfidf.fit_transform(sentence).toarray()
        graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return graph_sentence

    sent_graph = build_sent_graph(nouns)

    # idx2word는 단어횟수
    def build_words_graph(sentence):
        cnt_vec_mat = normalize(cnt_vec.fit_transform(sentence).toarray().astype(float), axis = 0)
        vocab = cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

    words_graph, idx2word = build_words_graph(nouns)

    def get_ranks(graph, d = 0.85):
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0
            link_sum = np.sum(A[:, id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        
        B = (1 - d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)
        return {idx : r[0] for idx, r in enumerate(ranks)}

    sent_rank_idx = get_ranks(sent_graph)

    sorted_sent_rank_idx = sorted(sent_rank_idx, key = lambda k : sent_rank_idx[k], reverse = True)

    word_rank_idx = get_ranks(words_graph)
    sorted_word_rank_idx = sorted(word_rank_idx, key = lambda k : word_rank_idx[k], reverse = True)

    # 5문장으로 요약
    def summarize(sent_num = 5):
        summary = []
        index = []
        for idx in sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
            
        index.sort()
        
        for idx in index:
            summary.append(sentences[idx])
            
        for text in summary :
            print(text)
            print("\n")
            
    # 키워드 출력
    def keywords(word_num = 10):
        
        keywords = []
        index = []
        for idx in sorted_word_rank_idx[:word_num]:
            index.append(idx)
            
        for idx in index:
            keywords.append(idx2word[idx])

        return keywords
    
    answer = keywords()
    
    return answer