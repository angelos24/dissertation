import dash, plotly
import dash_html_components as html
import dash_core_components as dcc
from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = dash.Dash()

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

for css in external_css:
    app.css.append_css({"external_url": css})



app.layout = html.Div([
	html.H2("Scotland Weather Data ", style={'font-family': 'Dosis'}),


	 dcc.Dropdown(
                id='data_drop',
                options=[
                    {'label': 'Max Temperature', 'value': 'tmax'},
                    {'label': 'Min Temperature', 'value': 'tmin'},
                    {'label': 'Rain (mm)', 'value': 'rain'},
                    {'label': 'Sun (hours)', 'value': 'sun'},
                ],
                value="rain",
                placeholder="Please choose a weather phenomeno",
                className="data_option"
            ),
	  dcc.Graph(id='map', figure={
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoiYWF0aGFuOTMiLCJhIjoiY2psdGVqdGhrMDVnaTNrbDgyZW9mZjBncSJ9.xQBdSA7YMBS_1Lnkj2nZ5Q'
            },
            'hovermode': 'closest',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
        }
    }),

	], className='container')



if __name__ == "__main__":
    app.run_server(debug=True)
