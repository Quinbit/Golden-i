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

    soup = BeautifulSoup(html, 'lxml')
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


def handle_disambiguation_options(options):
    company_keywords = set(['company', 'inc.', 'business', 'organization'])
    possible_companies = []
    for k in company_keywords:
        possible_companies.extend([o for o in options if k in o.lower()])

    if len(possible_companies) > 1:
        # Choose the page with the shortest title
        min_company = possible_companies[0]
        min_length = len(min_company)
        for company in possible_companies:
            if len(company) < min_length:
                min_company = company
                min_length = len(min_company)

        try:
            page = wikipedia.page(min_company)
            print('Found min company: ' + min_company)
            return page
        except:
            print('Disambiguation found no page')
            return None

    elif len(possible_companies) == 1:
        try:
            page = wikipedia.page(possible_companies[0])
            print('Found single company: ' + possible_companies[0])
            return page
        except:
            print('Disambiguation found no page')
            return None
    else:
        print('Disambiguation found no page')
        return None


def find_wikipedia_page(noun, disambiguations=False):
    try:
        page = wikipedia.page(noun, auto_suggest=False)
        if disambiguations and page.title + ' (disambiguation)' in page.links:
            # Trigger disambiguation handler
            print('*** Triggering disambiguation handler')
            page = wikipedia.page(page.title + ' (disambiguation)')
        else:
            print('Page found: ' + noun)
            return page

    except wikipedia.exceptions.DisambiguationError as e:
        if disambiguations:
            return handle_disambiguation_options(e.options)
        else:
            return None
    except wikipedia.exceptions.PageError:
        print('No page found: ' + noun)
        return None


def crawl_article(link):
    print('Crawling article ' + link)
    print('Opening html...')
    html = urlopen(link).read()
    print('Extracting text...')
    text = extract_text(html)
    print('Filtering to nouns...')
    nouns = get_proper_nouns(text)
    print('Trimming tokens...')
    alpha_nouns = remove_non_alpha(nouns)
    print('Filtering to proper nouns...')
    proper_nouns = [s for s in alpha_nouns if not s.lower() in english_words]

    pages = []
    for proper_noun in proper_nouns:
        print()
        print('*** Finding Wikipedia page for noun ' + proper_noun)
        page = find_wikipedia_page(proper_noun)
        if page != None:
            pages.append(page)
    return pages


def is_startup_page(page):
    print('Checking is_startup for ' + page.url + '...')
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

    if found_website and found_num_of_employees and num_of_employees < 1000:
        # We know that this is a startup
        print('found_website and found_num_of_employees and is_startup')
        return True
    elif found_website and not found_num_of_employees:
        # We can't confirm that this is a startup
        print('found_website and not found_num_of_employees')
        return True
    else:
        print('Not a startup site')
        return False


search_phrase = 'cheap wealth management tech startup'
print('Googling \'' + search_phrase + '\'')
results = google_search('cheap wealth management tech startup', num=1)
startup_links = []
for link in [r['link'] for r in results]:
    print()
    if link == get_scheme_and_domain(link):
        print('*** Direct link, adding: ' + link)
        startup_links.append(link)
    else:
        print('*** Article link, crawling for companies: ' + link)
        pages = crawl_article(link)
        startup_pages = [p for p in pages if is_startup_page(p)]
        startup_links.extend([p.url for p in startup_pages])

print()
print('*** Startup links:')
for l in startup_links:
    print(l)
