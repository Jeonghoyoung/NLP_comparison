import pandas as pd
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
import math


def word_score(score):
    return score.cohesion_forward * math.exp(score.right_branching_entropy)


df1 = pd.read_csv('../data/test_100.csv')

word_extractor = WordExtractor(min_cohesion_forward=0.05,
                               min_right_branching_entropy=0.0)
model1 = word_extractor.load('../wordextractor_default_params_149900.model')
words1 = word_extractor.extract(model1)

cohesion_scores1 = {word: word_score(score) for word, score in
                    words1.items()}
l_tokenizer1 = LTokenizer(scores=cohesion_scores1)
l_tok_corpus1 = [l_tokenizer1.tokenize(sent) for sent in df1['tgt']]
print(len(l_tok_corpus1))
print(l_tok_corpus1[0])


model2 = word_extractor.load('../wordextractor_default_params.model')
words2 = word_extractor.extract(model2)

cohesion_scores2 = {word: word_score(score) for word, score in
                    words2.items()}
l_tokenizer2 = LTokenizer(scores=cohesion_scores2)
l_tok_corpus2 = [l_tokenizer2.tokenize(sent) for sent in df1['tgt']]

print(len(l_tok_corpus2))
print(l_tok_corpus2[0])

soy_df = pd.DataFrame({'small_train': l_tok_corpus1,
                       'large_train': l_tok_corpus2})

soy_df.to_excel('../soynlp_train_dataset_comparison.xlsx', index=False)