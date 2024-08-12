# 
# pip install flask marshmallow apispec apispec-webframeworks flask-swagger-ui


from flask import Flask, request, jsonify
from flask.views import MethodView
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields as ma_fields
from flask_swagger_ui import get_swaggerui_blueprint

# Flask: A micro web framework used to create the web application.
# request, jsonify: Functions from Flask to handle HTTP requests and responses.
# MethodView: A class-based view from Flask for handling HTTP methods.
# APISpec: A tool to create OpenAPI (Swagger) documentation.
# MarshmallowPlugin, FlaskPlugin: Plugins for APISpec to support Marshmallow (data serialization/deserialization) and Flask.
# Schema, fields (ma_fields): Components from Marshmallow to define and validate the data schema.
# get_swaggerui_blueprint: A function to set up Swagger UI for API documentation.

app = Flask(__name__)
# Initializes the Flask application.

# Create an APISpec
spec = APISpec(
    title="Name API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
# APISpec: Initializes an APISpec object to create OpenAPI documentation.
# title: Title of the API.
# version: Version of the API.
# openapi_version: Version of the OpenAPI specification.
# plugins: List of plugins for integrating with Flask and Marshmallow.

class NameSchema(Schema):
    first_name = ma_fields.String(required=True, metadata={"description": "The first name"})
    last_name = ma_fields.String(required=True, metadata={"description": "The last name"})

# NameSchema: A Marshmallow schema to define and validate the input data structure.
# first_name, last_name: Fields in the schema, both required, with a description.

class NameAPI(MethodView):
    def post(self):
        """Get the full name
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema: NameSchema
        responses:
          200:
            description: A full name message
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: My name is John Doe
        """
        schema = NameSchema()
        data = schema.load(request.json)
        first_name = data['first_name']
        last_name = data['last_name']
        return jsonify({"message": f"My name is {first_name} {last_name}"}), 200

# NameAPI: A class-based view inheriting from MethodView.
# post method: Handles POST requests.
# docstring: Contains OpenAPI documentation for this endpoint, including request body and responses.
# schema.load: Validates and deserializes the incoming JSON data according to NameSchema.
# jsonify: Creates a JSON response with a message containing the full name.

# Register the endpoint
name_view = NameAPI.as_view('name_api')
app.add_url_rule('/api/names/', view_func=name_view, methods=['POST'])

# as_view: Converts the NameAPI class into a view function.
# add_url_rule: Registers the endpoint /api/names/ for POST requests

with app.app_context():
    # Register the schema with the spec within the app context
    spec.components.schema("Name", schema=NameSchema)
    spec.path(view=name_view, path='/api/names/')
# app.app_context(): Ensures the context for the Flask app is available.
# spec.components.schema: Registers the NameSchema with the APISpec.
# spec.path: Registers the path /api/names/ with the view function name_view in the APISpec

@app.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())
# create_swagger_spec: Endpoint to return the OpenAPI documentation in JSON format.

# Setup Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Name API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# SWAGGER_URL: URL prefix for accessing Swagger UI.
# API_URL: URL of the Swagger JSON endpoint.
# get_swaggerui_blueprint: Creates a blueprint for the Swagger UI.
# register_blueprint: Registers the Swagger UI blueprint with the Flask app.

if __name__ == '__main__':
    app.run(debug=True)
