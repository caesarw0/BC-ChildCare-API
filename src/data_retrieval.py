from flask import Blueprint, Flask, request, jsonify
from utils.data_loading import load_data_from_csv
from utils.str_processing import parse_str_to_list
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

@childcare_retrieval_bp.route('/childcare/query')
def query_childcare_data():
    """
    Query Childcare Data
    ---
    tags:
      - Childcare Query
    summary: Query childcare data with various filtering options
    parameters:
      - in: query
        name: select
        schema:
          type: string
        description: Fields to select in the response
      - in: query
        name: where
        schema:
          type: string
        description: Filtering conditions (e.g., location=Vancouver,age_group=toddler)
      - in: query
        name: order_by
        schema:
          type: string
        description: Field to order results by
      - in: query
        name: order_direction
        schema:
          type: string
        description: Direction of ordering (e.g. 'ASC', 'DESC')
      - in: query
        name: limit
        schema:
          type: integer
        description: Limit number of results
      - in: query
        name: offset
        schema:
          type: integer
        description: Offset for results
    responses:
      200:
        description: Query results
    """
    # Extract query parameters
    select_fields = request.args.get('select')
    where_conditions = request.args.get('where')
    order_by_field = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)

    

    # Apply filtering based on query parameters
    filtered_data = df # copy df
    # 1. WHERE clause
    if where_conditions:
        for condition in where_conditions.split(','):
            field, value = condition.split('=')
            if filtered_data[field].dtype == 'int64':
              filtered_data = filtered_data[filtered_data[field] == int(value)]
            if filtered_data[field].dtype == 'float64':
              filtered_data = filtered_data[filtered_data[field] == float(value)]
            if filtered_data[field].dtype == 'object':
              filtered_data = filtered_data[filtered_data[field] == (value)]
    
    # 2. SELECT clause
    if select_fields:
        select_fields = parse_str_to_list(select_fields)
        if all(item in filtered_data.columns for item in select_fields):
            filtered_data = filtered_data[select_fields]
        else:
            return jsonify({'message': 'Invalid selection: some fields specified are not in the df'}), 400
    # 3. ORDER BY clause
    if order_by_field:
        order_by_field = parse_str_to_list(order_by_field)
        if order_direction:
            order_direction = parse_str_to_list(order_direction)
        else:
            # Default to ascending if not provided
            order_direction = ['ASC'] * len(order_by_field)
        if all(item in filtered_data.columns for item in order_by_field):
          if len(order_by_field) != len(order_direction):
              return jsonify({'message': 'Number of order_by fields must match number of order_direction fields'}), 400
          
          try:
              for field, direction in zip(order_by_field, order_direction):                  
                  if direction.upper() == 'DESC':
                      filtered_data = filtered_data.sort_values(by=field, ascending=False)
                  else:
                      filtered_data = filtered_data.sort_values(by=field, ascending=True)
          except KeyError:
              return jsonify({'message': 'Invalid field specified for ordering'}), 400
        else:
            return jsonify({'message': 'Invalid Order: some fields specified are not in the Select Clause'}), 400
    # Apply limits and offsets
    if limit:
        if limit <= 0:
          return jsonify({'message': 'Invalid limit value: limit is less than or equal to 0'}), 400
        filtered_data = filtered_data[:limit]
    if offset:
        if limit and offset > limit:
            return jsonify({'message': 'Invalid offset: offset is larger than limit'}), 400
        if offset < 0 or offset > filtered_data.shape[0]:
          return jsonify({'message': 'Invalid offset value: limit is less than 0 or larger than length'}), 400
        filtered_data = filtered_data[offset:]

    return jsonify(filtered_data.to_dict(orient='records'))