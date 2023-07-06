

import os
import re

qData_folder = "Qdata"

target_str = "Example 1:"

all_lines = []

for i in range(1, 692):
    file_path = os.path.join(qData_folder, "{}/{}.txt".format(i, i))

    doc = ""
    with open(file_path, "r", encoding= 'utf-8', errors = "ignore") as f:
        lines = f.readlines()
    
    for line in lines:
        if target_str in line:
            break
        else:
            doc += line
    
    all_lines.append(doc)


def preprocess(text):      # remove problem no, and return a list of lowercase words
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)      # removing non alphanumeric chars
    terms = [term.lower() for term in text.strip().split()]

    return terms

vocab = {}          # word : no of docs that word is present in
documents = []      # all lists, with each list containing words of a document

for (index, line)  in enumerate(all_lines):
    tokens = preprocess(line)       #list of processed words of this doc
    documents.append(tokens)

    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

#reverse sort vocab by values (by the no of docs the word is present in)
vocab = dict( sorted(vocab.items(), key = lambda item : item[1], reverse = True) )


print("No of documents : ", len(documents))
print("Size of vocab : ", len(vocab))
print("Sample document: ", documents[100])

# keys of vocab thus is a set of distinct words across all docs
# save them in file vocab
with open(r"tf-idf\tokens.txt", "w", encoding = 'utf-8', errors = "ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

# save idf values
with open(r"tf-idf\frequencies.txt", "w", encoding = 'utf-8', errors = "ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])













doc= []

with open("Qdata\index.txt", "r") as file:
        # Read each line one by one
        for line in file:
            line = line.split()[1:]
            doc.append(line)




count = {}



for index, sentence in enumerate(doc):
    for token in sentence:
        if token not in count:
            count[token] = 1
        else:
            count[token] += 1




inverted_index = {}



with open(r'Qdata\index.txt', 'r') as file:
    # Read the contents of the file and populate the doc_collection list
    doc_collection = file.readlines()

inverted_index = {}

for doc_id, document in enumerate(doc_collection):
    # Split the document into terms
    terms = document.lower().split()

    for term in terms:
        if term not in inverted_index:
            inverted_index[term] = [doc_id]
        else:
            inverted_index[term].append(doc_id)


with open('inverted_index.txt', 'w') as file:
    for value, vector in inverted_index.items():
        file.write(f"{value} : {vector}\n")
