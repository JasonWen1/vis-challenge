# coding:utf-8
import pandas as pd
import numpy as np
import plotly.graph_objs as go

_temp_data = pd.read_csv('temperature_daily.csv')
temp_data = pd.DataFrame(
    [
        [*map(int, row.get('date').split('-'))] + [row.get('max_temperature'), row.get('min_temperature')]
        for index, row in _temp_data.iterrows()
    ], columns=('year', 'month', 'day', 'max_temp', 'min_temp')
)

years = temp_data['year'].drop_duplicates()
months = temp_data['month'].drop_duplicates()

max_temp = np.zeros(shape=(len(months), len(years)), dtype=np.int)
min_temp = np.zeros(shape=(len(months), len(years)), dtype=np.int)
for _index, _row in temp_data.loc[:, 'year': 'month'].drop_duplicates().iterrows():
    _temp = temp_data[(temp_data['year'] == _row.year) & (temp_data['month'] == _row.month)]
    max_temp[_row.month - min(months), _row.year - min(years)] = max(_temp.max_temp)
    min_temp[_row.month - min(months), _row.year - min(years)] = min(_temp.min_temp)


def level1_update_graph(selected_temp_option):
    if selected_temp_option == 'max':
        map_data = max_temp
        hover_template = 'Year: %{x}\nMonth: %{y}\n Max: %{z}'
    else:
        map_data = min_temp
        hover_template = 'Year: %{x}\nMonth: %{y}\n Min: %{z}'

    data = [
        go.Heatmap(
            x=years, y=months, z=map_data, hovertemplate=hover_template,
            colorscale='YlOrRd', reversescale=True, name='', xgap=5, ygap=5
        ),
    ]
    layout = go.Layout(
        xaxis=dict(title='Year', showline=True),
        yaxis=dict(title='Month', showline=True),
        height=650, width=1000
    )
    return {'data': data, 'layout': layout}
