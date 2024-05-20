# -*- coding: utf-8 -*-
"""copy 1 of NLP Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lNtqiogRr4QpdSNgwAXiNvVA00H_vIlK
"""

from getpass import getpass
import os

! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

!kaggle competitions download shai-training-2024-a-level-2

!unzip shai-training-2024-a-level-2.zip

#Importing necessary libraries
import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))
import spacy
import scipy
import string
import seaborn as sns
nltk.download('punkt')
nltk.download('wordnet')
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

#Reading the dataset
df = pd.read_csv("/content/Train.csv")
df.head()

"""# **Exploring Data**"""

df.info()

# Checking for missing values

df.isnull().values.any()

df['label'].value_counts()

sns.countplot(x='label', data=df)

"""# **Text Preprocessing**"""

#removing punctuation
df['text'] = df['text'].str.replace('[^\w\s]','')
df['text'] = df['text'].str.replace('/><br','')
df['text'] = df['text'].str.replace("-", "")

df['text'][0]

#applying stopwords removal
def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])
df["text"] = df["text"].apply(stopwords)

df['text'][0]

#removing urls
df['text'] = df.text.replace(regex = {r'<p>': ' ', r'</p>': '', r'<a.*?\/a>': '+'})

df['text'][0]

#toknize text
df['text'] = df.apply(lambda row: nltk.word_tokenize(row['text']), axis=1)

df['text'][0]

df['text'] = df['text'].astype(str)

df['text'][0]

#apply lemmatization
from nltk.stem import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

df['text'] = df['text'].apply(lambda text: ' '.join([lmtzr.lemmatize(word) for word in nltk.word_tokenize(text)]))

tfidf_vectorizer = TfidfVectorizer()

tfidf_vectorizer.fit(df['text'])

chunk_size = 1000
chunks = [df['text'][i:i + chunk_size] for i in range(0, len(df), chunk_size)]

x_vec = None

# Fit the vectorizer on each chunk and concatenate
for chunk in chunks:
    chunk_vec = tfidf_vectorizer.transform(chunk)
    if x_vec is None:
        x_vec = chunk_vec
    else:
        x_vec = scipy.sparse.vstack([x_vec, chunk_vec])

x_train,y_train=x_vec,df['label']

df_v=pd.read_csv('/content/Valid.csv')

df_v

df_v['text'] = df_v['text'].str.replace('[^\w\s]','')
df_v['text'] = df_v['text'].str.replace('/><br','')
df_v['text'] = df_v['text'].str.replace("-", "")

#applying stopwords removal
def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])
df_v["text"] = df_v["text"].apply(stopwords)

#removing urls
df_v['text'] = df_v.text.replace(regex = {r'<p>': ' ', r'</p>': '', r'<a.*?\/a>': '+'})

#toknize text
df_v['text'] = df_v.apply(lambda row: nltk.word_tokenize(row['text']), axis=1)

df_v['text'] = df_v['text'].astype(str)

#apply lemmatization

df_v['text'] = df_v['text'].apply(lambda text: ' '.join([lmtzr.lemmatize(word) for word in nltk.word_tokenize(text)]))

x_vald=tfidf_vectorizer.transform(df_v.text)

y_vald=df_v.label

"""##  Naive Bayes Model"""

nvb= MultinomialNB()

nvb.fit(x_train, y_train)

nvb_pre=nvb.predict(x_vald)

precision, recall, fscore, support = score(y_vald, nvb_pre)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-score: {fscore}")
print(f"Support: {support}")

accuracy_nvb, conf_matrix1 = accuracy_score(y_vald, nvb_pre), confusion_matrix(y_vald, nvb_pre)

print({'accuracy_nvb=':accuracy_nvb})

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = conf_matrix1, display_labels = [0, 1])

cm_display.plot()
plt.show()

"""# Logestic Regression Model"""

model = LogisticRegression()
model.fit(x_train, y_train)

log_pre=model.predict(x_vald)

accuracy_log = accuracy_score(y_vald, log_pre)
print(f"Accuracy: {accuracy_log:.2f}")

conf_matrix3 = confusion_matrix(y_vald, log_pre)

cm_display3 = metrics.ConfusionMatrixDisplay(confusion_matrix = conf_matrix3, display_labels = [0, 1])

cm_display3.plot()
plt.show()

"""# Support Vector Model"""

# Create and train the SVM model
model2 = SVC(kernel='linear')  # Linear kernel for binary classification
model2.fit(x_train, y_train)

# Make predictions on the test data
svc_pre = model2.predict(x_vald)

# Evaluate accuracy
accuracy_svc = accuracy_score(y_vald, svc_pre)
print(f"Accuracy: {accuracy_svc:.2f}")

conf_matrix4=confusion_matrix(y_vald,svc_pre)

cm_display4 = metrics.ConfusionMatrixDisplay(confusion_matrix = conf_matrix4, display_labels = [0, 1])

cm_display4.plot()
plt.show()

df_t=pd.read_csv('/content/Test.csv')

df_t

df_t['text'] = df_t['text'].str.replace('[^\w\s]','')
df_t['text'] = df_t['text'].str.replace('/><br','')
df_t['text'] = df_t['text'].str.replace("-", "")

def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])
df_t["text"] = df_t["text"].apply(stopwords)

df_t['text'] = df_t.text.replace(regex = {r'<p>': ' ', r'</p>': '', r'<a.*?\/a>': '+'})

df_t['text'] = df_t.apply(lambda row: nltk.word_tokenize(row['text']), axis=1)

df_t['text'] = df_t['text'].astype(str)

df_t['text'] = df_t['text'].apply(lambda text: ' '.join([lmtzr.lemmatize(word) for word in nltk.word_tokenize(text)]))

xt=tfidf_vectorizer.transform(df_t['text'])

yt_pred_nb = model.predict(xt)

yt_pred_nb

df_sub=pd.read_csv('/content/sample_submission.csv')

df_sub

df_sub['label']=yt_pred_nb

df_sub.to_csv('nlp4.csv',header=True,index=False)