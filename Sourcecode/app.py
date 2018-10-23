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
	date_start = '{}-01-01'.format(year_range[0])
	date_end = '{}-12-31'.format(year_range[1])
	yearvalues = pd.date_range(start=date_start ,end=date_end,freq='Y')
	years = yearvalues.year
	return str(years)





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

def update_graph( clickData, year_range):

    data = go.Data([
        go.Scatter(
            name='Max temperature',
            # events qty
            x=year_range,
            # year
            y=[df['tmax']],

            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#eb1054'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
        go.Scatter(
            name='Min temperature',
            # events qty
            x=year_range,
            # year
            y=df['tmin'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#C2FF0A'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
    ])
    layout = go.Layout(
        xaxis={
            'color': '#FFF',
            'title': 'year',
        },
        yaxis={
            'color': '#FFF',
            'title': 'temperature range',
        },
        margin={
            'l': 40,
            'b': 40,
            't': 10,
            'r': 0
        },
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,  
        layout=layout
    )



    @app.callback(
        Output('sun_graph', 'figure'),
        [Input('mapbox', 'clickData'),
         Input('my-range-slider', 'value')])

    def sun_chart(clickData):

    	data = go.Data([
        go.Scatter(
            name='Sun',
            # events qty
            x=year_range,
            # year
            y=df['sun'],

            mode='bar',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#eb1054'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
    ])
    layout = go.Layout(
        xaxis={
            'color': '#FFF',
            'title': 'year',
        },
        yaxis={
            'color': '#FFF',
            'title': 'Sunshine hours',
        },
        margin={
            'l': 40,
            'b': 40,
            't': 10,
            'r': 0
        },
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,  
        layout=layout
    )



if __name__ == "__main__":
	app.run_server(debug=True)
