# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

class Payload:
    def __init__(self, params):
        self.api_key=os.getenv("KEY")
        self.page=1
        self.per_page=100
        self.params = params
        
    def next_page(self):
        self.page += 1
        
    def get_params(self):
        base_params = {
                    'api_key': self.api_key,
                    'page': self.page,
                    'per_page': self.per_page
                }
        base_params.update(self.params)
        return base_params

class Client:
    def __init__(self):
        self.base_url = os.getenv("FEC_URL")
        
    def get_all_results(self, url, params):
        payload = Payload(params)
        resp=requests.get(url, params=payload.get_params())
        resp_json = resp.json()
        results = resp_json["results"]
        total_pages = resp_json["pagination"]["pages"]
        if total_pages > 1:
            for i in range(total_pages):
                payload.next_page()
                json=requests.get(url, params=payload.get_params()).json()
                results.extend(json["results"])
        return results
        
    def disbursements_by_purpose(self, committee_id, params={}):
        url = "{}/committee/{}/schedules/schedule_b/by_purpose".format(
                self.base_url, committee_id)
        results=self.get_all_results(url, params)
        df = pd.DataFrame(results)
        return df
    
    def efile(self, committee_id, params={}):
        url = "{}/schedules/schedule_b/efile".format(
                self.base_url)
        params["committee_id"] = [committee_id]
        results=self.get_all_results(url, params)
        df = pd.DataFrame(results)
        return df
        
    
                
                