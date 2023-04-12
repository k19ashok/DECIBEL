import tempfile
import requests
import json
from gensim import corpora
from gensim import similarities
import re
import string
from nltk.stem import WordNetLemmatizer
import spacy
from django.http import HttpResponse
from django.shortcuts import render
from django.http import request
from io import BytesIO
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
import os


def home(request):
    return render(request, 'index.html')


nlp = spacy.load('en_core_web_lg')


def lemmatize(s):
    lemmatizer = WordNetLemmatizer()
    l = []
    for i in s.split():
        l.append(lemmatizer.lemmatize(i))
    return ' '.join(l)


# Remove Punctuations and make the string lowercase
def task1(s):
    s = [i for i in s.split() if not i.isdigit(
    ) and not i in string.punctuation and i not in ['a', 'an', 'the']]
    return lemmatize(' '.join(s))


# Build Spacy Doc Object and Tokenize
def task2(s):
    doc = nlp(s)
    tokens = []
    l = [i.text for i in doc.noun_chunks]
    noun_chunks = []
    for c in l:
        x = c.split(' ')
        if len(x) > 2:
            for j in range(1, len(x)):
                if nlp(' '.join(x[:j])).similarity(nlp(' '.join(x[j:]))) < 0.65:
                    noun_chunks.append(' '.join(x[:j]))
                    noun_chunks.append(' '.join(x[j:]))
                    break
            else:
                noun_chunks.append(c)
        else:
            noun_chunks.append(c)

    for token in doc:
        if token.is_stop:
            continue
        p = re.compile(re.escape(token.text))
        for i in noun_chunks:
            if re.search(p, i):
                if i not in tokens:
                    tokens.append(i)
                break
        else:
            tokens.append(token.text)
    return tokens


s = ''

# VIDEOS_PATH = "C:\\Users\k19as\Desktop\Projects\Decibel\Ashok\Videos"
# FILENAMES_PATH = "C:\\Users\k19as\Desktop\Final\\filenames.txt"


# def getFileNames():
#     filenames = []
#     with open(FILENAMES_PATH) as f:
#         for i in f.read().split('\n'):
#             filenames.append(i)
#     return filenames


def get_similar(tokens):
    files = list(video_names.keys())
    dictionary = corpora.Dictionary([text.split() for text in files])

    # Preprocess the input sentence and convert it to a BoW representation
    s = 'labour union is playing with cricket ball'
    result = []
    for i in tokens:
        s = dictionary.doc2bow(i.split())

        corpus = [dictionary.doc2bow(text.split()) for text in files]
        index = similarities.MatrixSimilarity(
            corpus, num_features=len(dictionary))
        sims = index[s]

        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        result.append(files[sorted_sims[0][0]])
    return result
#     for i, sim in sorted_sims[:3]:
#         print(f'Similarity with file {i}, {files[i]}: {sim}')


def getfinal(tokens, result):
    out = []
    for i in range(len(tokens)):
        x = nlp(tokens[i])
        y = nlp(result[i])
        if x.similarity(y) > 0.7:
            out.append(y.text)
        else:
            out.extend(tokens[i])

#         x = tokens[i].split()
#         y = result[i].split()

#         for j in x:
#             if j not in y:
#                 print(j)
#                 out.extend(list(j))
#             elif ' '.join(y) not in out:
#                 out.append(' '.join(y))
    return out


result_video_names = []


def getSigns(request):
    s = request.POST['input_text']
    tokens = task2(task1(s))
    print(tokens)
    result = get_similar(tokens)
    print(result)
    result_video_names = getfinal(tokens, result)
    print(result_video_names)
    final_video = downloadVideo(result_video_names)
    return final_video
    # return HttpResponse(f'<h1>{result_video_names}</h1>')


with open('C:\\Users\k19as\Desktop\Final\WEB\DECIBEL\static\\file_ids.json') as f:
    video_names = json.loads(f.read())

def downloadVideo(result_video_names):

    import cv2
    import numpy as np
    videos = []
    for i in result_video_names:
        file_id = video_names.get(i, '')
        if not file_id:
            continue

        # Replace with the file URL you want to download
        file_url = "https://drive.google.com/uc?export=download&id={file_id}"


        # Send a GET request to the file URL
        response = requests.get(file_url)

    np_data = np.frombuffer(response.content, dtype=np.uint8)

    # Decode the numpy array into an OpenCV frame
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    # Create a VideoCapture object from the OpenCV frame
    cap = cv2.VideoCapture()
    cap.open(frame)
    return frame