#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:37:53 2019

@author: ilana
"""
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import re
import math
from aggregate import cmt_to_name

def plot_expense_categories():
    cand_expenses = pd.read_csv("candidate_expenses.csv", index_col=0)
    data = []
    for col in cand_expenses.columns:
        trace = go.Bar(
            x= list(cand_expenses.index),
            y= cand_expenses[col],
            name=col
        )
        data.append(trace)
        
    layout = go.Layout(
        title=go.layout.Title(
            text='Campaign expenditures by candidate and category'
        ),
        barmode='group'
    )
    
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='cand-expenses')

def plot_airlines():
    all_filings = pd.read_csv("actual_filings.csv")
    airfare = all_filings[all_filings["recipient_name"].str.contains('Airline', flags = re.IGNORECASE)]
    airfare.loc[:, "recipient_name"] = airfare["recipient_name"].apply(lambda x: x.split(',',1)[0])
    airfare = airfare.groupby("recipient_name")["disbursement_amount"].agg(['count', 'sum'])
    
    count_trace = go.Bar(
        x = list(airfare.index),
        y = airfare["count"],
        name = "Number of filings",
        yaxis = 'y2'
    )
    
    sum_trace = go.Bar(
        x = list(airfare.index),
        y = airfare["sum"],
        name = "Amount spent",
        xaxis= 'x1',
        yaxis = 'y1'        
    )
    
    trace1 = go.Bar(x = list(airfare.index), y=[0],showlegend=False,hoverinfo='none')
    trace2 = go.Bar(x = list(airfare.index), y=[0], yaxis='y2',showlegend=False,hoverinfo='none') 
    
    data = [sum_trace, trace1, trace2, count_trace]
    layout = go.Layout(
        title=go.layout.Title(
            text='Campaign expenditures by airline'
        ),
        barmode='group',
        yaxis=dict(
            range=[0,math.ceil(max(airfare["sum"]))],
            title='Amount spent'
        ),
        yaxis2=dict(
            range= [0, 500],
            title='Number of filings',
            overlaying='y',
            side='right'
        )
    )
    
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='airfare')
    
def plot_rideshare():
    all_filings = pd.read_csv("actual_filings.csv")
    rideshare = all_filings[all_filings["recipient_name"].str.contains('^uber|^lyft', flags = re.IGNORECASE)]
    rideshare["candidate_name"] = rideshare["committee_id"].apply(lambda x: cmt_to_name[x])
    rideshare.loc[:, "recipient_name"] = rideshare["recipient_name"].apply(lambda x: x.replace(',',' ').split(' ',1)[0])
    rideshare = rideshare.groupby(["candidate_name", "recipient_name"])[["disbursement_amount"]].sum()
    
    for k in cmt_to_name.keys():
        uber = (cmt_to_name[k], "Uber")
        lyft = (cmt_to_name[k], "Lyft")
        
        if not rideshare.index.isin([uber]).any():
            #add row
            rideshare.loc[uber,"disbursement_amount"] = 0
        if not rideshare.index.isin([lyft]).any():
            #add row
            rideshare.loc[lyft,"disbursement_amount"] = 0
    rideshare.reset_index(inplace=True)
    rideshare = rideshare.pivot_table(index="candidate_name", columns="recipient_name", values="disbursement_amount")
    
    uber_trace = go.Bar(
            x= list(rideshare.index),
            y= rideshare["Uber"],
            name="Spent on Uber"
    )
    
    lyft_trace = go.Bar(
            x= list(rideshare.index),
            y= rideshare["Lyft"],
            name="Spent on Lyft"
    )
    
    data = [uber_trace, lyft_trace]
    layout = go.Layout(
        title=go.layout.Title(
            text='Money spent on rideshares by candidate'
        ),
        barmode='group'
    )
    
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='rideshares')

plot_expense_categories()    
plot_airlines()
plot_rideshare()
    
    
    
    
