import pandas as pd
from konlpy.tag import Mecab
import spacy
import pkuseg
import jieba.posseg as psg
import jieba
import re
import util.file_util as ft
import util.random_sample_util as rst

# df = pd.read_csv('../data/raw/zhko/SELECT_substr_tg_ipc_1_1_as_ipc_ca.filter.csv')
# df = df[['src', 'tgt']]

# train = rst.random_sampling(df, random_seed=123, sample_num=158, data='train')
# test = rst.random_sampling(df, random_seed=123, sample_num=158, data='test')
test_zh = ft.get_all_lines('../data/input/nlp_zh_test.txt')
test_ko = ft.get_all_lines('../data/input/nlp_ko_test.txt')

# Spacy 명사 추출.
nlp = spacy.load('zh_core_web_sm')
spacy_list = []
for text in test_zh:
    doc = nlp(text)
    l_text = []
    for t in doc:
        l_text.append((t.text, t.pos_))
    spacy_list.append(l_text)
print(len(spacy_list))
print(spacy_list[1])

spacy_noun_list = []
for i in range(len(spacy_list)):
    noun_i = []
    for j in range(len(spacy_list[i])):
        if spacy_list[i][j][1] == 'NOUN':
            noun_i.append(spacy_list[i][j][0])
    spacy_noun_list.append(noun_i)
print(len(spacy_noun_list))

# PKUSEG 명사 추출.
seg = pkuseg.pkuseg(model_name='default', postag=True)
zh_pos = [seg.cut(text) for text in test_zh]
print(len(zh_pos))
print(test_zh[1])
print(zh_pos[1])

noun = ['n', 'nr', 'ns', 'nt', 'nx', 'nz']

pkuseg_noun_list = []
for i in range(len(zh_pos)):
    noun_i = []
    for j in range(len(zh_pos[i])):
        if zh_pos[i][j][1] in noun:
            noun_i.append(zh_pos[i][j][0])
    pkuseg_noun_list.append(noun_i)
print(len(pkuseg_noun_list))
print(pkuseg_noun_list[1])

# Jieba 명사 추출.
jieba_t = psg.cut(test_zh[1])
jieba_list = []
for text in test_zh:
    n_list = []
    j_tag = list(psg.cut(text))
    for j in range(len(j_tag)):
        j_text = str(j_tag[j]).split('/')[0]
        j_tg = str(j_tag[j]).split('/')[1]
        n_list.append((j_text, j_tg))
    jieba_list.append(n_list)
print(len(jieba_list))
print(jieba_list[1])

jieba_noun_list = []
for i in range(len(jieba_list)):
    noun_i = []
    for j in range(len(jieba_list[i])):
        if jieba_list[i][j][1] in noun:
            noun_i.append(jieba_list[i][j][0])
    jieba_noun_list.append(noun_i)
print(len(jieba_noun_list))
print(jieba_noun_list[1])

zh_noun_df = pd.DataFrame({'text_ko': test_ko,
                           'text_zh': test_zh,
                           'spacy': spacy_noun_list,
                           'pkuseg': pkuseg_noun_list,
                           'jieba': jieba_noun_list})
print(len(zh_noun_df))
print(zh_noun_df.head())

zh_noun_df.to_excel('../data/output/extract_noun_zh.xlsx', index=False)
