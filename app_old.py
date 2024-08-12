from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Name API', description='A simple API to get name')

ns = api.namespace('names', description='Operations related to names')

name_model = api.model('Name', {
    'first_name': fields.String(required=True, description='The first name'),
    'last_name': fields.String(required=True, description='The last name')
})

@ns.route('/')
class Name(Resource):
    @ns.expect(name_model)
    def post(self):
        """Get the full name"""
        data = request.json
        first_name = data['first_name']
        last_name = data['last_name']
        return {"message": f"My name is {first_name} {last_name}"}

if __name__ == '__main__':
    app.run(debug=True)
