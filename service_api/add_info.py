import sys
import urllib.request
import urllib.error
import json
import datetime
import random
import pandas as pd

class HS:
    def addInformation(type_data,path_file,username,password):

        df = pd.read_csv(path_file,header=0)
        data_list = df.to_dict('records')
        for data in data_list:
            data['user'] = username
            data['password'] = password
            if type_data == 'values':
                values_df = pd.read_csv(data['file_path'],header=0)
                values_df['dates'] = values_df['dates'].dt.strftime("%Y-%m-%d %H:%M:%S")
                values = list(values_df.values.to_records(index=False))
                data['values'] = values

            postdata = json.dumps(data)
            uploadURL = f'{data['uploadURL']}/{type_data}'
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
    try:
        type_data = sys.argv[1]
    except IndexError:
        print("You need to provide a type_data: sites, values, variables, sources")
        sys.exit(1)
    try:
        path_file = sys.argv[2]
    except IndexError:
        print("You need to provide a file path containing the data to add to the database")
        sys.exit(1)
    try:
        username = sys.argv[3]
    except IndexError:
        print("You need to provide the username for the HydroServerLite Account")
        sys.exit(1)
    try:
        password = sys.argv[4]
    except IndexError:
        print("You need to provide a password for the HydroServerLite Account")
        sys.exit(1)

    hydroservice = HS()
    hydroservice.addInformation(type_data,path_file,username,password)
