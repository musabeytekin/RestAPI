from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd


app = Flask(__name__)
api = Api(app)

class Books(Resource):
    def get(self):
        data = pd.read_csv('books.csv')
        data = data.to_dict('records')
        
        return {'data' : data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Title')
        parser.add_argument('Author')
        parser.add_argument('Genre')
        parser.add_argument('Height')
        parser.add_argument('Publisher')
        args = parser.parse_args()

        data = pd.read_csv('books.csv')

        new_data = pd.DataFrame({
            'Title'      : [args['Title']],
            'Author'      : [args['Author']],
            'Genre'       : [args['Genre']],
            'Height'      : [args['Height']],
            'Publisher'      : [args['Publisher']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('books.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Title', required=True)
        parser.add_argument('Author', required=True)
        parser.add_argument('Genre', required=True)
        parser.add_argument('Height', required=True)
        parser.add_argument('Publisher', required=True)
        args = parser.parse_args()

        data = pd.read_csv('books.csv')

        data = data[data['Title'] != args['Title']]

        data.to_csv('books.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200

class Title(Resource):
    def get(self,title):
        data = pd.read_csv('books.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['Title'] == title :
                return {'data' : entry}, 200
        return {'message' : 'No entry found with this name !'}, 404

class Author(Resource):
    def get(self):
        data = pd.read_csv('books.csv', usecols = [1])
        data = data.to_dict('records')

        return {'data' : data}, 200

api.add_resource(Books, "/books")
api.add_resource(Author, '/author')
api.add_resource(Title, '/<string:title>')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
    