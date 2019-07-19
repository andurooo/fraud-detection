import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import json, requests

class DataPoint():

    def get_json(self, URL="http://galvanize-case-study-on-fraud.herokuapp.com/data_point"):

        self.name = name
        self.URL = URL 
        # URL  = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
        PARAMS = {'address':location} 

        r = requests.get(url = URL, params = PARAMS) 
        
        json_data = json.loads(r.text)
        print(len(json_data))
        return json_data

    def get_df(self, json_data):

        df = pd.DataFrame([json_data])

        return df

