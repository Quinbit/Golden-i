import facebook
import requests
from google.cloud import language
from google.oauth2 import service_account
import json
from flask import Flask, jsonify
from flask_cors import CORS


access_token = "EAACEdEose0cBAHZCMJJk6Hq8F3zmImxIlxQFtS8I6k2xmOo5LVlBuBAjVFOYfmqFFbQq6etYdoG20S3uoGaQHGI4Pw7urOZBAxVQwoDoZCQVVp261AlOhMzE4EHZAcF5yBYmNQNZBadkgnfQYZCbNLPAOvF4Wx8T8nsGoKZCRu5ctr2w0u38ZAwjZAs5ha3s9cYAZD"
graph = facebook.GraphAPI(access_token=access_token, version="2.11")

base_url = "https://graph.facebook.com/v2.7/"
num_page = 10
max_page = 10
max_comments = 10

client = language.LanguageServiceClient()

needs = ['want', 'wish', 'problem', 'issue', 'dislike', 'annoying', 'annoyance']
headers = {'content-type': 'application/json'}

app = Flask(__name__)
CORS(app)

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
    wants["tag"] = page["name"]
    wants["busy"] = False
    wants["starts"] = False
    #print(wants)
    #g.write(str(data))
    headers = {'content-type': 'application/json'}
    #print(json.dumps(wants))
    r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
    print(r.status_code, r.reason)

def begin_crawl(search_term, num_pages):
    pages = graph.search(type='page',q=search_term)
    pages = pages['data']
    #f = open("messages.txt", "a")

    g = open("complaints.txt", "w")

    for i in range(int(num_pages)):
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
        wants["tag"] = search_term
        wants["busy"] = not (i == (int(num_pages) - 1))
        wants["starts"] = False
        #print(wants)
        #g.write(str(data))
        #print(json.dumps(wants))
        r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
        print(r.status_code, r.reason)

        if (int(r.status_code) != 200):
            break;
    #f.close()

    g.close()

@app.route('/crawl/<term>/<num_pages>', methods = ['POST'])
def start_general_crawl(term, num_pages):
    wants = {"busy" : True, "starts": True}
    r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
    begin_crawl(term, num_pages)

@app.route('/analyze/<url>', methods = ['POST'])
def start_specific_crawl(url):
    wants = {"busy" : True, "starts": True}
    r = requests.post("http://morrisjchen.com:4242/post_data", json=wants, headers=headers)
    crawl_page(url)

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=6996)
