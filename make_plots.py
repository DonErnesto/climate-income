import plotly.graph_objects as go
import pandas as pd

belgium_df = pd.read_csv(r'datasets/belgium.csv')
years = belgium_df['income decile'] #don't set as index. easier for now
y_payments = - belgium_df['carbon payment']
y_income = belgium_df['carbon revenue']
y_gain = belgium_df['net gain']

fig = go.Figure()
fig.add_trace(go.Bar(x=years,
                y=y_payments,
                name='Payments',
                marker_color='rgb(55, 83, 109)'
                ))
fig.add_trace(go.Bar(x=years,
                y=y_income,
                name='Income',
                marker_color='rgb(26, 118, 255)'
                ))
fig.add_trace(go.Bar(x=years,
                y=y_gain,
                name='Net gain',
                marker_color='rgb(180, 100, 20)'
                ))
fig.update_layout(
    title='Monthly carbon fee and carbon revenue',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.show()
