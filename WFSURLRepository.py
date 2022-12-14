
# import urllib library
from urllib.request import urlopen
# importing module
from pandas import *
import pandas as pd
# import json
import json
from models import db,ODLModel
import sqlalchemy as db
from URLmodels import ODL

from sqlalchemy.orm import Session

engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
connection = engine.connect()
metadata = db.MetaData()

 
# reading CSV file
data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations.csv")
 
# converting column data to list
loc_Codes = data['locality_code'].tolist()

def WFSURL():
    # store the URL in url as 
    # parameter for urlopen
    for id in loc_Codes:
        try:
            url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_odl_brutto_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+id+"%27%20AND%20end_measure%3E%272021-01-01T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%272022-12-31T00%3A00%3A00.000Z%27"
        
            # store the response of URL
            response = urlopen(url)       
            # storing the JSON response 
            # from url in data
            data_json = json.loads(response.read())
            datanorm= pd.json_normalize(data_json,"features")
            #df1 = pd.DataFrame(datanorm)
            #return(datanorm)
            with Session(engine) as session:
                #datanorm = WFSURL()
                #my_list = []
                for index in range(len(datanorm)):
                    new_ODL = ODL(
                        Locality_code=datanorm['properties.id'][index], 
                        Value=datanorm['properties.value'][index],
                        Start_measure=datanorm['properties.start'][index],
                        End_measure=datanorm['properties.end_measure'][index]
                        )
                    session.add(new_ODL) 
                session.commit()
        except:
            print("An exception occurred")
WFSURL()