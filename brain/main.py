import requests
import json
import time
from tinydb import TinyDB, Query

url = 'https://question.hortor.net/question/quiz/getCheckQuiz'
payload = {'uid': 'xxxxxxx',
           't': 'xxxxxxx',
           'sign': 'xxxxxxxx'
           }
db = TinyDB('db.json')
count = db.all()[-1].doc_id
while True:
    # GET with params in URL
    r = requests.get(url, params=payload, verify=False)

    # POST with form-encoded data
    # r = requests.post(url, data=payload)

    # POST with JSON
    # r = requests.post(url, data=json.dumps(payload))

    # Response, status etc
    # {
    # 	"data": {
    # 		"id": 2945336,
    # 		"schoolId": 6,
    # 		"quizType": 29,
    # 		"title": "以下那项不是雾霾的主要成分",
    # 		"option0": "一氧化碳",
    # 		"option1": "二氧化硫",
    # 		"option2": "氮氧化物",
    # 		"option3": "可吸入颗粒物",
    # 		"status": 0,
    # 		"reason": "",
    # 		"createdAt": 1515562256
    # 	},
    # 	"errcode": 0
    # }
    print(r)

    if r.json()['errcode'] != 0:
        print(r.json())
        break
    else:
        data = r.json()['data']
        print("%s. %s:%s" % (count, data['title'], data['option0']))
        count += 1
        db.insert({'title': data['title'],
                   'option': data['option0'],
                   't': int(time.time()*1000),
                   })

print("Script Exit!")
