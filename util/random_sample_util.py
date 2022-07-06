import os
import pandas as pd
import random
import util.file_util as ft


def get_txt_to_df(path, src_lang:str):
    file_list = os.listdir(path)

    domain = []
    src_list = []
    tgt_list = []

    for file in file_list:
        if file.split('.')[1] == src_lang:
            file_name = file.split('_')[3]
            src_text_list = ft.get_all_lines(f"{path}/{file}")

            for src_text in src_text_list:
                src_list.append(src_text)
                domain.append(file_name)

        else:
            tgt_text_list = ft.get_all_lines(f"{path}/{file}")
            for tgt_text in tgt_text_list:
                tgt_list.append(tgt_text)

    df = pd.DataFrame({
        'domain' : domain,
        'src' : src_list,
        'tgt' : tgt_list
    })

    return df


def read_tab_file(input_path):
    df = pd.read_csv(input_path, sep='\t',error_bad_lines=False)
    df.columns = ['src', 'tgt']
    return df


def random_sampling_path(input_path, src_lang='en', random_seed=123, sample_num=100):
    random_seed = random_seed
    sample_num = sample_num

    df = get_txt_to_df(input_path, src_lang=src_lang)

    random.seed(random_seed)
    random_sample_index = random.sample(range(0, len(df)), sample_num)

    df_sample = df.loc[random_sample_index]
    df_sample.reset_index(inplace=True, drop=True)

    return df_sample


def random_sampling(df, random_seed:int, sample_num:int, data:str):
    random.seed(random_seed)
    random_sample_index = random.sample(range(len(df)), sample_num)

    if data == 'train':
        result_df = df.drop(random_sample_index)
        result_df.reset_index(inplace=True, drop=True)
    elif data == 'test':
        result_df = df.loc[random_sample_index]
        result_df.reset_index(inplace=True, drop=True)

    return result_df


def random_sampling_df(input_path, random_seed:int, sampling_num:int, data:str):
    df = read_tab_file(input_path)
    random.seed(random_seed)
    random_sample_index = random.sample(range(len(df)), sampling_num)

    if data == 'train':
        result_df = df.drop(random_sample_index)
        result_df.reset_index(inplace=True, drop=True)
    elif data == 'test':
        result_df = df.loc[random_sample_index]
        result_df.reset_index(inplace=True, drop=True)

    return result_df
