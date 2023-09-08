import json
from flask import Flask, request, jsonify
from flasgger import Swagger
# blueprint imports
# from resources import resources_bp
from . import resources
from . import data_retrieval
# from data_retrieval import childcare_retrieval_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(resources_bp, url_prefix='/api')
app.register_blueprint(childcare_retrieval_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)