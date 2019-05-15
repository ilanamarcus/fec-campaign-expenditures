#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 22:28:09 2019

@author: ilana
"""

from client import Client
import pandas as pd

def expense_cats(df):
    return df.groupby(["disbursement_description"])["disbursement_amount"].sum()

cmt_kamala="C00694455"
cmt_bernie="C00696948"
cmt_pete="C00697441"
cmt_beto="C00699090"
cmt_warren="C00693234"
cmt_klobuchar="C00696419"

c = Client()

kamala = c.efile(cmt_kamala)
bernie = c.efile(cmt_bernie)
pete = c.efile(cmt_pete)
beto = c.efile(cmt_beto)
warren = c.efile(cmt_warren)
klobuchar = c.efile(cmt_klobuchar)

expenses = {
            "kamala":expense_cats(kamala),
            "bernie":expense_cats(bernie),
            "pete":expense_cats(pete),
            "beto":expense_cats(beto),
            "warren":expense_cats(warren),
            "klobuchar":expense_cats(klobuchar)
        }

expense_df = pd.DataFrame.from_dict(expenses, orient="index")

import csv
cols = expense_df.columns
with open('cats_2.csv', 'w') as file:
    writer = csv.writer(file)
    for cat in cols:
        writer.writerow([cat])
    
