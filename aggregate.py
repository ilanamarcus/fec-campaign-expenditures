#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 22:28:09 2019

@author: ilana
"""

from client import Client
import pandas as pd
import functools

#committee id's
cmt_kamala="C00694455"
cmt_bernie="C00696948"
cmt_pete="C00697441"
cmt_beto="C00699090"
cmt_warren="C00693234"
cmt_klobuchar="C00696419"

committee_ids = [cmt_kamala, cmt_bernie, cmt_pete, cmt_beto, cmt_warren, cmt_klobuchar]

#get data from API
c = Client()

kamala = c.efile(cmt_kamala)
bernie = c.efile(cmt_bernie)
pete = c.efile(cmt_pete)
beto = c.efile(cmt_beto)
warren = c.efile(cmt_warren)
klobuchar = c.efile(cmt_klobuchar)

#one dataframe
all_filings = kamala.append([bernie, pete, beto, warren, klobuchar])
all_filings.to_csv("all_filings.csv")

def expense_cats(df, committee_id, cats): 
    df = df[df["committee_id"] == committee_id]
    df = df.merge(cats, how='left')
    print(df.columns)
    df = df.groupby(["expense_category"])["disbursement_amount"].sum()
    #df.reset_index(inplace=True)
    return df

#map committee id's to candidate name
cmt_to_name = {
    cmt_kamala: "Kamala",
    cmt_bernie: "Bernie",
    cmt_pete: "Pete",
    cmt_beto: "Beto",
    cmt_warren: "Warren",
    cmt_klobuchar: "Klobuchar"
}

#remove reimbursements that are also itemized
filings = pd.read_csv("all_filings.csv")
sub_transactions = filings[~filings["back_reference_transaction_id"].isna()]
items = sub_transactions[sub_transactions["back_reference_schedule_id"].str.strip() == "SB23"]
reimb_trans_ids = list(items["back_reference_transaction_id"].unique())
reimb_trans_str_ids = [str(int(id)) for id in reimb_trans_ids]
filings = filings[~filings["transaction_id"].isin(reimb_trans_str_ids)]
filings["disbursement_description"] = filings["disbursement_description"].str.lower()
filings.to_csv("actual_filings.csv")

cats = pd.read_csv("cats.csv")
cats.columns = ["disbursement_description", "expense_category"]
cats["disbursement_description"] = cats["disbursement_description"].str.lower()
expenses = {
            cmt_to_name[cmt_kamala]:expense_cats(filings, cmt_kamala, cats),
            cmt_to_name[cmt_bernie]:expense_cats(filings, cmt_bernie, cats),
            cmt_to_name[cmt_pete]:expense_cats(filings, cmt_pete, cats),
            cmt_to_name[cmt_beto]:expense_cats(filings, cmt_beto, cats),
            cmt_to_name[cmt_warren]:expense_cats(filings, cmt_warren, cats),
            cmt_to_name[cmt_klobuchar]:expense_cats(filings, cmt_klobuchar, cats)
        }


expense_df = pd.DataFrame.from_dict(expenses, orient="index")
expense_df.to_csv("candidate_expenses.csv")

#sum expenditures by candidate
grouped = filings.groupby("committee_id")[["disbursement_amount"]].agg('sum')
grouped.reset_index(inplace=True)
grouped["name"] = grouped["committee_id"].apply(lambda x: cmt_to_name[x])

#How much did each candiate refund?
refunds = filings[filings["line_number"] == "28A"]
refunds = refunds.groupby("committee_id")[["disbursement_amount"]].agg(['sum', 'count'])
refunds.reset_index(inplace=True)
refunds["name"] = refunds["committee_id"].apply(lambda x: cmt_to_name[x])
refunds.columns = ["committee_id", "disbursement_amount", "refund_count", "name"]
refunds.set_index('name', inplace=True)
refunds.to_csv("refunds.csv", header=True, index=True)

#Did anyone get refunded by the same candidate? No
refundees = filings[filings["line_number"] == "28A"]
refundees = refundees.groupby(["recipient_name", "committee_id"])["disbursement_amount"].agg('count')
