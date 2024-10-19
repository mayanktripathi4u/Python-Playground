from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

Data = []

class People(Resource):
    def get(self, name):
        for x in Data:
            if x['Data'] == name:
                return x
        return {'Data':None}

    def post(self, name):
        team = {'Data':name}
        Data.append(team)
        return team

    def delete(self, name):
        for idx, x in enumerate(Data):
            if x['Data'] == name:
                team = Data.pop(idx)
                return {'Note':"Deleted"}

api.add_resource(People, "/Name/<string:name>")


if __name__ == "__main__":
    app.run(debug = True, port=5002)