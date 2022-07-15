from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import numpy as np
import csv

filename = "zoomg.csv"

fields = []
rows = []

docs = []
Data = []

with open(filename, 'r',encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        Data.append(row)
        docs.append(row[1])

    print("Total no. of rows: %d" % (csvreader.line_num))



vectorizer = TfidfVectorizer()
tfidf_docs = vectorizer.fit_transform(docs)
while True:
    query = input("query:")

    tfidf_query = vectorizer.transform([query])[0]

    cosines = []
    for d in tqdm(tfidf_docs):
      cosines.append(float(cosine_similarity(d, tfidf_query)))

    Result_num = 10
    sorted_ids = np.argsort(cosines)
    for i in range(Result_num):
        cur_id = sorted_ids[-i - 1]
        print(docs[cur_id],'\n', cosines[cur_id] ,'\n', Data[cur_id][2] , '\n-----------------------------------------------------------------------' )
