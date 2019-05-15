#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 22:28:09 2019

@author: ilana
"""

from client import Client
import pandas as pd

def expense_cats(df, cats): 
    df = df.merge(cats, how='left')
    print(df.columns)
    df = df.groupby(["expense_category"])["disbursement_amount"].sum()
    #df.reset_index(inplace=True)
    return df

cmt_to_name = {
    "C00694455": "Kamala",
    "C00696948": "Bernie",
    "C00697441": "Pete",
    "C00699090": "Beto",
    "C00693234": "Warren",
    "C00696419": "Klobuchar"
}

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

all_filings = kamala.append([bernie, pete, beto, warren, klobuchar])
all_filings.to_csv("all_filings.csv")

cats = pd.read_csv("cats.csv")
cats.columns = ["disbursement_description", "expense_category"]
expenses = {
            "kamala":expense_cats(kamala, cats),
            "bernie":expense_cats(bernie, cats),
            "pete":expense_cats(pete, cats),
            "beto":expense_cats(beto, cats),
            "warren":expense_cats(warren, cats),
            "klobuchar":expense_cats(klobuchar, cats)
        }


expense_df = pd.DataFrame.from_dict(expenses, orient="index")
expense_df.to_csv("candidate_expenses.csv")




