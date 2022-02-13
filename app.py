import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from dash_canvas import DashCanvas
from dash_canvas.utils import array_to_data_url, parse_jsonstring
import numpy as np
from dash.exceptions import PreventUpdate
import json
from skimage import io

githublink='https://git.generalassemb.ly/plotly-dash-apps/525-canvas-drawing'
sourceurl='https://dash.plotly.com/canvas'

########### Initiate the app
tabtitle='Canvas'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle
app.config.suppress_callback_exceptions = True

height, width = 200, 500
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width

app.layout = html.Div([
    html.H5('Press down the left mouse button and draw inside the canvas'),
    DashCanvas(id='canvas',
                lineWidth=5,
                width=canvas_width,
                height=canvas_height,
                scale=scale,
                goButtonTitle='test',
                hide_buttons=["zoom", "pan", "line", "pencil", "rectangle", "undo", "select"],
                ),
    html.Div(id='output-message', children='test'),
    html.Div(id='output-message-2', children='test'),
    html.Div(html.Img(id='my-image',width=canvas_width,)),
# Footer
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ])

# Callback 1
@app.callback(Output('output-message', 'children'),
              Input('canvas', 'json_data'))
def update_data(string):
    if string:
        data = json.loads(string)

    else:
        raise PreventUpdate
    return str(data['objects'][0]['path'])

# Callback 2
@app.callback(Output('my-image', 'src'),
              Input('canvas', 'json_data'))
def update_data(string):
    if string:
        mask = parse_jsonstring(string)
    else:
        raise PreventUpdate
    return array_to_data_url((100 * mask).astype(np.uint8))


# Callback 3
@app.callback(Output('output-message-2', 'children'),
              Input('canvas', 'json_data'))
def update_data(string):
    if string:
        mask = parse_jsonstring(string)
    else:
        raise PreventUpdate
    return str(mask)

if __name__ == '__main__':
    app.run_server(debug=True)
