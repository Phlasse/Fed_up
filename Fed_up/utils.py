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


def cleaning_strings(element, remove_punctuation=True, lower_case=True, remove_numbers=True, removes_stopwords=True, language='english', word_lemmatizer=False):
    if remove_punctuation:
        element = remove_punctuation(element)
    if lower_case:
        element = lower_case(element)
    if remove_numbers:
        element = remove_numbers(element)
    if removes_stopwords:
        element = removes_stopwords(element, language)
    if word_lemmatizer:
        element = word_lemmatizer(element)

    return element



if __name__ == "__main__":
    data = get_data()
    columns = ['steps', 'description', 'tags', 'ingredients']

    print("")
    print("********************")

    for column in columns:
        import ipdb; ipdb.set_trace()
        #data[column] = data[column].map(cleaning_strings)
        data[column] = data[column].apply(remove_punctuation)

    print(data.head())
