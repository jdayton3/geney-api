#!flask/bin/python
from flask import Flask, make_response, jsonify

# TODO: rename this class
class MyAPI:
    def __init__(self):
        self.app = Flask(__name__)
        thing = []
        self.app.add_url_rule('/api/datasets', 'datasets', self.datasets)
        self.app.add_url_rule('/api/meta/<string:dataset_id>', 'meta', self.meta)
        self.app.register_error_handler(404, self.not_found)
        #self.app.errorhandler(404)

    #@app.errorhandler(404)
    def not_found(self, error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    #@app.route('/api/datasets')
    def datasets(self):
        return jsonify([])

    #@app.route('/api/meta/<string:dataset_id>', methods=['GET'])
    def meta(self, dataset_id):
        return jsonify({"thing": "You input a dataset id: %s" % dataset_id})

if __name__ == '__main__':
    api = MyAPI()
    api.app.run(debug=True)
