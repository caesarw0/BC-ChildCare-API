from flask import Blueprint
from flasgger import swag_from

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/welcome/')
def welcome():
    """
    Welcome Endpoint
    ---
    tags:
      - Resources
    summary: Get a welcome message
    description: This endpoint provides a welcome message for users accessing the BC childcare API.
    responses:
      200:
        description: Welcome message
        content:
          application/json:
            example: {"message": "Welcome to the BC childcare API"}
    """
    return {'message' : 'welcome to the BC childcare API'}

@resources_bp.route('/about/')
def about():
    """
    About Endpoint
    ---
    tags:
      - Resources
    summary: Get information about the API
    description: This endpoint provides information about the BC childcare API, including its data source.
    responses:
      200:
        description: Information about the API
        content:
          application/json:
            example: {"message": "This is an API endpoint that uses data from the British Columbia Government", "url": "https://catalogue.data.gov.bc.ca/dataset/child-care-map-data/resource/9a9f14e1-03ea-4a11-936a-6e77b15eeb39"}
    """
    return {'message' : 'this is an API endpoint that uses data from the British Columbia Government',
            'url': 'https://catalogue.data.gov.bc.ca/dataset/child-care-map-data/resource/9a9f14e1-03ea-4a11-936a-6e77b15eeb39'}