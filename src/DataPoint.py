import pandas as pd
import json, requests

class DataPoint():

    def __init__(self):
        self.get_json()
        self.get_df()
    
    def get_json(self, URL="http://galvanize-case-study-on-fraud.herokuapp.com/data_point"):

        self.URL = URL 
        # URL  = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
        #location = "dehli technological university"
        #PARAMS = {'address':location} 

        r = requests.get(url = URL) 
        
        self.json_data = json.loads(r.text)


    def get_df(self):

        self.df = pd.DataFrame([self.json_data])

