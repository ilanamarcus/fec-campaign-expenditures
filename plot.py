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
    all_filings = pd.read_csv("all_filings.csv")
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

plot_expense_categories()    
plot_airlines()

    
    
    
    
