from flask import Flask, jsonify
import math
import re

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

def load_vocabs():
    vocab={}
    with open(r'tf-idf\\frequencies.txt', 'r') as f:
        idf_values = f.readlines()
    with open(r'tf-idf\\tokens.txt', 'r') as f:
        vocab_terms = f.readlines()
        vocab_terms= vocab_terms

        for (term,idf_value) in zip(vocab_terms, idf_values):
            vocab[term.strip().lower()] = int(idf_value.strip())
        return vocab



def document():
    with open(r'Qdata\index.txt', 'r') as f:
         documents= f.readlines()
         #line = doc.split().strip()[1:]
    documents = [document.strip().split()[1:] for document in documents]

    return documents

def links():
    with open(r'Qdata\Qindex.txt', 'r') as f:
          fol= f.readlines()
         #line = doc.split().strip()[1:]

    return fol

def inverted_document():
    inverted_document = {}
    with open(r'Qdata\index.txt', 'r') as f:
        terms = f.readlines()
    for doc_id, term in enumerate(terms):
        term = term.lower().split()[1:]
        for i in term:
            if i not in inverted_document:
                inverted_document[i] = [doc_id]
            else:
                inverted_document[i].append(doc_id)
    
    return inverted_document



vocab_idf_values = load_vocabs()
documents = document()
inverted_index = inverted_document()
link_part = links()


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values


def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])





def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])





def final_doc(query_terms):
    potential_documents = {}
    result = []

    for term in query_terms:
        idf = get_idf_value(term)
        if idf == 0:
            continue

        tf = get_tf_dictionary(term)

        for document in tf:
            if document not in potential_documents:
                potential_documents[document] = tf[document] * idf
                potential_documents[document] += tf[document] * idf

    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    for document_index in potential_documents:
        result.append(link_part[int(document_index)])
    
    return result


        #print('Document: ', documents[int(document_index)], ' Score: ', potential_documents[document_index])



#query_string = input('Enter your query: ')
#query_terms = [term.lower() for term in query_string.strip().split()]

#print(query_terms)
#final_doc(query_terms)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(final_doc(q_terms)[:20:])


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = final_doc(q_terms)[:10:]
    return render_template('index.html', form=form, results=results)

