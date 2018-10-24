import dash, plotly
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
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
# df.sort_values(by=['yyyy'])

string_tmax = [str(x) for x in df['tmin']]

print(df)


# dfmax = df['tmax'].groupby(df['yyyy']).describe()







app.layout = html.Div([
	html.H2("Scotland Weather Data"),


	    dcc.Graph(
            id = "mapbox",
            figure={
                "data": [
                    dict(
                    	lat = ['56.38'],
                    	lon =  ['-2.88'],
                        type = "scattermapbox",
                        customdata = df['tmax'],
                        mode = "markers",
                        marker = {'size': '14',},
                        text = ['Leuchar']
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
        dcc.RangeSlider(
        className = 'my-range-slider',
        id = 'my-range-slider',
        min = df['yyyy'].min(),
        max = df['yyyy'].max(),
        marks = {str(date): str(date)
        		for date in df['yyyy'].unique()},
		value=[1970, 1993],

		
    ),
        html.H3(id='test', style={'color': 'white'}),


     html.Div([
     	html.H3(id='year-range', style={'color': 'white'}),
		], className='row'),

        html.Div([
        	html.Div([
        	dcc.Graph(
        		 id='temp_graph',
        		 config={'displayModeBar': False})], className='col-md-12'),
			# html.Div([
			# 	dcc.Graph(
			# 		id='sun_graph',
			# 		config={'displayModeBar': False})], className='col-md-6'),
			# html.Div([dcc.Graph(id='rain_graph')], className='col-md-4'),
		], className='row')
	],  className='container-fluid')


@app.callback(
    Output('year-range', 'children'),
    [Input('my-range-slider', 'value')]
)

def update_output(year_range):


	return str(year_range)




# @app.callback(
#     	Output('test', 'children'),
#     	[Input('my-range-slider', 'value')]
#     	)

# def test(year_range):
#     dff = df[df['year'] == year_range]
#     return '{} joules'.format(str(dff['tmax'].max()))


@app.callback(
        Output('temp_graph', 'figure'),
        [Input('mapbox', 'clickData'),
         Input('my-range-slider', 'value')])

def update_graph(clickData, year_range):

	date_start = '{}-01-01'.format(year_range[0])
	date_end = '{}-12-31'.format(year_range[1])
	yearvalues = pd.date_range(start=date_start ,end=date_end,freq='Y')
	string_dates = [str(x) for x in yearvalues.year]

	string_tmax = [str(x) for x in df['tmax']]
	string_tmin = [str(x) for x in df['tmin']]

	month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
         'August', 'September', 'October', 'November', 'Decemberss','test1', 'test2']
	high_2000 = [3,4,10]
	low_2000 = [1,2,5]

	trace0 = go.Scatter(
    x = string_dates,
    y = string_tmax,
    name = 'High 2014',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
    )
	trace1 = go.Scatter(
	x = string_dates,
    y = string_tmin,
    name = 'Low 2014',
    line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,))

	return {
	'data': [trace0,trace1],
	'layout': dict(plot_bgcolor='black', paper_bgcolor='black', title = 'Average High and Low Temperatures in Leuchar',
              xaxis = dict(title = 'Month', gridcolor='black',),
              yaxis = dict(title = 'Temperature (degrees Celsius)',gridcolor='black',),
              )
	}

if __name__ == "__main__":
	app.run_server(debug=True)
