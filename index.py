import argparse
import os
import string
import json
import timeit

import nltk
from nltk import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import sent_tokenize

'''
get the ordered file list in the folder
input file name
return ordered list
'''

nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

def get_docIDs(folder_of_documents):
    doctIDs = []
    dirs = os.listdir(folder_of_documents)
    if dirs:
        for item in dirs:
            doctIDs.append(item)
            doctIDs.sort()
    return doctIDs


def index(folder_of_documents, folder_of_indexes):
    # inverted_index = {}
    positional_index = {}
    docIDs = get_docIDs(str(folder_of_documents))
    token_size = []
    # get file contents
    # to split doc into sentences
    for docID in docIDs:
        pos_in_doc = -1
        doc_path = os.path.join(str(folder_of_documents), str(docID))
        file = open(doc_path)
        doc = file.readlines()
        start = 0
        temp_doc = []
        new_doc = []
        # split doc and strip indentation
        for index, line in enumerate(doc):
            if len(doc) == 1:
                temp_doc.append(doc[0].strip())
            else:
                if line.startswith("    "):
                    temp_doc.append(" ".join(x.strip() for x in doc[start:index]))
                    start = index
                if index == len(doc) - 1:
                    temp_doc.append(" ".join(x.strip() for x in doc[start:index]))

        for d in temp_doc:
            new_doc.extend(sent_tokenize(d))
        file.close()

        #  preprocessing
        # define lemmatizer
        lemma = WordNetLemmatizer()

        for sentence_index, str1 in enumerate(new_doc):
            # search is case-insensitive
            # full stops for abbreviations are ignored(strs are separate sentences)
            str1 = str1.lower().replace(".", "")
            no_digit_str = []
            for i in str1:
                # a sentence can only end with a full stop, a question mark, an exclamation mark
                # replace all punctuations except "'" with blank
                if i != "'" and i in string.punctuation:
                    str1 = str1.replace(i, " ")
            str1 = str1.split()
            for j in str1:
                # all numeric tokens are ignored
                if not j.isdigit():
                    no_digit_str.append(j)
            new_sentence = []
            pos = pos_tag(no_digit_str)

            # According to pos_tag, if after removing "'...", the left part is "N"
            # we only need to keep the left part
            # in the other situation, the "'" is defined as punctuation
            for item in pos:
                if item[1][0] != "N" and "'" in item[0]:
                    new_sentence.append(item[0].replace("'", " "))
                    continue
                else:
                    if item[1][0] == "N" and "'" in item[0]:
                        new_token = item[0].replace("'", " ").split()
                        temp_pos = pos_tag([new_token[0]])
                        a = temp_pos[0][1][0]
                        if temp_pos[0][1][0] == "N":
                            new_sentence.append(new_token[0])
                            continue
                        else:
                            new_sentence.append(item[0].replace("'", " "))
                            continue
                new_sentence.append(item[0])

            # do lemmatize according to words' pos_tag
            new_str = ' '.join(x for x in new_sentence)
            new_str = new_str.split()
            pos = pos_tag(new_str)
            # singular/plural is ignored
            single_sentence = []
            for word in pos:
                if word[1][0] == "N" and word[0] != "ios":
                    single_sentence.append(lemma.lemmatize(word[0], "n"))
                    continue
                single_sentence.append(word[0])
            # Tense is ignored
            lem_sentence = []
            pos = pos_tag(single_sentence)
            for word in pos:
                lem_sentence.append(lemma.lemmatize(word[0], "v"))

            for index_in_sentence, term in enumerate(lem_sentence):
                pos_in_doc += 1
                if term not in positional_index.keys():
                    positional_index[term] = [[docID, [(pos_in_doc, sentence_index)]]]
                else:
                    if docID == positional_index[term][len(positional_index[term])-1][0]:
                        positional_index[term][len(positional_index[term])-1][1].append((pos_in_doc, sentence_index))
                    else:
                        positional_index[term].append([docID, [(pos_in_doc, sentence_index)]])
            token_size.append(len(lem_sentence))



    # store index
    os.mkdir(str(folder_of_indexes))
    with open(str(folder_of_indexes) + '/' + "positional index.json", 'w') as f:
        json.dump(positional_index, f)
    f.close()


    print(f"Total number of documents: {len(docIDs)}")
    print(f"Total number of tokens: {sum(token_size)}")
    print(f"Total number of terms: {len(positional_index)}")


'''
prints the proper command usage
'''

parser = argparse.ArgumentParser(
    description='Index data for boolean retrieval')
parser.add_argument('input_path', help='Directory for documents to be indexed')
parser.add_argument('output_path', help='Output indexes json')
args = parser.parse_args()

# Get arguments
folder_of_documents = args.input_path
folder_of_indexes = args.output_path

index(folder_of_documents, folder_of_indexes)