#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from shapely.geometry import Polygon, mapping

app = Flask(__name__, static_url_path = "")

def coords_to_tuples_list(coords):
    """ Takes a list of lists, and converts it to a list of tuples"""
    op = []
    for lst in coords:
        op.append(tuple(lst))
    return op

def get_coords_list(json_in, entry_num):
    """ Extracts the coordinates list from a geojson standard formatted input"""
    return json_in['features'][entry_num]["geometry"]["coordinates"][0]

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

    coords1 = get_coords_list(request.json, 0)
    coords2 = get_coords_list(request.json, 1)

    op1 = coords_to_tuples_list(coords1)
    op2 = coords_to_tuples_list(coords2)

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
    
    coords1 = get_coords_list(request.json, 0)
    coords2 = get_coords_list(request.json, 1)

    op1 = coords_to_tuples_list(coords1)
    op2 = coords_to_tuples_list(coords2)

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