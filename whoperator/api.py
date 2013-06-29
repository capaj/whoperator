from whoperator import app


### COLLECTION CRUD

@app.route('/collection/')
def list_collections():
    pass


@app.route('/collection/<int:collection_id>')
def show_collection(collection_id):
    pass


@app.route('/collection/', methods=['POST'])
def add_collection():
    pass


@app.route('/collection/<int:collection_id>', methods=['POST', 'PUT'])
def modify_collection(collection_id):
    pass


@app.route('/collection/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    pass


### ITEM CRUD

@app.route('/collection/<int:collection_id>/item')
def list_collection_items(collection_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>')
def show_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/', methods=['POST'])
def add_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['POST', 'PUT'])
def modify_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['DELETE'])
def delete_collection_item(collection_id, item_id):
    pass
