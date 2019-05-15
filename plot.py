#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:37:53 2019

@author: ilana
"""
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

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
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='cand-expenses')

#
#trace1 = go.Bar(
#    x=['giraffes', 'orangutans', 'monkeys'],
#    y=[20, 14, 23],
#    name='SF Zoo'
#)
#trace2 = go.Bar(
#    x=['giraffes', 'orangutans', 'monkeys'],
#    y=[12, 18, 29],
#    name='LA Zoo'
#)
#
#data = [trace1, trace2]
#layout = go.Layout(
#    barmode='group'
#)
#
#fig = go.Figure(data=data, layout=layout)
#py.iplot(fig, filename='grouped-bar')