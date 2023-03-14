#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('pip install Flask')


# In[2]:


import openai
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import re

# Replace 'your_api_key' with your actual OpenAI API key
openai.api_key = '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'


# In[4]:


url = "https://www.record.com.mx/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

article_links = soup.find_all("div", class_="itemTit views-field-title")[:5]

translator = Translator()

def sentiment_analysis(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Sentiment analysis of the following text: '{prompt}'.",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    sentiment = response.choices[0].text.strip().lower()
    return sentiment

def extract_first_sentence(text):
    sentences = re.split(r'[.!?]+', text)
    return sentences[0]

for i, link in enumerate(article_links, start=1):
    article_url = url + link.a['href']
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    title_element = article_soup.find("h1", class_="titulo") or article_soup.find("h1")
    content_element = article_soup.find("div", class_="field-name-body")

    if title_element and content_element:
        title = title_element.text.strip()
        content = content_element.text.strip()

        translated_title = translator.translate(title, src="es", dest="en").text
        translated_content = translator.translate(content, src="es", dest="en").text

        first_sentence = extract_first_sentence(translated_content)
        sentiment = sentiment_analysis(first_sentence)

        print(f"Article {i}:")
        print(f"Original Title: {title}")
        print(f"Translated Title: {translated_title}")
        print(f"First Sentence: {first_sentence}")
        print(f"Sentiment: {sentiment}\n")
    else:
        print(f"Article {i}: Unable to extract title or content.")


# In[6]:


from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import re
import openai

app = Flask(__name__)

# Be sure to replace "your-api-key" with your actual OpenAI API key.
openai.api_key = "your-api-key"

# The rest of your code (i.e., the sentiment_analysis function, extract_first_sentence function, and so on) goes here.
# For example:
def sentiment_analysis(prompt):
    ...

@app.route("/")
def index():
    url = "https://www.record.com.mx/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Your existing code continues here, until the end of the for loop
    ...

    # Instead of printing the output, store it in a list of dictionaries
    articles = []
    for i, link in enumerate(article_links, start=1):
        ...

        # Replace the print statements with this:
        articles.append({
            "index": f"Article {i}",
            "original_title": title,
            "translated_title": translated_title,
            "first_sentence": first_sentence,
            "sentiment": sentiment,
        })

    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




