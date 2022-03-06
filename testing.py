import requests

BASE = "http://127.0.0.1:5000/"

# to się robi jesli zrobimy get
# response = requests.get(BASE + "rename")
# print(response.json())

"""data = [{"isbn": fields.Integer, }
    "title": fields.String,
    "author": fields.String,
    "published": fields.String,
    "pages": fields.Integer,
    "cover": fields.String,
    "language": fields.String"""

"""response = requests.put(BASE + "book/78", {"isbn": 78, "title": "elves in ireland", "author":
    "rienn", "date": "02-02-2022", "pages": 555})
print(response.json())"""

response = requests.get(BASE + "book/78")
print(response.json())
input()
response = requests.patch(BASE + "book/78", {"title": "Elves in Dublin", "author": "Rienn"})
print(response.json())
input()
response = requests.get(BASE + "book/78")
print(response.json())
