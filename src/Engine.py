## 3. Import Packages
import re
import numpy as np
import pandas as pd
from pprint import pprint
import networkx as nx

import json

####La7S<AB?5_H=ObFmIo{


# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.test.utils import datapath

# Let's go get our friend WikiRelate:
#from folder.wikirelate as wikirelate

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this


# MySQL Import
import pymysql

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)


## 5. Prepare Stopwords
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'timestamp', 'com', 'http', 'www'])


## 6. Import Newsgroups Data
# Import Dataset
connection = pymysql.connect(host='127.0.0.1', user='root', password='5TRcaSeTr4L', db='Twitter')


##
#
#df = pd.read_csv('abcnews-reduced.csv', dtype=str, usecols=[1])

Tweets_df = pd.read_sql('SELECT * FROM Tweets', con=connection)

#print(Tweets_df.iloc[:,0]) #Random IDs
#print(Tweets_df.iloc[:,1]) #Tweet Text Content
#print(Tweets_df.iloc[:,2]) #Timestamps
#print(Tweets_df.iloc[:,3]) #User IDs

UserIdList = Tweets_df.iloc[:,3].tolist()
UserIdString = str(UserIdList)
UserIdString = UserIdString[1:-1]

#print(UserIdString)



Users_df = pd.read_sql(('SELECT * FROM Users WHERE Id IN ('+UserIdString+')'), con=connection)



#print(Users_df.iloc[:,1])



data = Tweets_df.iloc[:,1].tolist()
#pprint(data[:1])


    ## 8.Tokenize document in GenSim modifiable tokens.
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(data))
#print(data_words[:1])


    ## 9. Creating Bigram and Trigram Models
    # Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

    ## 10. Remove Stopwords, Make Bigrams and Lemmatize
    # Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

    # Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[u'NOUN', u'ADJ', u'VERB', u'ADV'])

print(data_lemmatized[:1])

    ## 11. Create the Dictionary and Corpus needed for Topic Modeling
    # Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
texts = data_lemmatized

    # Create corpus bag of words
corpus = [id2word.doc2bow(text) for text in texts]

    # Human readable format of corpus (term-frequency)
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]

    ## 12. Building Topic Model (LDA)
    # Build LDA model
load_file = datapath("C:\\Users\\Trent Rand\\Documents\\edp-eb05\\edp-eb05-master\\Models\\TweetsLdaModel")
lda_model = gensim.models.ldamodel.LdaModel.load(load_file)


    # Print the Keyword in the 10 topics
pprint(lda_model.get_topics())
doc_lda = lda_model[corpus]

#pprint(doc_lda)


ndarray = lda_model.get_topics()
pprint(ndarray)


nameList = lda_model.get_topic_terms(2)
pprint(nameList)


user_topic_edges = [(0,0),(0,1),(1,1)]

#For each lemmatized tweet:
ind = 0;
for doc in data_lemmatized:
    q_vec = id2word.doc2bow(doc)
    #pprint(q_vec)

    #Fetch the topic of each tweet, in order to pair it with a UserId.
    topic_vec = lda_model.get_document_topics(q_vec)

    topic_prob = 0;
    topic_id = -1;
    for pair in topic_vec:
        prob = pair[1]
        id = pair[0]

        if prob > topic_prob:
            topic_prob = prob
            topic_id = id



    #pprint(topic_vec)

    user_id = UserIdList[ind]

    user_topic_edges.append((topic_id, user_id))

    ind = ind + 1;



G = nx.Graph()
#G.add_nodes_from(data)
G.add_nodes_from(UserIdList)
G.add_edges_from(user_topic_edges)

nx.draw(G)


nx.write_edgelist(G, "test1.edgelist", data=True)
graphJSONData = nx.readwrite.node_link_data(G)


# We made it here, we can go anywhere
# "Don't put song lyrics in the comments" -Ron, probably.

# wikirelate was here

topicModel = Word2Vec.load_word2vec_format('conceptEmbeddings.bin.gz', binary=True)



t = 0;
for topic in np.nditer(ndarray):

    tsg.add_node(t)
        #This isn't what a Try/Catch is for, dummy. This is embarassing. You're better than this.
    try:
        topicTermsA = lda_model.show_topic(t)
        topicTermsB = lda_model.show_topic(t + 1)

        distance = topicModel.wmdistance(topicTermsA, topicsTermsB)

        tempEdge = (t, t + 1, {'weight':distance})

        topic_topic_edges.append(tempEdge)
    except:
        #Pathetic.
        print("End of Topics!")

tsg.add_weighted_edges_from(topic_topic_edges)
topicGraphJSONData = nx.readwrite.node_link_data(G)
json.dump(topicGraphJSONData, 'topicGraph.json')
