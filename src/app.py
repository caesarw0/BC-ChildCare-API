import json
from flask import Flask, request, jsonify
from flasgger import Swagger
# blueprint imports
from resources import resources_bp
from data_retrieval import childcare_retrieval_bp

swagger_config = {
    "title": "BC Childcare API",
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)

@app.route('/')
def home():
    return '''Welcome to the BC Childcare API Application, please refer to the 
    <a href="https://github.com/caesarw0/BC-ChildCare-API">GitHub Page</a> for more info'''

app.register_blueprint(resources_bp, url_prefix='/api')
app.register_blueprint(childcare_retrieval_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)