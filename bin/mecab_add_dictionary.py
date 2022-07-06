import pandas as pd
import util.file_util as ft
import argparse

def has_coda(word):
    '''
    국문 받침 확인
    :param word: 문장
    :return: 받침이 있는 경우 False, 없는 경우 True
    EX: 안녕하세요 = True, 안녕 = False
    '''
    return (ord(word[-1]) - 44032) % 28 == 0


def args():
    parser = argparse.ArgumentParser(usage='usage', description='Usage of parameters ')
    parser.add_argument('--user_dic', required=False, default='/usr/local/lib/mecab/dic/mecab-ko-dic-20180720/user-dic/nnp.csv')
    parser.add_argument('--add_dic', required=False, default='../../enko_patent_dict/term_2dir_en-XX-ko-YY_Patent__patent-ALL-kipo-20180302.ko/term_2dir_en-XX-ko-YY_Patent__patent-ALL-kipo-20180302.ko')
    return parser.parse_args()


def main():
    config = args()
    user_dic = config.user_dic
    add_dic = config.add_dic
    nnp_list = ft.get_all_lines(user_dic)
    print(nnp_list[1])

    add_nnp = ft.get_all_lines(add_dic)
    print(add_nnp[0])

    has_coda_list = []
    for word in add_nnp:
        if has_coda(word):
            has_coda_list.append('F')
        else:
            has_coda_list.append('T')

    for word, coda in zip(add_nnp, has_coda_list):
        dic_word = word + f',,,,NNP,*,{coda},{word},*,*,*,*,*'
        nnp_list.append(dic_word)

    ft.write_list_file(nnp_list,'/usr/local/lib/mecab/dic/mecab-ko-dic-20180720/user-dic/nnp.csv')


if __name__ == '__main__':
    main()