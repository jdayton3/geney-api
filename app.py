#!flask/bin/python
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/datasets')
def datasets():
    return "There are no datasets."

@app.route('/api/meta/<string:dataset_id>', methods=['GET'])
def meta(dataset_id):
    return "You input a dataset id: %s" % dataset_id

if __name__ == '__main__':
    app.run(debug=True)
