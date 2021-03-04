# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Imports from this application
from app import app
from joblib import load
pipeline = load('assets/pipeline.joblib')

@app.callback(
    Output('prediction-content', 'H1N1 Vaccine'),
    [Input('opinion_h1n1_risk', 'value'),
    Input('health_insurance', 'value'),
    Input('age_group', 'value'),
    Input('doctor_recc_h1n1', 'value'),
    Input('employment_status', 'value')]
)
def predict(opinion_h1n1_risk, health_insurance, age_group, doctor_recc_h1n1, employment_status):
    df = pd.DataFrame(
        columns = ['opinion_h1n1_risk','health_insurance','age_group','doctor_recc_h1n1','employment_status'],
        data=[[opinion_h1n1_risk,health_insurance,age_group,doctor_recc_h1n1, employment_status]]
    )
    y_pred=pipeline.predict(df)[0]
    return {y_pred}

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Which Features Matter Most

            Move the sliders to see how it affects the probability a person received a vaccine.

            """
        ),
        html.H2('Predicting Vaccine Usage', className='mb-5'),
        html.Div(id='prediction-content', className='Lead')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown('## Predictions', className='mb-5'),
        dcc.Markdown('#### Patient Fear of H1N1 Risk'),
        dcc.Slider(
            id='opinion_h1n1_risk',
            min=1,
            max=5,
            step=1,
            value=3,
            marks={n: str(n) for n in range(1, 5, 1)},
            className='mb-5',
        ),
        dcc.Markdown('#### Health Insurance'),
        dcc.Dropdown(
            id='health_insurance',
            options= [
                {'label': 'Patient Has Health Insurance', 'value': 1},
                {'label': "Patient Has No Health Insurance", 'value': 0},
                {'label': 'nan', 'value': 'nan'}
            ],
            value='Patient Has Health Insurance',
            className='mb-5'
        ),
        dcc.Markdown('#### Patient Age Group'),
        dcc.Dropdown(
            id='age_group',
            options= [
                {'label': '18 - 34 Years', 'value': '18 - 34 Years'},
                {'label': '35 - 44 Years', 'value': '35 - 44 Years'},
                {'label': '45 - 54 Years', 'value': '45 - 54 Years'},
                {'label': '55 - 64 Years', 'value': '55 - 64 Years'},
                {'label': '65+ Years', 'value': '65+ Years'}
            ],
            value='18 - 34 Years',
            className='mb-5'
        ),
        dcc.Markdown('#### Doctor Recommendation'),
        dcc.Dropdown(
            id='doctor_recc_h1n1',
            options= [
                {'label': 'Vaccine Recommended', 'value': 1},
                {'label': "Vaccine Wasn't Recommended", 'value': 0},
                {'label': 'nan', 'value': 'nan'}
            ],
            value='Vaccine Recommended',
            className='mb-5'
        ),
        dcc.Markdown('#### Employment Status'),
        dcc.Dropdown(
            id='employment_status',
            options= [
                {'label': 'Not in Labor Force', 'value': 'Not in Labor Force'},
                {'label': 'Employed', 'value': 'Employed'},
                {'label': 'Unemployed', 'value': 'Unemployed'},
                {'label': 'nan', 'value': 'nan'}
            ],
            value='Employed',
            className='mb-5'
        )
    ]
)

layout = dbc.Row([column1, column2])