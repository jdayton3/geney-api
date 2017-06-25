#!flask/bin/python
from flask import Flask, make_response, jsonify, request

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
        self.app.add_url_rule('/api/meta/<string:dataset_id>/metaType/<string:variable>',
                              view_func=self.meta_search,
                              methods=["GET"])
        self.app.register_error_handler(404, self.not_found)

    def not_found(self, error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def datasets(self):
        return jsonify(self.dao.get_datasets())

    def meta(self, dataset_id):
        return jsonify(self.dao.get_meta(dataset_id))

    def gene_search(self, dataset_id):
        search = request.args.get('search')
        return jsonify(self.dao.search_genes(search))

    def meta_search(self, dataset_id, variable):
        vals = self.dao.meta[dataset_id]["meta"][variable]["options"]
        search = request.args.get('search')
        return jsonify(
            [x for x in vals if search in x]
        )

if __name__ == '__main__':
    api = MyAPI()
    api.app.run(debug=True)
