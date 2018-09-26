import dash, plotly
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import json



app = dash.Dash()

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

mapbox_access_token = "pk.eyJ1IjoiYWF0aGFuOTMiLCJhIjoiY2psdGVqdGhrMDVnaTNrbDgyZW9mZjBncSJ9.xQBdSA7YMBS_1Lnkj2nZ5Q"

for css in external_css:
    app.css.append_css({"external_url": css})

df = pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\leuchar.csv')
print(df['yyyy'])

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
        min = df['yyyy'].min(),
        max = df['yyyy'].max(),
        marks = {str(date): str(date)
        		for date in df['yyyy'].unique()},
		value=[1970, 1993],

		
    ),
        html.Div(
        html.Pre(id='test', style={'overflowY': 'scroll', 'height': '100vh', 'color': 'white'})
    ),

        html.Div([
        	html.Div([
        	dcc.Graph(
        		 id='temp_graph',
        		 config={'displayModeBar': False})], className='col-md-4'),
			html.Div([dcc.Graph(id='sun_graph')], className='col-md-4'),
			html.Div([dcc.Graph(id='rain_graph')], className='col-md-4'),
		], className='row')
	],  className='container-fluid')


@app.callback(
        Output('test', 'children'),
        [Input('mapbox', 'clickData')])

def display_data(clickData):
    return json.dumps(clickData, indent=2)




if __name__ == "__main__":
    app.run_server(debug=True)
