# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:04:54 2019

@author: Ken
"""

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt 
from PIL import Image
from os import path, getcwd
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def get_soup(html):
    """ get data for web page"""
    resp = requests.get(html)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, from_encoding=encoding)
    return soup

def get_links(soup):
    """ Get links from a web page """
    http_link_list = [] 
    for link in soup.find_all('a', href=True):
        if link['href'][0] != '/': 
            http_link_list.append(link['href'].strip("'"))
    return http_link_list 

def get_ps(soup):
    """ get <p> tags from web page"""
    http_link_list = [] 
    for link in soup.find_all('p'):
        http_link_list.append(link.get_text())
    return http_link_list 

def get_text(text_array):
    """ get text from an array"""
    text = " ".join(text_array)
    return text

def get_episode_text(episode_list):
    """get text from all episodes in list"""
    text_return = []
    for i in episode_list:
        print(i)
        soup = get_soup(i)
        text_array = get_ps(soup)
        full_text = get_text(text_array)
        text_return.append(full_text)
    return text_return    

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered


#webpage 
bp_transcripts = 'https://www.biggerpockets.com/podcast-transcripts'

#gets word soup from website 
soupout = get_soup(bp_transcripts)
soupout
#gets links from website     
h_links = get_links(soupout)

#trims to only relevant links
html_links = h_links[5:163]

#return list of all episode text 
text_return_list = get_episode_text(html_links)
all_text = get_text(text_return_list)

#removed punctuation and stop words 
filteredlst = punctuation_stop(all_text)

#list of unwanted words 
unwanted = ['brandon','josh','one','guy','really','mean','little bit','thing','say','go','actually','even','probably','going','said','something','okay','maybe','got','well','way']

#remove unwanted words 
text = " ".join([ele for ele in filteredlst if ele not in unwanted])

#get the working directory 
d = getcwd()

#numpy image file of mask image 
mask_logo = np.array(Image.open(path.join(d, "Bigger_Pockets_Logo4.png")))

#create the word cloud object 
wc= WordCloud(background_color="white", max_words=2000, max_font_size=90, random_state=1, mask=mask_logo, stopwords=STOPWORDS)
wc.generate(text)

image_colors = ImageColorGenerator(mask_logo)

plt.figure(figsize=[10,10])
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis('off')
plt.show()

