import requests
import sys
import random
#
#     print(word)
#     # res=requests.get(url=f"https://jsonplaceholder.typicode.com/{word}")
#     # print(res)
#     # data=res.json()
#     # print(data)
count=0
for word in sys.stdin:

    word=word.strip()
    sample=f"https://jsonplaceholder.typicode.com/{word}"
    res=requests.get(url=sample)
    data=res
    if(res.status_code==200):
        print(data)
        print(res.text)


