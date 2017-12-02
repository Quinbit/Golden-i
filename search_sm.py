import facebook
import requests
from google.cloud import language
from google.oauth2 import service_account


access_token = "EAACEdEose0cBAIZBci7JVpgF3RjDRnIIaT0KzHdbZArPZAonbPasQQd6jHepaUPRWFb64NumlUX1sOsGUmZCYsBvX0iDoaaLstThV3ZA4ZAxhgzIjZCWUMyVglr83IJ2e7u3qSMuH1X6MoFLocZCWBZBQOiZBACZA5SctZCZBVU5SmCkpI6Bbl6D7VDr7yyLun5YlOD4ZD"
graph = facebook.GraphAPI(access_token=access_token, version="2.11")

base_url = "https://graph.facebook.com/v2.7/"
num_page = 1
max_page =3
max_comments = 3

client = language.LanguageServiceClient()
#f = open("messages.txt", "a")

g = open("complaints.txt", "w")

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
    mes = mes["comments"]["data"]

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

if __name__=="__main__":
    pages = graph.search(type='page',q='news')
    pages = pages['data']

    for i in range(num_page):
        messages_and_ids = []
        id = pages[i]['id']
        print("Processing " + pages[i]["name"])
        url = base_url + id + "/posts?access_token=" + access_token
        messages =  get_facebook_data(max_page, url)
        print("Finished page with " + str(len(messages)) + " valid messages")
        messages_and_ids += messages



        wants = {"data":[]}
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
                    g.write(messages_and_ids[n][0])
                    words.append(x.name)

            data.append({"keywords":words, "id": ids})

        #print(wants)
        wants["data"] = data
        string = str(wants)
        r = requests.post("http://morrisjchen.com:4242/post_data", data=string)
        print(r.status_code, r.reason)

        if (int(r.status_code) != 200):
            break;
    #f.close()

    g.close()
