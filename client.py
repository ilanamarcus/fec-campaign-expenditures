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
        self.sort = "-disbursement_date"
        self.last_indexes = dict()
        self.params = params
        
        
    def next_page(self, last_indexes):
        self.last_indexes = last_indexes
        
    def get_params(self):
        base_params = {
                    'api_key': self.api_key,
                    'sort': self.sort,
                    'per_page': self.per_page
                }
        base_params.update(self.params)
        base_params.update(self.last_indexes)
        return base_params

class Client:
    def __init__(self):
        self.base_url = os.getenv("FEC_URL")
        
    def get_all_results(self, url, params):
        all_results = []
        payload = Payload(params)
        print("GET:", url, payload.get_params())
        resp=requests.get(url, params=payload.get_params())
        json = resp.json()
        results = json["results"]
        total_pages = json["pagination"]["pages"]
        print("Count:", json["pagination"]["count"], "Total pages:", total_pages, "Results length:", len(results))
        while len(results) > 0:
            all_results.extend(results)
            payload.next_page(json["pagination"]["last_indexes"])
            print("GET:", url, payload.get_params())
            json=requests.get(url, params=payload.get_params()).json()
            print("Results length:", len(json["results"]))
            results = json["results"]
        print("Retrieved", len(all_results), "records.")
        return all_results
        
    def disbursements_by_purpose(self, committee_id, params={}):
        url = "{}/committee/{}/schedules/schedule_b/by_purpose".format(
                self.base_url, committee_id)
        results=self.get_all_results(url, params)
        df = pd.DataFrame(results)
        return df
    
    def efile(self, committee_id, two_yr_period=2020, params={}):
        url = "{}/schedules/schedule_b".format(
                self.base_url)
        params["committee_id"] = [committee_id]
        params["two_year_transaction_period"] = two_yr_period
        results=self.get_all_results(url, params)
        df = pd.DataFrame(results)
        return df
        
    
                
                