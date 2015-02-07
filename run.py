from flask import Flask, Response
from bson import json_util
from pymongo import MongoClient

app = Flask(__name__)
'''
mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements
'''
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
