#!flask/bin/python
from flask import Flask, make_response, jsonify

# TODO: rename this class
class MyAPI:
    def __init__(self, data_access_obj):
        self.dao = data_access_obj
        self.app = Flask(__name__)
        thing = []
        self.app.add_url_rule('/api/datasets',
                              view_func=self.datasets)
        self.app.add_url_rule('/api/meta/<string:dataset_id>',
                              view_func=self.meta)
        self.app.add_url_rule('/api/meta/<string:dataset_id>/gene', 
                              view_func=self.gene_search,
                              methods=["GET"])
        self.app.register_error_handler(404, self.not_found)
        #self.app.errorhandler(404)

    #@app.errorhandler(404)
    def not_found(self, error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    #@app.route('/api/datasets')
    def datasets(self):
        return jsonify(self.dao.get_datasets())

    #@app.route('/api/meta/<string:dataset_id>', methods=['GET'])
    def meta(self, dataset_id):
        return jsonify(self.dao.get_meta(dataset_id))

    def gene_search(self, dataset_id):
        return '["gene1", "gene2"]'

if __name__ == '__main__':
    api = MyAPI()
    api.app.run(debug=True)
