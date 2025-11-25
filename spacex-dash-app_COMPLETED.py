# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
#import seaborn as sns

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 
                                            2500: '2500', 
                                            5000: '5000', 
                                            7500: '7500', 
                                            10000: '10000'},
                                    value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site',
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data = filtered_df[filtered_df['Launch Site']==entered_site]
        #data = data.groupby(['Launch Site', 'class']).agg(
        data = data.groupby('class').agg(            
            count_class=('class', 'count'))
        fig = px.pie(data, values='count_class', 
        names='count_class',
#        names='class',        
        title=f"Total Success Launches for Site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_slider_value):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_slider_value[0], payload_slider_value[1])]
    #filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_payload, max_payload)]
    if entered_site == 'ALL':
#        data = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.scatter(            
                filtered_df, 
                y="class", x="Payload Mass (kg)", 
                color="Booster Version Category", 
#                aspect = 2,
                title='Correlation between success and payload for all sites')
#        plt.xlabel("PayloadMass",fontsize=20)
#        plt.ylabel("class",fontsize=20)
        return fig
    else:
        data = filtered_df[filtered_df['Launch Site']==entered_site]
#        data = data.groupby('class').agg(count_class=('class', 'count'))
        fig = px.scatter(            
                data, 
                y="class", x="Payload Mass (kg)", 
                color="Booster Version Category", 
                title=f"Correlation between success and payload for Site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
