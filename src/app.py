import json
from flask import Flask, request, jsonify
from flasgger import Swagger
# blueprint imports
from resources import resources_bp
from data_retrieval import childcare_retrieval_bp

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return '''Welcome to the BC Childcare API Application, please refer to the 
    <a href="https://github.com/caesarw0/BC-ChildCare-API">GitHub Page</a> for more info'''

app.register_blueprint(resources_bp, url_prefix='/api')
app.register_blueprint(childcare_retrieval_bp, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)