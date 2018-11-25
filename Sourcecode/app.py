import dash, plotly
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import statistics
import numpy as np
import plotly.graph_objs as go
import json



app = dash.Dash()

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

mapbox_access_token = "pk.eyJ1IjoiYWF0aGFuOTMiLCJhIjoiY2psdGVqdGhrMDVnaTNrbDgyZW9mZjBncSJ9.xQBdSA7YMBS_1Lnkj2nZ5Q"

for css in external_css:
    app.css.append_css({"external_url": css})

df = pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\leuchar.csv')


app.layout = html.Div([
	html.H2("Scotland Weather Data"),


	    dcc.Graph(
            id = "mapbox",
            figure={
                "data": [
                    dict(
                    	lat = ['56.38','57.593'],
                    	lon =  ['-2.88','-3.821'],
                        type = "scattermapbox",
                        customdata = df['tmax'],
                        mode = "markers",
                        marker = {'size': '14',},
                        text = ['leuchar','nairn']
                    )
                ],
                "layout": dict(
                    hovermode = "closest",
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    mapbox = dict(
                        accesstoken = mapbox_access_token,
                        center = dict(lat = 56.49, lon = -4.20),
                        style = "dark",
                        zoom = 6,
                        layers = []
                    )   
                )
            },
        ),
        html.Div([
            html.H4('Showing data for:'),
            dcc.RangeSlider(
                className = 'my-range-slider',
                id = 'my-range-slider',
                min = df['yyyy'].min(),
                max = df['yyyy'].max(),
                marks = {str(date): str(date)
                for date in df['yyyy'].unique()},
                value=[1970, 1993],
                ),
            html.Div([
                html.Div([html.H5('Max Temperature')], className='col-md-4'),
                html.Div([html.H5('Low Temperature')], className='col-md-4'),
                html.Div([html.H5('High Percipitation')], className='col-md-4'),
                ], className='row'),
            ], className='container-fluid'),


     html.Div([
     	html.H3('test', id='year-range'),
		], className='row'),

        html.Div([
        	html.Div([
        	dcc.Graph(
        		 id='temp_graph',
        		 config={'displayModeBar': False})], className='col-md-12'),
			html.Div([
				dcc.Graph(
					id='rain_graph',
					config={'displayModeBar': False})], className='col-md-12'),
			html.Div([
				dcc.Graph(
					id='sun_graph',
					config={'displayModeBar': False})], className='col-md-12'),
		], className='row')
	],  className='container-fluid')


@app.callback(
    Output('year-range', 'children'),
    [Input('mapbox', 'clickData')]
)

def showstation(clickData):
    point = clickData['points'][0]
    return pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\'+ point['text'] +'.csv')

# test = 'leuchar'

# df = pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\'+ test +'.csv')




@app.callback(
        Output('temp_graph', 'figure'),
        [Input('mapbox', 'clickData'),
         Input('my-range-slider', 'value')])

def update_graph(clickData, year_range):
    point = clickData['points'][0]
    df = pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\'+ point['text'] +'.csv')
    date_start = '{}'.format(year_range[0])
    date_end = '{}'.format(year_range[1])
    yearvalues = pd.date_range(start=date_start ,end=date_end,freq='M')
    string_dates = [str(x) for x in yearvalues]
    newdata = df.loc[(df['yyyy'] > int(date_start)) & (df['yyyy'] <= int(date_end)), ['tmax', 'tmin', 'sun', 'rain', 'af']] 
    string_tmax = [int(float(x)) for x in newdata['tmax']]
    string_tmin = [int(float(x)) for x in newdata['tmin']]
    data = np.array([string_tmax, string_tmin])
    average = np.average(data, axis=0)

    upper_bound = go.Scatter(
        name='High Temperature',
        x=string_dates,
        y=string_tmax,
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(68, 68, 68, 0.7)',
        fill='tonexty')

    trace = go.Scatter(
        name='average',
        x=string_dates,
        y=average,
        mode='lines',
        line=dict(color='rgb(255, 147, 41)'),
        fillcolor='rgba(68, 68, 68, 0.7)',
        fill='tonexty')

    lower_bound = go.Scatter(
        name='Low Temperature',
        x=string_dates,
        y=string_tmin,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines')

    return {
    'data': [lower_bound, trace, upper_bound],
    'layout': dict(plot_bgcolor='black', paper_bgcolor='black', title = 'Max and Low Temperatures in Leuchar',
              xaxis = dict(title = 'Year Range', gridcolor='rgba(0, 0, 0, 0.9)',),
              yaxis = dict(title = 'Temperature (degrees Celsius)',gridcolor='rgba(0, 0, 0, 0.9)',),
              font=dict(size=14, color='#7f7f7f'),
              )
	}


@app.callback(
        Output('rain_graph', 'figure'),
        [Input('mapbox', 'clickData'),
         Input('my-range-slider', 'value')])

def update_graph(clickData, year_range):

    date_start = '{}'.format(year_range[0])
    date_end = '{}'.format(year_range[1])
    yearvalues = pd.date_range(start=date_start ,end=date_end,freq='M')
    string_dates = [str(x) for x in yearvalues]
    newdata = df.loc[(df['yyyy'] > int(date_start)) & (df['yyyy'] <= int(date_end)), ['tmax', 'tmin', 'sun', 'rain', 'af']] 
    string_rain = [str(x) for x in newdata['rain']]

    trace1 = go.Bar(
    x=string_dates,
    y=string_rain,
    marker=dict(
        color='rgb(49,130,189)'
        )
    )

    return {
    'data': [trace1],
    'layout': dict(plot_bgcolor='black', paper_bgcolor='black', title = 'Percipitation in Leuchar',
              xaxis = dict(title = 'Year Range', gridcolor='black',),
              yaxis = dict(title = 'Rain (MM)',gridcolor='black',),
              font=dict(size=14, color='#7f7f7f'),

              )
    }

@app.callback(
        Output('sun_graph', 'figure'),
        [Input('mapbox', 'clickData'),
         Input('my-range-slider', 'value')])

def update_graph(clickData, year_range):

    date_start = '{}'.format(year_range[0])
    date_end = '{}'.format(year_range[1])
    yearvalues = pd.date_range(start=date_start ,end=date_end,freq='M')
    string_dates = [str(x) for x in yearvalues]
    newdata = df.loc[(df['yyyy'] > int(date_start)) & (df['yyyy'] <= int(date_end)), ['tmax', 'tmin', 'sun', 'rain', 'af']] 
    string_sun = [str(x) for x in newdata['sun']]
    string_af = [str(x) for x in newdata['af']]


    trace1 = go.Bar(
    x=string_dates,
    y=string_sun,
    name = 'Sunshine',
    marker=dict(
        color='rgb(237, 250, 98)'
        )
    )

    trace2 = go.Bar(
    x=string_dates,
    y=string_af,
    name = 'Air frost',
    marker=dict(
        color='red'
        )
    )

    return {
    'data': [trace1,trace2],
    'layout': dict(plot_bgcolor='black', paper_bgcolor='black', title = 'Total Monthly Sunshine & Air Frost in Leuchar',
              xaxis = dict(title = 'Year Range', gridcolor='black',),
              yaxis = dict(title = 'Sunshine hours',gridcolor='black',),
              font=dict(size=14, color='#7f7f7f'),

              )
    }


if __name__ == "__main__":
	app.run_server(debug=True)
