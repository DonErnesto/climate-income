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

# titles

#st.title('Country')
st_country = st.sidebar.selectbox('Country', ['belgium', 'uk'])
st_deciles_quintiles = st.sidebar.selectbox('Quantiles', ['deciles', 'quintiles'])
st_orientation = st.sidebar.selectbox('Orientation', ['horizontal', 'vertical'])
st_plot_type = st.sidebar.selectbox('Plot type', ['bars', 'bars and line'])


st_reverse_quantiles = st.sidebar.checkbox('Reverse quantile ordering')
st_payment_negative = st.sidebar.checkbox('Plot payments as negative values')
orientation = {'horizonal':'h',
                'vertical': 'v'}.get(st_orientation, 'h')

title_country_dict = {'belgium': 'Belgium',
                        'uk': 'UK'}
xlabel_quantile_dict = {'deciles': 'Income Decile',
                        'quintiles': 'Income Quintile'}
@st.cache
def load_data():
    file_name = os.path.join(r'datasets', f'{st_country}.csv')
    return pd.read_csv(file_name) #pd.read_csv(file_name, index_col='income decile')

@st.cache
def load_metadata():
    file_name = os.path.join(r'datasets/raw', f'{st_country}.json')
    with open(file_name, "r") as jsonfile:
        return(json.load(jsonfile))

def change_to_quintiles(df):
    df = df.groupby(np.arange(10)//2).mean()
    df['income decile'] = np.arange(1, 6)
    return df

def make_barplot(df, meta_data, orientation='h', payment_negative=st_payment_negative):
    #df = df.sort_values('income decile', ascending=True)
    bargroupgap = 0.15
    idx = df['income decile']
    col_list = ['carbon payment', 'carbon revenue', 'net gain']
    name_list = ['Payment', 'Revenue', 'Net gain']
    rgb_list = ['rgb(180, 100, 100)', 'rgb(100, 180, 100)', 'rgb(80, 100, 180)']

    money_title, quantile_title = (f"Payment/Revenue ({meta_data['price_unit']}/year)",
                                    xlabel_quantile_dict[st_deciles_quintiles])
    x_axis_title = money_title if orientation == 'h' else quantile_title
    y_axis_title = quantile_title if orientation == 'h' else money_title

    fig = go.Figure()

    for col, rgb, name in zip(col_list, rgb_list, name_list):
        if orientation == 'v':
            x = idx
            if payment_negative and col == 'carbon payment':
                y = - df[col]
            else:
                y = df[col]
        else:
            y = idx
            if payment_negative and col == 'carbon payment':
                x = - df[col]
            else:
                x = df[col]
        fig.add_trace(go.Bar(x=x,
                        y=y,
                        name=name,
                        marker_color=rgb,
                        orientation=orientation
                        ))
    fig.update_traces(width=0.25)

    # fig.show()
    #fig.update_yaxes(categoryorder='array', categoryarray=np.arange(1, 6))
    if st_reverse_quantiles:
        if orientation == 'h':
            fig.update_yaxes(autorange="reversed")
        else:
            fig.update_xaxes(autorange="reversed")

    annotations = []
    space = 0
    for col_i, col in enumerate(col_list):

        for i in range(0, len(idx)):
            # labeling the rest of percentages for each bar (x_axis)
            if orientation == 'h':
                if col == 'carbon payment' and payment_negative:
                    x_loc = - df.iloc[i, :][col]
                else:
                    x_loc = df.iloc[i][col]

                y_loc = df.iloc[i, :]['income decile'] + (col_i - 1) * (bargroupgap + 0.125)
                value = x_loc
                x_loc = 0.5 * x_loc # placement of number in bar
            else:
                if col == 'carbon payment' and payment_negative:
                    y_loc = - df.iloc[i, :][col]
                else:
                    y_loc = df.iloc[i][col]

                x_loc = df.iloc[i, :]['income decile'] + (col_i - 1) * (bargroupgap + 0.125)
                value = y_loc
                y_loc = 0.5* y_loc  # placement of number in bar
            annotations.append(dict(xref='x', yref='y',
                                    x=space + x_loc, y=y_loc,
                                    text= f'{value:.0f}' ,
                                    font=dict(family='Arial', size=14,
                                              color='rgb(240, 240, 250)'),
                                    showarrow=False))
    fig.update_layout(annotations=annotations)
    fig.update_layout(
        title=dict(
            text=f'Yearly carbon fee and carbon revenue, {title_country_dict.get(st_country)}',
            xanchor='center',
            x=0.5,
        ),
        titlefont_size=20,
        yaxis=dict(
            title=y_axis_title,
            titlefont_size=16,
            tickfont_size=14
        ),
        xaxis=dict(
            title=x_axis_title,
            titlefont_size=16,
        ),
        legend=dict(
            x=1.0,
            y=1.05,
            bgcolor='rgba(200, 200, 210, 0.15)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=bargroupgap, # gap between bars of the same location coordinate.,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(200, 220, 220)'
    )
    st.plotly_chart(fig)



def make_bar_lineplot(df, meta_data, orientation='h', payment_negative=st_payment_negative):
    #df = df.sort_values('income decile', ascending=True)
    bargroupgap = 0.15
    idx = df['income decile']
    col_list = ['carbon revenue', 'carbon payment', 'net gain']
    name_list = ['Revenue', 'Payment', 'Net gain']
    rgb_list = ['rgb(100, 180, 100)', 'rgb(180, 100, 100)',  'rgb(80, 100, 180)']

    money_title, quantile_title = (f"Payment/Revenue ({meta_data['price_unit']}/year)",
                                    xlabel_quantile_dict[st_deciles_quintiles])
    x_axis_title = money_title if orientation == 'h' else quantile_title
    y_axis_title = quantile_title if orientation == 'h' else money_title

    fig = go.Figure()

    for col, rgb, name in zip(col_list, rgb_list, name_list):
        if orientation == 'v':
            x = idx
            if payment_negative and col == 'carbon payment':
                y = - df[col]
            else:
                y = df[col]
        else:
            y = idx
            if payment_negative and col == 'carbon payment':
                x = - df[col]
            else:
                x = df[col]
        if col =='carbon revenue':
            if orientation == 'v':
                x_min = x.min() - 0.5
                x_max = x.max() + 0.5
                y_min = y.min()
                y_max = y.max()

            else:
                x_min = x.min()
                x_max = x.max()
                y_min = y.min() - 0.5
                y_max = y.max() + 0.5
            fig.add_trace(go.Scatter(x=[x_min, x_max],
                            y=[y_min, y_max],
                            name=name,
                            orientation=orientation,
                            line_color=rgb,
                            #text = ['carbon revenue'] + ['']*(len(df)-1),
                            marker=dict(size=1),
                            mode='lines+markers'
                            ))
        else:
            fig.add_trace(go.Bar(x=x,
                            y=y,
                            name=name,
                            marker_color=rgb,
                            orientation=orientation,
                            width=0.4
                            ))


    # fig.show()
    #fig.update_yaxes(categoryorder='array', categoryarray=np.arange(1, 6))
    if st_reverse_quantiles:
        if orientation == 'h':
            fig.update_yaxes(autorange="reversed")
        else:
            fig.update_xaxes(autorange="reversed")

    annotations = []
    space = 0
    for col_i, col in enumerate([col_list[1], col_list[2]]):
        for i in range(0, len(idx)):
            # labeling the rest of percentages for each bar (x_axis)
            if orientation == 'h':
                if col == 'carbon payment' and payment_negative:
                    x_loc = - df.iloc[i, :][col]
                else:
                    x_loc = df.iloc[i][col]

                y_loc = df.iloc[i, :]['income decile'] + (col_i - 0.5) * (bargroupgap + 0.2)
                value = x_loc
                x_loc = 0.5 * x_loc # placement of number in bar
            else:
                if col == 'carbon payment' and payment_negative:
                    y_loc = - df.iloc[i, :][col]
                else:
                    y_loc = df.iloc[i][col]

                x_loc = df.iloc[i, :]['income decile'] + (col_i - 0.5) * (bargroupgap + 0.2)
                value = y_loc
                y_loc = 0.5* y_loc  # placement of number in bar
            annotations.append(dict(xref='x', yref='y',
                                    x=space + x_loc, y=y_loc,
                                    text= f'{value:.0f}' ,
                                    font=dict(family='Arial', size=14,
                                              color='rgb(240, 240, 250)'),
                                    showarrow=False))
    # add line text
    col_i, col = 0, col_list[0]
    if orientation == 'h':
        x_loc = 1.05 * df.loc[:, col].mean()
        y_loc = idx.mean()
        value = x_loc
        textangle = 90
    else:
        y_loc = 1.05* df.loc[:, col].mean()
        x_loc = idx.mean()
        value = y_loc
        textangle = 0
    annotations.append(dict(xref='x', yref='y',
                            x=space + x_loc, y=y_loc,
                            text= f'revenue: {value:.0f}',
                            font=dict(family='Arial', size=14,
                                      color="rgb(240, 250, 240)"),
                            showarrow=False,
                            textangle=textangle,
                            bgcolor="rgb(10, 100, 10)",
                            opacity=0.5
                            ))


    fig.update_layout(annotations=annotations)
    fig.update_layout(
        title=dict(
            text=f'Yearly carbon fee and carbon revenue, {title_country_dict.get(st_country)}',
            xanchor='center',
            x=0.5,
        ),
        titlefont_size=20,
        yaxis=dict(
            title=y_axis_title,
            titlefont_size=16,
            tickfont_size=14
        ),
        xaxis=dict(
            title=x_axis_title,
            titlefont_size=16,
        ),
        legend=dict(
            x=1.0,
            y=1.05,
            bgcolor='rgba(200, 200, 210, 0.15)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=bargroupgap, # gap between bars of the same location coordinate.,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(200, 220, 220)'
    )
    st.plotly_chart(fig)


def plot_data(df, meta_data):
    idx_list = df.index

    #x = df['income decile'] #don't set as index. easier for now
    x = df.index
    y_payments = - df['carbon payment']
    y_income = df['carbon revenue']
    y_gain = df['net gain']
    fig = go.Figure()
    fig.add_trace(go.Bar(y=x,
                    x=y_payments,
                    name='Payments',
                    marker_color='rgb(180, 83, 20)',
                    orientation='h'
                    ))
    fig.add_trace(go.Bar(y=x,
                    x=y_income,
                    name='Income',
                    marker_color='rgb(26, 180, 40)',
                    orientation='h'
                    ))
    fig.add_trace(go.Bar(y=x,
                    x=y_gain,
                    name='Net gain',
                    marker_color='rgb(80, 100, 220)',
                    orientation='h'
                    ))
    fig.update_layout(
        title=dict(
            text=f'Yearly carbon fee and carbon revenue, {title_country_dict.get(country)}'
            ),
        xaxis_tickfont_size=20,
        yaxis_tickfont_size=20,
        yaxis_title = f"Payment/Revenue, {meta_data['price_unit']}/year",
        xaxis_title=xlabel_quantile_dict[st_deciles_quintiles],
        legend=dict(
            x=0,
            y=0.0,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.05 # gap between bars of the same location coordinate.
    )
    # fig.show()
    st.plotly_chart(fig)

#if st.checkbox('Show dataframe'):
chart_data = load_data()
if st_deciles_quintiles == 'quintiles':
    chart_data = change_to_quintiles(chart_data)
meta_data = load_metadata()

if st_plot_type == 'bars':
    make_barplot(chart_data, meta_data, orientation=orientation)
else:
    make_bar_lineplot(chart_data, meta_data, orientation=orientation)
meta_data['text']
meta_data['origin']
