from googleapiclient.discovery import build
from urllib.parse import urlparse
from urllib.request import urlopen
import pprint
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.tag import pos_tag
import string
import wikipedia
from lxml import etree
import requests


my_api_key = "AIzaSyBItnuy5o16BtfVEfCbkm6PHlq_JnlU_mY"
my_cse_id = "005011606875748037020:u78tilaw9me"

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def search(keyword):
    for i in range(1):
        print('Fetching range {}...'.format(i+1))
        results = google_search(
            keyword, my_api_key, my_cse_id, lowRange=(i*10), highRange=(i*10+10))
        for result in results:
            print(result['pagemap'])
            break


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_proper_nouns(text):
    tagged_sent = pos_tag(text.split())
    return [word for word,pos in tagged_sent if pos == 'NNP']

def keep_alpha(strings):
    alpha_strings = []
    for string in strings:
        chars = [c for c in string if c.isalpha()]
        if len(chars) > 0:
            alpha_strings.append(''.join(chars))
    return list(set(alpha_strings))

def keep_nums(string):
    return ''.join([c for c in string if c.isnumeric()])

with open("english_words.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

def is_english_word(word):
    return word.lower() in english_words

html = urlopen('https://www.cbinsights.com/research/wealth-tech-fin-tech-market-map/').read()
text = text_from_html(html)
props = get_proper_nouns(text)
alpha = keep_alpha(props)
names = [s for s in alpha if not is_english_word(s)]


for string in names:
    try:
        # Throw exception if no wikipedia page found
        page = wikipedia.page(string, auto_suggest=False)

        r = requests.get('https://en.wikipedia.org/wiki/' + page.title).text
        doc = etree.fromstring(r)
        num_of_employees = doc.xpath('//table[@class="infobox vcard"]/tr[th/div/text()="Number of employees"]/td')
        website = doc.xpath('//table[@class="infobox vcard"]/tr[th/text()="Website"]/td/span/a')

        found_num_of_employees = len(num_of_employees) > 0
        if found_num_of_employees:
            num_of_employees = int(keep_nums(num_of_employees[0].text))
        else:
            num_of_employees = -1

        found_website = len(website) > 0
        if found_website:
            website = website[0].attrib['href']
        else:
            website = 'N/A'

        if found_num_of_employees and num_of_employees < 1000:
            print(string)
            print(str(num_of_employees) + ' employees')
            print(website)
            print()
        elif not found_num_of_employees and found_website:
            print(string + '(?)')
            print(website)
            print()


    except Exception as e:
        pass
