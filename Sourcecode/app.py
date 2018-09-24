import dash, plotly
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


app = dash.Dash()

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

mapbox_access_token = "pk.eyJ1IjoiYWF0aGFuOTMiLCJhIjoiY2psdGVqdGhrMDVnaTNrbDgyZW9mZjBncSJ9.xQBdSA7YMBS_1Lnkj2nZ5Q"

for css in external_css:
    app.css.append_css({"external_url": css})

df = pd.read_csv('C:\\Users\\aathan\\Desktop\\dissertation\\data\\leuchar.csv')
print(df)

app.layout = html.Div([
	html.H2("Scotland Weather Data"),


	    dcc.Graph(
            id = "mapbox",
            figure={
                "data": [
                    dict(
                        type = "scattermapbox",
                        mode = "markers",
                        marker = {'size': '14'},
                    )
                ],
                "layout": dict(
                    hovermode = "closest",
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    mapbox = dict(
                        accesstoken = mapbox_access_token,
                        center = dict(lat = 38.30, lon = -90.68),
                        style = "dark",
                        zoom = 3.5,
                        layers = []
                    )   
                )
            },
        ),
        dcc.RangeSlider(
        className='my-range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),

        html.Div([
        	html.Div([
        	dcc.Graph(
        		 id='temp_graph',
        		 config={'displayModeBar': False})], className='col-md-4'),
			html.Div([dcc.Graph(id='sun_graph')], className='col-md-4'),
			html.Div([dcc.Graph(id='rain_graph')], className='col-md-4'),
		], className='row')
	], className='container-fluid')



if __name__ == "__main__":
    app.run_server(debug=True)
