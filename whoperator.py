import logging
from logging.handlers import RotatingFileHandler
from whoperator import app, log_file_path


log_file_handler = RotatingFileHandler(log_file_path, maxBytes=1024**2 * 100, backupCount=5)
log_file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_file_handler.setFormatter(formatter)

app.logger.addHandler(log_file_handler)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

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
