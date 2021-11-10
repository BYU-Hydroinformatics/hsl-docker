import sys
import urllib.request
import urllib.error
import json
import datetime
import random
import pandas as pd

class HS:
    def addValues():
        with open(sys.argv[1]) as json_data:
            try:
                data = json.load(json_data)
            except Exception as e:
                print(e)
                return
        username = sys.argv[2]
        password = sys.argv[3]
        sourceID = data['sourceID']
        variableID = data['variableID']
        siteID = data['siteID']
        methodID = data['methodID']
        values_file_path = data['values']
        values_df = pd.read_csv(values_file_path,header=0)
        values_df['dates'] = values_df['dates'].dt.strftime("%Y-%m-%d %H:%M:%S")
        values = list(values_df.values.to_records(index=False))

        data = {
            "user": username,
            "password": password,
            "SiteID": siteID,
            "VariableID": variableID,
            "MethodID": methodID,
            "SourceID": sourceID,
            "values": values
        }

        postdata = json.dumps(data)
        uploadURL = f'{data['uploadURL']}/values'
        req = urllib.request.Request(uploadURL)
        req.add_header('Content-Type', 'application/json')
        try:
            response = urllib.request.urlopen(req, postdata)
            print response.read()
            return
        except urllib.error.HTTPError, e:
            print e.code
            print e.msg
            print e.headers
            print e.fp.read()
            return

if __name__ == "__main__":
    hydroservice = HS()
    hydroservice.addValues()
