import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash
import pandas as pd


# ----------------------------- functions for data preparation ------------------------------------------
def data_prep(data_file):
    #Reading the data and making a copy
    df = pd.read_excel(data_file)
    temp = df.copy()

    #Removing empty rows
    temp.dropna(thresh=2, inplace=True)

    #Reseting columns - Changing the column names using the values in the 1st row
    temp_header = temp.iloc[0,]
    temp = temp[1:]
    temp.columns = temp_header

    #Removing all columns whose names are nan
    temp = temp.loc[:, temp.columns.notnull()]

    #Ensuring the indices go from 0 without skipping any number
    temp.reset_index(inplace=True, drop = True)

    #Categorize Geography as Country, Province, and City
    temp['Region/City'] = ""
    temp['Region/City'][temp.index ==0] = 'Country'
    temp['Region/City'][(temp.index < 11) & (temp.index >0)] = 'Province'
    temp['Region/City'][temp.index >= 11] = 'City'

    #Rearrange columns -- bring column 'Region/City' to the 1st column position
    # Access columns
    cols = temp.columns.tolist()
    # Bring last col to front
    cols = cols[-1:] + cols[:-1]
    # Set new column order
    temp = temp[cols] 

    #Converting data type to the right format
    #Isolating yearly and quarterly columns and convert to numeric.
    int_cols = temp.columns.drop(['Region/City', 'Geography'])
    temp[int_cols] = temp[int_cols].apply(pd.to_numeric, errors='coerce')

    return temp


def slice_data(df, level):
    """
    df: data frame with mortgage data
    level: "Province" or "City"
    Extract a subset of df based on level
    Return a dataframe
    """
    try:
        temp = df[df['Region/City']==level]
        temp = pd.melt(temp, id_vars='Geography', value_vars=temp.columns[2:])
        temp.rename(columns = {3:'Time'}, inplace = True)
        return temp
    except KeyError:
        print("Key not found. Make sure that 'level' is in ['Province','City']")

#------------------------------------ read in the data ---------------------------------------------------
data = "./data/"
data_file = data + "average-value-new-mortgage-loans-ca-prov-cmas-2012-q3-2020-q3-en.xlsx"
df_mortgage = data_prep(data_file)
level = 'Province'
df_mortgage_long = slice_data(df_mortgage, level = level)

#-------------------------------------- APP section ------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-dropdown'),
    dcc.Dropdown(
        id='province',
        options=[{'label': i, 'value': i} for i in df_mortgage_long['Geography'].unique()],
        value= 'Newfoundland'
    )
])

#-----------------------------------------------------
@app.callback(
    Output('graph-with-dropdown', 'figure'),
    Input('province', 'value'))
def update_figure(selected_province):
    filtered_df = df_mortgage_long[df_mortgage_long['Geography'] == selected_province]

    fig = px.line(filtered_df, x="Time", y="value", 
                  title = f'Line plot of mortgage loans in {selected_province}', 
                  hover_name="value")
    fig.update_xaxes(tickangle=-45)
    fig.update_layout(transition_duration=500)

    return fig


#-----------------------------------------------------------------------
#fig = px.line(df_mortgage_long, x='Time', y='value', color = 'Geography',
#              title = f'Line plot of mortgage loans by {level}'.upper())
#fig.update_xaxes(tickangle=-45)
#fig.show()

#-----------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(mode='inline')  # 'inline' so that we don't have to open a new browser
   