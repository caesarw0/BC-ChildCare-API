from flask import Blueprint, Flask, request, jsonify
from utils.data_loading import load_data_from_csv
from flasgger import swag_from

# data loading
df = load_data_from_csv()

childcare_retrieval_bp = Blueprint('childcare_retrieval', __name__)

@childcare_retrieval_bp.route('/childcare/')
def get_all_childcare_centers():
    """
    Get All Childcare Data within BC
    ---
    tags:
      - Childcare Retrieval
    summary: Retrieve a list of all childcare centers
    description: This endpoint retrieves a list of all childcare centers in British Columbia.
    responses:
      200:
        description: List of childcare center data
    """
    return jsonify(df.to_dict(orient='records'))

@childcare_retrieval_bp.route('/childcare/<int:center_id>')
def get_childcare_center(center_id):
    """
    Get Childcare Center Data by Center ID within BC
    ---
    tags:
      - Childcare Retrieval
    summary: Retrieve a Childcare Center by Center ID
    description: This endpoint retrieves details of a single childcare center in British Columbia, based on the provided center ID.
    parameters:
      - in: path
        name: center_id
        required: true
        schema:
          type: integer
          format: int64
        description: The unique ID of the childcare center to retrieve.
    responses:
      200:
        description: Successful response with the childcare center's details
        content:
          application/json:
            example: {"center_name": "ABC Childcare", "location": "Vancouver"}
      404:
        description: Childcare center not found
        content:
          application/json:
            example: {"message": "Childcare center not found"}
    """
    center = df[df['FAC_PARTY_ID'] == center_id].to_dict(orient='records')
    if center:
        return jsonify(center[0])
    else:
        return jsonify({'message': 'Child care center not found'}), 404

def filter_by_vacancy_columns():
    filtered_centers = df[df.apply(lambda row: any(row[col] == 'Y' for col in row.index if col.startswith('VACANCY_SRVC')), axis=1)]
    return filtered_centers

@childcare_retrieval_bp.route('/childcare/with-vacancy')
def filter_vacancy_by_columns():
    """
    Filter Childcare Centers by Vacancy Columns
    ---
    tags:
      - Childcare Retrieval
    summary: Filter Childcare Centers by Vacancy
    description: This endpoint filters childcare centers based on VACANCY_SRVC and returns the filtered results.
    responses:
      200:
        description: Successful response with filtered childcare centers
        content:
          application/json:
            example: [{"center_name": "ABC Childcare", "vacant_spots": 3}, {"center_name": "XYZ Childcare", "vacant_spots": 2}]
    """
    filtered_centers = filter_by_vacancy_columns()
    return jsonify(filtered_centers.to_dict(orient='records'))

@childcare_retrieval_bp.route('/childcare/cities')
def get_available_cities():
    """
    Get Available Cities with Childcare Centers
    ---
    tags:
      - Childcare Retrieval
    summary: Retrieve a list of available cities with childcare centers in BC
    description: This endpoint retrieves a list of cities where childcare centers are available in BC.
    responses:
      200:
        description: Successful response with list of available cities
        content:
          application/json:
            example: {"available_cities": ["Vancouver", "Burnaby", "Richmond"]}
    """
    available_cities = df['CITY'].unique().tolist()
    return {"available_cities": available_cities}