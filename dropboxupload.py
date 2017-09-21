#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            #dbx.files_upload(f.read(), file_to)
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode('overwrite', None), autorename=False, client_modified=None, mute=False)

def main():
    # --load our API credentials
    config = {}
    execfile("/home/pi/git_code/python-twitter-examples/config.py", config)

    #----TODO: add access_token to above config file
    #access_token = 'W-PWCPYb80UAAAAAAAABTlqDbTSN9i-JpuldCmGGUgurUhGQo8Leq83agDQzqUyj'
    access_token = config["access_token"]

    transferData = TransferData(access_token)

    file_from = './outfile.out'
    file_to = '/kegstatus/outfile.out'  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

if __name__ == '__main__':
    main()
