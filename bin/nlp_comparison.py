from konlpy.tag import Mecab
from khaiii import KhaiiiApi
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
import pandas as pd
import math
from time import time
import util.file_util as ft
import util.random_sample_util as rst


def word_score(score):
    return score.cohesion_forward * math.exp(score.right_branching_entropy)


path = '../data/raw/enko/'

df = pd.read_csv(path + 'enko_patent_20211029.csv')

src = df[['src']]
tgt = df[['tgt']]

train_soy = rst.random_sampling(tgt, random_seed=123, sample_num=100, data='train')
print(len(train_soy))
comparison_data = rst.random_sampling(tgt, random_seed=123, sample_num=100, data='test')
# comparison_data.to_csv('../data/test_100.csv', index=False)
print(len(comparison_data))
print(comparison_data)

# Mecab
mecab_start = time()
mecab = Mecab()
mecab_result = [mecab.morphs(s) for s in comparison_data['tgt']]
print(len(mecab_result))
print(mecab_result)
mecab_end = time()
print(f'Mecab Time : {mecab_end - mecab_start} sec')


# ft.write_list_file(mecab_result, '../data/mecab_morphs.txt')


# Khaiii
def khaii_morphs(sentence, tokenizer=KhaiiiApi()): # tag 정보 포함 추출.
    k_sent = tokenizer.analyze(sentence)
    tokens = []
    for word in k_sent:
        tokens.extend([(str(m.lex), str(m.tag)) for m in word.morphs])
    return tokens


def khaii_morphs2(sentence, tokenizer=KhaiiiApi()): # 형태소 분리.
    k_sent = tokenizer.analyze(sentence)
    tokens = []
    for word in k_sent:
        tokens.extend([str(m).split("/")[0] for m in word.morphs])
    return tokens


kh_start = time()
kh_morphs_list = []
for s in comparison_data['tgt']:
    s2 = khaii_morphs2(s)
    kh_morphs_list.append(s2)
print(kh_morphs_list[0])
print(len(kh_morphs_list))
kh_end = time()
print(f'Khaiii Time : {kh_end - kh_start} sec')


# soynlp
soy_start = time()
word_extractor = WordExtractor(min_cohesion_forward=0.05,
                               min_right_branching_entropy=0.0)
word_extractor.train(train_soy['tgt'])
model_path = '../model/wordextractor_default_params.model'
# word_extractor.save(model_path)

model = word_extractor.load(model_path)
words = word_extractor.extract(model)

cohesion_scores = {word: word_score(score) for word, score in
                   words.items()}
l_tokenizer = LTokenizer(scores=cohesion_scores)
l_tok_corpus = [l_tokenizer.tokenize(sent) for sent in comparison_data['tgt']]

print(l_tok_corpus)
soy_end = time()
print(f'Soynlp Time : {soy_end - soy_start} sec')

comparison_df = pd.DataFrame({'raw_text':comparison_data['tgt'],
                              'mecab' : mecab_result,
                              'khaiii' : kh_morphs_list,
                              'soynlp' : l_tok_corpus})
print(comparison_df.head())
comparison_df.to_excel('../Result_comparison_2236269.xlsx', index=False)
#
# # 시간 : khaiii < mecab < soynlp 순으로 소모.
