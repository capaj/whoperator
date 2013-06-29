from whoperator import app


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
