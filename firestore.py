import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./jonvi.json')
default_app = firebase_admin.initialize_app(cred)

client = firestore.client()

# data = client.collection(u'trading_bot').document().get().to_dict()

users_ref = client.collection('trading_bot')
docs = users_ref.get()

for doc in docs:
    # print doc.to_dict()
    data = doc.to_dict()
    # print data["uid"]
    if data["uid"] == "eQv7pFLHp4WXjAmoSI4i8ZNL6WF2":
        print data["bot_id"]

    # print(u'{} => {}'.format(doc.id, doc.to_dict()))


# cities_ref = client.collection(u'trading_bot')
# print cities_ref


# https://firebase.google.com/docs/admin/setup
# https://stackoverflow.com/questions/51213446/working-with-firestore-server-timestamp-in-python