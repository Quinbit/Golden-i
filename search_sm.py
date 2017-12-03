import facebook
import requests
from google.cloud import language
from google.oauth2 import service_account
import json


access_token = "EAACEdEose0cBAM6DeELkJz7PfdV4XMz2ZAsUpD1fcmSq07ohI7iunkcl0BR3h1HAdTWWgXwFLX0j2FqLu1IuPrAcRWM7BP7DLXM3A6LzCr43eNLjpBz11z8bQjrpykOhv508ptICIAIaqRZAC0yF9eW3WwYXhEMPUcrpPnVaPUtKnxbgrZACZA6bfZAKrLI0ZD"
graph = facebook.GraphAPI(access_token=access_token, version="2.11")

base_url = "https://graph.facebook.com/v2.7/"
num_page = 10
max_page = 10
max_comments = 10

client = language.LanguageServiceClient()

needs = ['want', 'wish', 'problem', 'issue', 'dislike', 'annoying', 'annoyance']

def get_facebook_data(index, url):
    r = requests.get(url)
    data = r.json()
    #print(data)
    paging = data["paging"]
    data = data['data']
    n_page = paging.get("next", 0)
    print("Working on page " + str(max_page - index + 1))
    if (n_page != 0) and index > 1:
        return parse_data(data) + get_facebook_data(index - 1, n_page)
    else:
        return parse_data(data)

def parse_data(data):
    res = []
    for i in range(len(data)):
        mes = data[i]
        iden = mes.get("id","")
        message = get_comments(iden)
        #f.write(message.lower() + "\n")
        res = res + message

    return res

def get_comments(iden):
    mes = graph.get_object(id=iden,fields="comments")
    try:
        mes = mes["comments"]["data"]
    except:
        print(mes)
        return []

    res = []

    for i in range(len(mes)):
        if (test_for_want(mes[i]["message"])):
            res += [[mes[i]["message"],mes[i]["id"]]]

    return res


def test_for_want(message):
    for i in needs:
        if i in message:
            return True

    return False

def crawl_page(url):
    page = graph.search(id=url)

    messages_and_ids = []
    id = page['id']
    print("Processing " + page["name"])

    url = base_url + id + "/posts?access_token=" + access_token
    messages =  get_facebook_data(max_page, url)
    print("Finished page with " + str(len(messages)) + " valid messages")
    messages_and_ids += messages

    wants = {"keywords":[], "message_id":[]}
    data = []
    for n in range(len(messages_and_ids)):
        print("Analyzing content of message " + str(n+1))
        try:
            document = language.types.Document(
                content=messages_and_ids[n][0],
                type='PLAIN_TEXT',
            )

            response = client.analyze_entity_sentiment(
                document=document,
                encoding_type='UTF32',
            )
        except:
            continue

        entities = response.entities
        #print("Analyzing sentiment " + str(n))
        words = []
        ids = messages_and_ids[n][1]
        for x in entities:
            #print(x.sentiment.score)
            #print(messages_and_ids[1][n][i])
            try:
                val = x.sentiment.score
            except:
                val = 1.0
            if val < 0.0:
                #g.write(messages_and_ids[n][0])
                words.append(x.name)

        #data.append({"keywords":words, "id": ids})
        wants["keywords"].append(words)
        wants["message_id"].append(ids)
    wants["name"] = page["name"]
    wants["url"] = base_url + id + "?access_token=" + access_token
    #print(wants)
    #g.write(str(data))
    headers = {'content-type': 'application/json'}
    #print(json.dumps(wants))
    r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
    print(r.status_code, r.reason)

def begin_crawl(search_term):
    pages = graph.search(type='page',q=search_term)
    pages = pages['data']
    #f = open("messages.txt", "a")

    g = open("complaints.txt", "w")

    for i in range(num_page):
        messages_and_ids = []
        id = pages[i]['id']
        print("Processing " + pages[i]["name"])

        url = base_url + id + "/posts?access_token=" + access_token
        messages =  get_facebook_data(max_page, url)
        print("Finished page with " + str(len(messages)) + " valid messages")
        messages_and_ids += messages



        wants = {"keywords":[], "message_id":[]}
        data = []
        for n in range(len(messages_and_ids)):
            print("Analyzing content of message " + str(n+1))
            try:
                document = language.types.Document(
                    content=messages_and_ids[n][0],
                    type='PLAIN_TEXT',
                )

                response = client.analyze_entity_sentiment(
                    document=document,
                    encoding_type='UTF32',
                )
            except:
                continue

            entities = response.entities
            #print("Analyzing sentiment " + str(n))
            words = []
            ids = messages_and_ids[n][1]
            for x in entities:
                #print(x.sentiment.score)
                #print(messages_and_ids[1][n][i])
                try:
                    val = x.sentiment.score
                except:
                    val = 1.0
                if val < 0.0:
                    #g.write(messages_and_ids[n][0])
                    words.append(x.name)

            #data.append({"keywords":words, "id": ids})
            wants["keywords"].append(words)
            wants["message_id"].append(ids)
        wants["name"] = pages[i]["name"]
        wants["url"] = base_url + id + "?access_token=" + access_token
        #print(wants)
        #g.write(str(data))
        headers = {'content-type': 'application/json'}
        #print(json.dumps(wants))
        r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
        print(r.status_code, r.reason)

        if (int(r.status_code) != 200):
            break;
    #f.close()

    g.close()
