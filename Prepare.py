
doc= []

with open("Qdata\index.txt", "r") as file:
        # Read each line one by one
        for line in file:
            line = line.split()[1:]
            doc.append(line)
print(doc)



count = {}



for index, sentence in enumerate(doc):
    for token in sentence:
        if token not in count:
            count[token] = 1
        else:
            count[token] += 1

with open(r'tf-idf\tokens.txt', 'w') as token_file, open(r'tf-idf\frequencies.txt', 'w') as freq_file:
    for token, frequency in count.items():
        token_file.write(f"{token}\n")
        freq_file.write(f"{frequency}\n")



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

print(inverted_index)

with open('inverted_index.txt', 'w') as file:
    for value, vector in inverted_index.items():
        file.write(f"{value} : {vector}\n")
