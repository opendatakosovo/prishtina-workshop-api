from flask import Flask, Response
from bson import json_util
from pymongo import MongoClient

app = Flask(__name__)

mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<string:komuna>/redflags/<int:viti>')
def red_flags(komuna, viti):
    json = collection.aggregate([
            {
                "$match": {
                    "viti": viti,
                    "city": komuna
                }
            },
            {
                "$group": {
                    '_id': {
                        'kompania_emri': '$kompania.emri',
                        "aktiviteti": "$aktiviteti",
                        'muaji': {
                            '$month': '$dataNenshkrimit'
                        }
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "qmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "qmimiAneks": {
                        "$sum": "$kontrata.qmimiAneks"
                    }
                },
            },
            {
                '$sort': {
                        'muaji': -1
                    }
            },
            {
                "$project": {
                    "_id": 0,
                    "pershkrimi": "$_id.aktiviteti",
                    "kompania": "$_id.kompania_emri",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "qmimiAneks": "$qmimiAneks",
                }
            }
        ])
    resp = Response(
        response=json_util.dumps(json["result"]),
    mimetype='application/json')

    return resp

@app.route('/prokurimi')
def prokurimi():
	json_obj = collection.aggregate([
		{"$match":{
			"city":"prishtina"
		}},
		{"$group":{
			"_id":{
				"tipiProkurimit":"$tipi",
			},
			"vleraKontrates":{
				"$sum":"$kontrata.vlera"
			}
		}},
		{"$project":{
			"_id":0,
			"tipi":"$_id.tipiProkurimit",
			"vlera":"$vleraKontrates"
		}

		}
	])
	return Response(response=json_util.dumps(json_obj['result']), mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
