import libs  # adds libs directory to path

from pygazelle.api import GazelleAPI

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from torrentwrangler import TorrentFileCollection

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


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


if __name__ == "__main__":
    app.run()

    # print "This script will check all of the .torrent files in a directory to see if they're available on What.cd."
    # username = raw_input("What is your what.cd username? ")
    # password = raw_input("What is your what.cd password? ")
    # testdir = raw_input("What directory would you like to check? ")
    # api = GazelleAPI(username=username, password=password)
    # for file_path, info_hash in TorrentFileCollection(testdir).list_files_and_info_hashes().iteritems():
    #     torrent = api.get_torrent_from_info_hash(info_hash)
    #     if torrent:
    #         print "%s exists on what.cd" % file_path
    #     else:
    #         print "%s doesn't exist on what.cd" % file_path
