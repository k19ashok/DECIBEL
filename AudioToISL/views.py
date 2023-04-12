import tempfile
import requests
import json
from gensim import corpora
from gensim import similarities
import re
import string
from nltk.stem import WordNetLemmatizer
import spacy
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.http import request
import django.http
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


# Remove Punctuations and digits and make the string lowercase
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
        stop_words = ["am","are","is","was","were","be","being","been","have","has","had",\
                  "does","did","could","should","would","can","shall","will","may","might","must","let"]
        print(token)
        if token.text in stop_words:
            continue
        p = re.compile(re.escape(token.text))
        for i in noun_chunks:
            if re.search(p, i):
                if i not in tokens:
                    tokens.append(i)
                break
        else:
            tokens.append(token.text)
        print(token,tokens)
    return tokens


VIDEOS_PATH = "C:\\Users\k19as\Desktop\Projects\Decibel\Ashok\Videos"
FILENAMES_PATH = "C:\\Users\k19as\Desktop\Final\\filenames.txt"


def getFileNames():
    filenames = []
    with open(FILENAMES_PATH) as f:
        for i in f.read().split('\n'):
            filenames.append(i)
    return filenames


def get_similar(tokens):
    files = list(getFileNames())
    dictionary = corpora.Dictionary([text.split() for text in files])

    # Preprocess the input sentence and convert it to a BoW representation
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
            out.append(list(tokens[i]))

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

import speech_recognition as sr
from pydub import AudioSegment
import soundfile


def getTextFromAudio(file):
    print(file)
    # Open the MP3 file using pydub
    
    r = sr.Recognizer()
    print('Recognizing')
    data, samplerate = soundfile.read(file)
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
    with sr.AudioFile('new.wav') as source:
        audio_data = r.record(source) 
    text = r.recognize_google(audio_data)
    print(text)
    return text


VIDEOS_PATH = "C:\\Users\k19as\Desktop\Projects\Decibel\A\\Videos"

def getSigns(request):
    # s = request.POST['input_text']
    try:
        file = request.FILES['audio-file']
        if not file:
            return HttpResponse('<h1>Invalid file</h1>')
        with open('audio.mp3','wb') as f:
            for chunk in file.chunks():
                    f.write(chunk)
        s = getTextFromAudio('audio.mp3')
    except:
        s = request.POST['input_text']
    tokens = task2(task1(s))
    print(tokens)
    result = get_similar(tokens)
    print(result)
    result_video_names = getfinal(tokens, result)
    print(result_video_names)
    final_video = downloadVideo(request,result_video_names)

    return final_video
    # return HttpResponse(f'<h1>{result_video_names}</h1>')


# with open('C:\\Users\k19as\Desktop\Final\WEB\DECIBEL\static\\file_ids.json') as f:
#     video_names = json.loads(f.read())

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
def getAnimation(letters):
    images = []
    letters = [let for let in letters if let!=' ']
    video_name = ''.join(letters)+'.mp4'
    for letter in letters:
        fpath = os.path.join('C:\\Users\k19as\Desktop\Final\WEB\DECIBEL\static\\',letter.upper()+'.jpg')
        images.append(fpath)
    duration = 1  # Duration of each frame in seconds
    fps = 1  # Frame rate of the animation
    clip = ImageSequenceClip(images, fps=fps).set_duration(len(images)*duration)
    clip.write_videofile(video_name, fps=fps)
    return video_name


def downloadVideo(request,result_video_names):
    l = []
    for i in result_video_names:
        if type(i) == str:
            v = VideoFileClip(os.path.join(VIDEOS_PATH,i+'.mp4'),audio=False)
            t = 20 if v.duration > 20 else v.duration
            v = v.subclip(0, t)
            l.append(v) 
        else:
            p = getAnimation(i)
            v = VideoFileClip(p, audio=False)
            t = 20 if v.duration > 20 else v.duration
            v = v.subclip(0, t)
            l.append(v)
    print(l)
    out = concatenate_videoclips(l,method='compose').without_audio()
    # res = HttpResponse(content_type='video/mp4')
    # out.write_videofile(res)
    out.write_videofile('static/result.mp4')
    # C:\Users\k19as\Desktop\Final\WEB\DECIBEL\result.mp4

    return render(request, 'decibel.html')


    
    
    
    # import os
    # import wget

    # def download_video_from_drive(file_id, save_path):
    #     # Get the download URL for the video file
    #     download_url = f'https://drive.google.com/uc?id={file_id}&export=download'

    #     # Download the video file and save it to the specified path
    #     wget.download(download_url, out=save_path)

    #     print(f'Successfully downloaded video from Google Drive to {save_path}')

    #     return save_path
    # paths = []
    # for i in result_video_names:
    #     file_id = video_names.get(i)
    #     x = download_video_from_drive(file_id, i+'.mp4')
    #     paths.append(x)
    # out = []
    # for p in paths:
    #     k = VideoFileClip(p)
    #     out.append(k)

    # dd = concatenate_videoclips(out).without_audio()
    # out = HttpResponse(content_type='video/mp4')
    # dd.write_videofile(out)