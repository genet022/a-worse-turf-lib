#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from shapely.geometry import Polygon, mapping

app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/digitalglobe/genet/intersection', methods = ['POST'])
def intersection():
    if not request.json:
        abort(400)

    # Grab list of list of coordinates
    coords1 = request.json['features'][0]["geometry"]["coordinates"][0]
    coords2 = request.json['features'][1]["geometry"]["coordinates"][0]

    op1 = []
    op2 = []
    # Convert list of list of coordinates to list of tuples
    for lst in coords1:
        op1.append(tuple(lst))
    for lst in coords2:
        op2.append(tuple(lst))

    poly1 = Polygon(op1)
    poly2 = Polygon(op2)

    # Calculate intersection of poly1 and poly2
    intersection = poly1.intersection(poly2)
    geojson_result = mapping(intersection)

    data = {
        "operation": "intersection",
        "result" : geojson_result
    }

    return jsonify( { 'data': data } ), 201

@app.route('/digitalglobe/genet/union', methods = ['POST'])
def union():
    if not request.json:
        abort(400)
    
    # Grab list of list of coordinates
    coords1 = request.json['features'][0]["geometry"]["coordinates"][0]
    coords2 = request.json['features'][1]["geometry"]["coordinates"][0]

    op1 = []
    op2 = []
    
    # Convert list of list of coordinates to list of tuples
    for lst in coords1:
        op1.append(tuple(lst))
    for lst in coords2:
        op2.append(tuple(lst))

    poly1 = Polygon(op1)
    poly2 = Polygon(op2)

    # Calculate union of poly1 and poly2
    union = poly1.union(poly2)
    geojson_result = mapping(union)

    data = {
        "operation": "union",
        "result" : geojson_result
    }

    return jsonify( { 'data': data } ), 201
    
if __name__ == '__main__':
    app.run(debug = True)