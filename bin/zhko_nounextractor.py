import pandas as pd
import util.file_util as ft
from konlpy.tag import Mecab
from khaiii import KhaiiiApi


def khaii_morphs(sentence, tokenizer=KhaiiiApi()):  # tag 정보 포함 추출.
    k_sent = tokenizer.analyze(sentence)
    tokens = []
    for word in k_sent:
        tokens.extend([(str(m.lex), str(m.tag)) for m in word.morphs])
    return tokens


def Noun_extract(pos_list):
    '''
    NNG = 일반명사, NNP = 고유명사, NP = 대명사
    :param pos_list: tagging된 리스트
    :return: 명사 리스트
    '''
    result = []
    noun = ['NNG', 'NNP', 'NP']
    for i in range(len(pos_list)):
        noun_i = []
        for j in range(len(pos_list[i])):
            if pos_list[i][j][1] in noun:
                noun_i.append(pos_list[i][j][0])
        result.append(noun_i)
    return result


df = pd.read_excel('../data/output/extract_noun_zh.xlsx')
print(df.columns)

mecab = Mecab()
mecab_ko = [mecab.pos(s) for s in df['text_ko']]
mecab_noun = Noun_extract(mecab_ko)
print(mecab_ko)
print(mecab_noun)
print(len(mecab_noun))

khaiii_ko = []
for s in df['text_ko']:
    s2 = khaii_morphs(s)
    khaiii_ko.append(s2)
print(khaiii_ko[0])
khaiii_noun = Noun_extract(khaiii_ko)
print(khaiii_noun)
print(len(khaiii_noun))

result_df = pd.DataFrame({'KO': df['text_ko'],
                          'mecab': mecab_noun,
                          'ZH': df['text_zh'],
                          'spacy':df['spacy'],
                          'pkuseg':df['pkuseg'],
                          'jieba':df['jieba']})
print(result_df.head())

result_df.to_excel('../data/output/zhko_extract_noun.xlsx', index=False)
