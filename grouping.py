import pandas as pd
import re,collections,nltk
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.mlab as mlab  
import matplotlib.pyplot as plt  
from matplotlib import font_manager as fm
from  matplotlib import cm
import sys
import warnings
warnings.filterwarnings("ignore") 

path = sys.argv[1]
corpus = pd.read_csv(path+'/text.csv',header=0)

stop_words = set(stopwords.words('english'))
lmtzr = WordNetLemmatizer()

# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    #new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''

def merge(words):
    new_words = []
    for word in words:
        if word:
            tag = nltk.pos_tag(word_tokenize(word)) # tag is like [('bigger', 'JJR')]
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    return new_words

def append_ext(words):
    new_words = []
    for item in words:
        word, count = item
        tag = nltk.pos_tag(word_tokenize(word))[0][1] # tag is like [('bigger', 'JJR')]
        new_words.append((word, count, tag))
    return new_words


frequency = {}
ps = PorterStemmer()
week = 0
topic_idx = {}
topics_everyweek = []
for index, row in corpus.iterrows():
    words_box=[]
    pat = re.compile(r'[^a-zA-Z \']+')
    words_box.extend(merge(replace_abbreviations(row[1]).split()))

    words_box = [word for word in words_box if word not in stopwords.words('english')]
    words = collections.Counter(words_box)
    total_count = sum(words.values())
    freq_sub = {}
    for w in words.elements():
        freq_sub[w] = words[w]/total_count+1

    label = row[0].lower()
    topic_idx[label]=index
    frequency[label] = freq_sub


query = pd.read_csv(path+'/questions.csv',header=0)


result = []
for index,row in query.iterrows():
    words_box=[]
    pat = re.compile(r'[^a-zA-Z \']+')
    words_box.extend(merge(replace_abbreviations(row[0]).split()))
    words_box = [word for word in words_box if word not in stopwords.words('english')]
    res = []
    output = {}
    for topic,freq in frequency.items():
        prob = 1
        for w in words_box:
            if w in freq.keys():
                prob = prob*freq[w]
            output[topic]=prob
    for key,value in output.items():
        if(value == max(output.values())):
            res.append(key)
    res = list(set(res))
    result.append(res[0])
label_q = pd.DataFrame(result)
label_q.columns = ['labels']
output_csv = pd.concat([query,label_q], axis=1)
output_csv.to_csv(path+'/grouping_output.csv',index=False,header=True)

count_labels = collections.Counter(result)
plot_lables = []
plot_count = []
for l,c in count_labels.items():
    plot_lables.append(l)
    plot_count.append(int(c))
plot_lables = pd.DataFrame(plot_lables)
plot_count = pd.DataFrame(plot_count)
plot_file = pd.concat([plot_lables,plot_count], axis=1)
plot_file.columns = ['labels','count']
plot_file.sort_values(by="count" , ascending=False,inplace=True)
plot_file.to_csv(path+'/counter_topics.csv',index=False,header=True)


fig, axes = plt.subplots(figsize=(20,10),ncols=2) 
ax1, ax2 = axes.ravel()

colors = cm.rainbow(np.arange(len(plot_file['count']))/len(plot_file['count'])) # colormaps: Paired, autumn, rainbow, gray,spring,Darks
patches, texts, autotexts = ax1.pie(plot_file['count'], labels=plot_file['labels'], autopct='%1.0f%%',
        shadow=False, startangle=170, colors=colors)

ax1.axis('equal')  

proptease = fm.FontProperties()
proptease.set_size('x-large')
# font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
plt.setp(autotexts, fontproperties=proptease)
plt.setp(texts, fontproperties=proptease)

ax1.set_title('Distribution of Question Topics', loc='center')

ax2.axis('off')
ax2.legend(patches, plot_file['labels'], loc='center left')

plt.tight_layout()
plt.savefig(path+'/Distribution of Question Topics.svg', format="svg",transparent=True)