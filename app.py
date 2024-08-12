from flask import Flask, request, jsonify
from flask.views import MethodView
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields as ma_fields
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title="Name API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    servers=[{"url": "/"}] 
)

class NameSchema(Schema):
    first_name = ma_fields.String(required=True, metadata={"description": "The first name"})
    last_name = ma_fields.String(required=True, metadata={"description": "The last name"})

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

# Register the endpoint
name_view = NameAPI.as_view('name_api')
app.add_url_rule('/api/names/', view_func=name_view, methods=['POST'])

with app.app_context():
    # Register the schema with the spec within the app context
    spec.components.schema("Name", schema=NameSchema)
    spec.path(view=name_view, path='/api/names/')

@app.route('/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())

# Setup Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Name API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
