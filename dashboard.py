import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from dateutil.parser import parse
import requests

app = dash.Dash()
app.title = 'When To Drop Princeton Courses!'
server = app.server

url = "https://when-to-drop-api.herokuapp.com/dept/COS"
options = requests.get(url).json()

app.layout = html.Div([
    html.Div(
        [
            dcc.Markdown(
                '''
                ### Course Enrollment at Princeton University
                A visualization of Princeton course enrollment over time. Data for COS and ORFE classes begins from Fall 2018, and data for all other classes begins from Spring 2019. All data was obtained by scraping the Registrar website daily.
                '''.replace('  ', ''),
                className='eight columns offset-by-two'
            )
        ],
        className='row',
        style={'text-align': 'center', 'margin-bottom': '15px'}
    ),
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

    return ({
        'data': [{
            'x': x,
            'y': y
        }],
        'layout': {
            'xaxis':{
                'title':'Time'
            },
            'yaxis':{
                'title':'Number of Students'
            },
            'title': '{}'.format(get_coursetitle(course_id))
        }
    })

def get_coursetitle(course_id):
    options = requests.get(url).json()
    for course in options:
        if course['value'] == course_id:
            return course['label']

if __name__ == '__main__':
    app.run_server()
