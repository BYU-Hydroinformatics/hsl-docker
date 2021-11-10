import sys
import urllib.request
import urllib.error
import json
import datetime
import random
import pandas as pd

class HS:
    def addSites():
        path_file = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]

        sites_df = pd.read_csv(path_file,header=0)
        sites_data = sites_df.to_dict('records')
        for data in sites_data:
            data['user'] = username
            data['password'] = password
            postdata = json.dumps(data)
            uploadURL = f'{data['uploadURL']}/sites'
            req = urllib.request.Request(uploadURL)
            req.add_header('Content-Type', 'application/json')
            try:
                response = urllib.request.urlopen(req, postdata)
                print response.read()
                continue
            except urllib.error.HTTPError, e:
                print e.code
                print e.msg
                print e.headers
                print e.fp.read()
                continue

if __name__ == "__main__":
    hydroservice = HS()
    hydroservice.addSites()
