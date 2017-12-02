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
import time


my_api_key = "AIzaSyBItnuy5o16BtfVEfCbkm6PHlq_JnlU_mY"
my_cse_id = "005011606875748037020:u78tilaw9me"


def get_scheme_and_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain


def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
    return res['items']


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


def get_proper_nouns(text):
    tagged_sent = pos_tag(text.split())
    return [word for word,pos in tagged_sent if pos == 'NNP']


def remove_non_alpha(strings):
    alpha_strings = []
    for string in strings:
        chars = [c for c in string if c.isalpha()]
        if len(chars) > 0:
            alpha_strings.append(''.join(chars))
    return list(set(alpha_strings))


def remove_non_numeric(string):
    return ''.join([c for c in string if c.isnumeric()])


with open("english_words.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)


def get_sites(link):
    print('Opening html...')
    html = urlopen(link).read()
    print('Extracting text...')
    text = extract_text(html)
    print('Filtering nouns...')
    props = get_proper_nouns(text)
    print('Trimming tokens...')
    alpha = remove_non_alpha(props)
    print('Filtering proper nouns...')
    names = [s for s in alpha if not s.lower() in english_words]

    res_links = []
    for string in names:
        print('Checking noun ' + string + '...')
        try:
            # Throw exception if no wikipedia page found
            page = wikipedia.page(string, auto_suggest=False)

            r = requests.get(page.url).text
            doc = etree.fromstring(r)
            num_of_employees = doc.xpath('//table[@class="infobox vcard"]/tr[th/div/text()="Number of employees"]/td')
            website = doc.xpath('//table[@class="infobox vcard"]/tr[th/text()="Website"]/td/span/a')

            found_num_of_employees = len(num_of_employees) > 0
            if found_num_of_employees:
                num_of_employees = int(remove_non_numeric(num_of_employees[0].text))

            found_website = len(website) > 0
            if found_website:
                website = website[0].attrib['href']

            if not found_num_of_employees:
                print('No employee count found')
            elif not found_website:
                print('No website found')

            if found_num_of_employees and num_of_employees < 1000 and found_website:
                print(string)
                print(str(num_of_employees) + ' employees')
                print(website)
                print()
                res_links.append(website)

        except Exception as e:
            print('No Wikipedia page found')
            pass
    return res_links

search_phrase = 'mental violence mass people domestic "tech startup"'
print('Googling \'' + search_phrase + '\'')
results = google_search(search_phrase, num=5)
company_links = []
for link in [r['link'] for r in results]:
    print()
    if link == get_scheme_and_domain(link):
        print('*** Direct link, adding to company_links: ' + link)
        company_links.append(link)
    else:
        print('*** Article link, crawling for companies: ' + link)
        company_links.append(get_sites(link))
