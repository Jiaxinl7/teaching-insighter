from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh import index
import os, os.path
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser
import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings("ignore")


schema = Schema(content_id=ID(stored=True), lesson=NUMERIC(stored=True), topic=TEXT(stored=True), content=TEXT(stored = True))

# create empty index directory

if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

df = pd.read_csv("text.csv")
i = 0
new_list = []

for _, row in df.iterrows():
    all_sentence = str(row["TEXT"]).split('.')
    for sentence in all_sentence:
        content_id = i
        i += 1
        lesson = row["Lesson"]
        topic = row["Topic"]
        content = sentence
        if content != "":
            while content[0] == ' ':
                content = content[1:]
            temp = [content_id, lesson, topic, content]
            new_list.append(temp)

for row in new_list:
    content_id = row[0]
    lesson = row[1]
    topic = row[2]
    content = row[3]
    writer.add_document(content_id=str(content_id), lesson=str(lesson), topic=str(topic), content=str(content))
writer.commit()

result_list = []

def index_search(dirname, search_fields, search_query):
    ix = index.open_dir(dirname)
    schema = ix.schema

    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(search_fields, schema, group = og)


    q = mp.parse(search_query)


    with ix.searcher() as s:
        results = s.search(q, terms=True, limit = 5)
#         print("Search Results: ")
        if results.is_empty():
            result_list.append("")
        else:
            result_list.append(results[0]['content'])
        return results

questions = pd.read_csv("questions.csv")
all_result = []
for _, row in questions.iterrows():
    index_search("index_dir", ['topic', 'content'], row["questions"])

questions['answer'] = result_list
questions.to_csv('questions.csv')
