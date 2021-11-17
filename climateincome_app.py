import os
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# constants
local_grid = False
y_label = 'Outcome'
x_title, y_title = 'Transaction Volume', 'AUM'

#st.title('Country')
country = st.sidebar.selectbox('Country', ['belgium', 'uk'])
title_country_dict = {'belgium': 'Belgium',
                        'uk': 'UK'}

@st.cache
def load_data():
    file_name = os.path.join(r'datasets', f'{country}.csv')
    return pd.read_csv(file_name, index_col='income decile')

@st.cache
def load_metadata():
    file_name = os.path.join(r'datasets/raw', f'{country}.json')
    with open(file_name, "r") as jsonfile:
        return(json.load(jsonfile))




def plot_data(df, meta_data):
    #x = df['income decile'] #don't set as index. easier for now
    x = df.index
    y_payments = - df['carbon payment']
    y_income = df['carbon revenue']
    y_gain = df['net gain']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x,
                    y=y_payments,
                    name='Payments',
                    marker_color='rgb(180, 83, 20)'
                    ))
    fig.add_trace(go.Bar(x=x,
                    y=y_income,
                    name='Income',
                    marker_color='rgb(26, 180, 40)'
                    ))
    fig.add_trace(go.Bar(x=x,
                    y=y_gain,
                    name='Net gain',
                    marker_color='rgb(80, 100, 220)'
                    ))
    fig.update_layout(
        title=f'Yearly carbon fee and carbon revenue, {title_country_dict.get(country)}',
        titlefont_size=20,
        xaxis_tickfont_size=14,
        yaxis=dict(
            title=f"Payment/Revenue, {meta_data['price_unit']}/year",
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title="Income Decile"
        ),
        legend=dict(
            x=0,
            y=0.0,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    # fig.show()
    st.plotly_chart(fig)

#if st.checkbox('Show dataframe'):
chart_data = load_data()
meta_data = load_metadata()
plot_data(chart_data, meta_data)
meta_data['text']
meta_data['origin']
#chart_data
