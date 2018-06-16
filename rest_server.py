#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__, static_url_path = "")
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

dataset = [
    {
        'id': 1,
        'title': u'Ari',
        'description': u'dog'
    },
    {
        'id': 2,
        'title': u'Frazier',
        'description': u'also dog'
    }
]

def make_public_data(data):
    """Instead of returning data ids, return the full URI that controls the data, so that clients get the URIs ready to be used
    """
    new_data = {}
    for field in data:
        if field == 'id':
            new_data['uri'] = url_for('get_data', data_id = data['id'], _external = True)
        else:
            new_data[field] = data[field]
    return new_data
    
@app.route('/digitalglobe/genet', methods = ['GET'])
def get_dataset():
    return jsonify( { 'dataset': map(make_public_data, dataset) } )

@app.route('/digitalglobe/genet/<int:data_id>', methods = ['GET'])
def get_data(data_id):
    data = filter(lambda d: d['id'] == data_id, dataset)
    if len(data) == 0:
        abort(404)
    return jsonify( { 'data': make_public_data(data[0]) } )

@app.route('/digitalglobe/genet', methods = ['POST'])
def create_data():
    if not request.json or not 'title' in request.json:
        abort(400)
    data = {
        'id': dataset[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }
    dataset.append(data)
    return jsonify( { 'data': make_public_data(data) } ), 201

@app.route('/digitalglobe/genet/<int:data_id>', methods = ['PUT'])
def update_data(data_id):
    data = filter(lambda d: d['id'] == data_id, dataset)
    if len(data) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    data[0]['title'] = request.json.get('title', data[0]['title'])
    data[0]['description'] = request.json.get('description', data[0]['description'])
    return jsonify( { 'data': make_public_data(data[0]) } )
    
@app.route('/digitalglobe/genet/<int:data_id>', methods = ['DELETE'])
def delete_data(data_id):
    data = filter(lambda d: d['id'] == data_id, dataset)
    if len(data) == 0:
        abort(404)
    dataset.remove(data[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)