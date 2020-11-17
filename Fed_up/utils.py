import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer
from recipe import get_data

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

def remove_punctuation(col_to_change):
    # Remove the punctuation of a string
    return ''.join([i for i in col_to_change if i not in string.punctuation])


def lower_case(col_to_change):
    # Put each word of a string in lower case
    return col_to_change.lower()


def remove_numbers(col_to_change):
    # Remove the numbers of a String
    return ''.join(character for character in col_to_change if not character.isdigit())


def removes_stopwords(col_to_change, language='english'):
    # Remove the most commun words of String - Need to specify a language
    stop_words = set(stopwords.words(language))
    word_tokens = word_tokenize(col_to_change)
    col_to_change = [word for word in word_tokens if not word in stop_words]
    return col_to_change


def word_lemmatizer(col_to_change):
    # Lemmatize the words of the String.
    lemmatize = [WordNetLemmatizer().lemmatize(word) for word in col_to_change]
    return ' '.join(word for word in lemmatize)


def cleaning_strings(df_series, remove_punc=True, lower_c=True, remove_num=True, remove_stopw=True, language='english', word_lemmatize=False):
    # Calling each function if paramter(s) is(are) True
    df_series = df_series.fillna("")  ## => Handling if Na inside the Pandas series.

    if remove_punc:
        df_series = df_series.apply(remove_punctuation)
    if lower_c:
        df_series = df_series.apply(lower_case)
    if remove_num:
        df_series = df_series.apply(remove_numbers)
    if remove_stopw:
        df_series = df_series.apply(removes_stopwords, language=language)
    if word_lemmatize:
        df_series = df_series.apply(word_lemmatizer)

    return df_series


if __name__ == "__main__":
    data = get_data().head(100)
    columns = ['steps', 'description', 'tags', 'ingredients']
    #print(data.info())
    print("")
    print("********************")

    for column in columns:
        #print(type(data[column]))
        #import ipdb; ipdb.set_trace()
        data[column] = cleaning_strings(data[column])


    print(data[columns].head(50))
