import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from dateutil.parser import parse
import requests

app = dash.Dash()
server = app.server

url = "https://when-to-drop-api.herokuapp.com/dept/COS"
options = requests.get(url).json()

app.layout = html.Div([
    html.H1('Course Enrollments'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=21276
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(course_id):
    url = "https://when-to-drop-api.herokuapp.com/enroll/" + str(course_id)
    data = requests.get(url).json()

    x = [parse(d) for d in data['x']]
    y = data['y']

    return {
        'data': [{
            'x': x,
            'y': y
        }]
    }

if __name__ == '__main__':
    app.run_server()
