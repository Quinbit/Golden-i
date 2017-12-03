from google.cloud import language
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import imgkit
from purpose_similarity import *

client = language.LanguageServiceClient()

def extract_text(html):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    soup = BeautifulSoup(html)
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return ''.join(t.strip() for t in visible_texts)

def get_breakdown(url):
    try:
    	f = requests.get(url)
    except:
	print("Failed to access url")
	return []
    text = f.text
    string = extract_text(text)

    #print(string)

    document = language.types.Document(
        content=str(string.encode("ascii","ignore")),
        type='PLAIN_TEXT',
    )

    response = client.analyze_entity_sentiment(
        document=document,
        encoding_type='UTF32',
    )
    entities = response.entities

    words = []
    for x in entities:
        words.append(x.name)

    return words

def order_list(links, terms):
    words = []
    for i in range(len(links)):
	print("Breaking down word " + str(i+1))
        words.append(get_breakdown(links[i]))

    similarity = []
    for i in range(len(words)):
	print("Getting similarity of " + str(i+1))
        similarity.append([similarity_of_set(words[i], terms), links[i]])

    l = sorted(similarity)

    final_link = []

    for i in range(len(similarity)):
        final_link.append(l[i][1])

    return final_link


if __name__=="__main__":
    url = "https://techcrunch.com/2016/05/12/the-technology-driven-transformation-of-wealth-management/"
    get_breakdown(url)
    imgkit.from_url(url, 'image.jpg')
