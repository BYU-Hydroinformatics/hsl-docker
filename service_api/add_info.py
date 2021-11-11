import sys
import urllib.request
import urllib.error
import json
import datetime
import random
import pandas as pd
import numpy as np


# Use the following command #

# Use any of the options [sites,sources,variables,values,methods] as the first arg
# python add_info.py [sites,sources,variables,data_values,methods] url path_file username password

# Use the folliwing order when adding data for the first time #
# first upload Sources
# second upload Sites
# third upload Variables
# fourth upload DataValues

# If you get any error, refer to it and go to the mysql database if you need further reference.

# To add Sites Make sure you have the following columns #

    # SourceID,SiteName,SiteCode,Latitude,Longitude,
    # SiteType,Elevation_m,Comments

    # Example

    # "SiteID": 35,
    # "SiteName": "siteName",
    # "SiteCode": "site1ID",
    # "Latitude": 46.535,
    # "Longitude": 15.2366,
    # "SiteType": "Atmosphere",
    # "Elevation_m": 256,
    # "Comments": "site uploaded from Python"

    # Please check the posible sitetypes uisng the following command:

    # Select * FROM sitetypecv;


# To add Variables Make sure you have the following columns #

    # VariableCode,VariableName,Speciation,VariableUnitsID,
    # SampleMedium,ValueType,IsRegular,TimeSupport
    # TimeUnitsID,DataType,GeneralCategory,NoDataValue

    # Example

    # "VariableCode": "var1ID",
    # "VariableName": "Color",
    # "Speciation": "Not Applicable",
    # "VariableUnitsID": 189,
    # "SampleMedium": "Surface Water",
    # "ValueType": "Sample",
    # "IsRegular": 1,
    # "TimeSupport": 0,
    # "TimeUnitsID": 100,
    # "DataType": "Average",
    # "GeneralCategory": "Hydrology",
    # "NoDataValue": -9999

# To add Sources Make sure you have the following columns #
    # organization,descriptionlink,name, phone
    # email,address,city,state,zipcode,citation,metadata

    # Example

    # "organization": "python source organization",
    # "description": "uploaded from python:",
    # "link": "http://example.com",
    # "name": "Source name",
    # "phone": "012-345-6789",
    # "email": "test@gmail.com",
    # "address": "any addres",
    # "city": "any city",
    # "state": "any state",
    # "zipcode": "any zipcode",
    # "citation": "uploaded from python as a test",
    # "metadata": 10

    # You need to check the metadata values that already exits in the isometadata table by using the following.
    # Select * FROM isometadata;
    # you need to go inside the container for this and activate mysql


# To add DataValues Make sure you have the following columns #

    # SiteID,VariableID,MethodID,SourceID,file_path

    # "SiteID": "Any siteID",
    # "VariableID": "Any variableID",
    # "MethodID": "Any methodID",
    # "SourceID": "Any sourceID",
    # "file_path": "/path/to/file/containing/data/for/the/variable"

    # The file from the file_path shuld have the date column called "LocalDateTime"


# To add Methods Make sure you have the following columns #

    # MethodDescription,MethodLink,VariableID

    # "MethodDescription": "Any MethodDescription",
    # "MethodLink": "Any MethodLink",
    # "MethodID": "Any MethodID",

class HS:
    def addInformation(self, type_data, url, path_file, username, password):
        df = pd.read_csv(path_file,header=0)
        df = df.astype(object).replace(np.nan, 'None')
        print(df)
        data_list = df.to_dict('records')
        print(data_list)
        for data in data_list:
            data['user'] = username
            data['password'] = password
            if type_data == 'values':
                values_df = pd.read_csv(data['file_path'],header=0)
                values_df['LocalDateTime'] = pd.to_datetime(values_df['LocalDateTime'])
                values_df['LocalDateTime'] = values_df['LocalDateTime'].dt.strftime("%Y-%m-%d %H:%M:%S")
                print(values_df)
                # values = list(values_df.to_records(index=False))
                values = values_df.values.tolist()
                data['values'] = values
                # print(data['values'])

            postdata = json.dumps(data)
            uploadURL = f'{url}/{type_data}'
            req = urllib.request.Request(uploadURL)
            req.add_header('Content-Type', 'application/json')
            try:
                response = urllib.request.urlopen(req, postdata.encode('utf-8'))
                print (response.read())
                continue
            except urllib.error.HTTPError as e:
                print (e.code)
                print (e.msg)
                print (e.headers)
                print (e.fp.read())
                continue

if __name__ == "__main__":
    try:
        type_data = sys.argv[1]
    except IndexError:
        print("You need to provide a type_data: sites, values, variables, sources")
        sys.exit(1)
    try:
        url = sys.argv[2]
    except IndexError:
        print("You need to provide a type_data: sites, values, variables, sources")
        sys.exit(1)
    try:
        path_file = sys.argv[3]
    except IndexError:
        print("You need to provide a file path containing the data to add to the database")
        sys.exit(1)
    try:
        username = sys.argv[4]
    except IndexError:
        print("You need to provide the username for the HydroServerLite Account")
        sys.exit(1)
    try:
        password = sys.argv[5]
    except IndexError:
        print("You need to provide a password for the HydroServerLite Account")
        sys.exit(1)

    hydroservice = HS()
    hydroservice.addInformation(type_data, url, path_file, username, password)
