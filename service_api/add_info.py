import sys
import urllib.request
import urllib.error
import json
import datetime
import random
import pandas as pd
import numpy as np
import asyncio
import aiohttp

# Use the following command #

# Use any of the options [sites,sources,variables,values,methods] as the first arg
# python add_info.py [sites,sources,variables,values,methods] url path_file username password

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
    # "VariableID": "Any VariableID",

class HS:

    # parameterized constructor to make easier the args in the functions
    def __init__(self,type_data,url,path_file,username,password):
        self.type_data = type_data
        self.url = url
        self.path_file = path_file
        self.username = username
        self.password = password

    # Single request
    async def get_single_request(self, session, uploadURL, postdata):
        try:
            async with session.post(uploadURL, data=postdata, ssl=False) as response:
                return await response.read()
        except Exception as e:
            return e, 'Error'


    async def bound_single_request(self,asyncio_semaphore, session, data):

        async with asyncio_semaphore:
            data['user'] = self.username
            data['password'] = self.password
            if self.type_data == 'values':

                values_df = pd.read_csv(data['file_path'],header=0)
                values_df.iloc[:, 0] = pd.to_datetime(values_df.iloc[:, 0])
                values_df.iloc[:, 0] = values_df.iloc[:, 0].dt.strftime("%Y-%m-%d %H:%M:%S")
                values = values_df.values.tolist()
                data['values'] = values

            postdata = json.dumps(data)
            uploadURL = f'{self.url}/{self.type_data}'
            return await self.get_single_request(session, uploadURL, postdata)

    # gather all the different requests
    def gather_data(self,data_list,session,asyncio_semaphore):
        re_list = []
        for data in data_list:
            try:
                sing_req = asyncio.ensure_future(self.bound_single_request(asyncio_semaphore, session, data))
                re_list.append(sing_req)
            except Exception as e:
                print (e.code)
                print (e.msg)
                print (e.headers)
                print (e.fp.read())
                continue
        return re_list

    async def get_data_values(self,data_list):
        results = []
        asyncio_semaphore = asyncio.Semaphore(100)
        timeout = aiohttp.ClientTimeout(total=1000)

        try:
            conn = aiohttp.TCPConnector(limit=100)

            async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            # async with aiohttp.ClientSession() as session:
                req_list = self.gather_data(data_list,session,asyncio_semaphore)
                responses = await asyncio.gather(*req_list)
                for response in responses:
                    print(response)
        except asyncio.TimeoutError as e:
            print (e)

    def addInformation(self):
        df = pd.read_csv(self.path_file,header=0)
        df = df.astype(object).replace(np.nan, 'None')
        data_list = df.to_dict('records')
        data_list = self.sortByRowNumber(data_list)
        return data_list

    # Sort list
    def sortByRowNumber(self,data_list):
        sorted_list = []
        unsorted_dict = {}
        if self.type_data == 'values':
            for data in data_list:
                values_df = pd.read_csv(data['file_path'],header=0)
                num_rows = values_df[values_df.columns[0]].count()
                unsorted_dict[num_rows] = data

            sorted_dict = dict(sorted(unsorted_dict.items()))
            print(sorted_dict)
            sorted_list = list(sorted_dict.values())
            return sorted_list

        return data_list


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

    hydroservice = HS(type_data,url,path_file,username,password)
    # hydroservice.addInformation(type_data, url, path_file, username, password)
    data_list = hydroservice.addInformation()
    # print(data_list)
    asyncio.run(hydroservice.get_data_values(data_list))
