import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_auth
import dash_table as dt
import pandas as pd

USERNAME_PASSWORD_PAIRS = [
    ['Shubham', 'abcd@123'],['Saurabh', 'password#123']
]


def DataframeFormatter(df):
    df.iloc[:4,:].fillna("",inplace = True)
    t_h = df.iloc[0,:]+" "+df.iloc[1,:]+" "+df.iloc[2,:]+" "+df.iloc[3,:]
    df.columns = t_h
    df = df.iloc[4:,:]
    df = df.transpose()
    df.columns = df.iloc[0,:]
    df = df.iloc[1:,:]
    df.reset_index(inplace = True)
    return df


Sheets = ["State Vs LLC Count & Amount(cr)","Product Vs DisbursedAmount(cr)","Lender Vs DisbursedAmount(cr)"] 
app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server
 

year_options = []
for year in Sheets:
    year_options.append({'label':str(year),'value':year})


app.layout = html.Div([
    html.H1("HI"),
    dcc.Dropdown(id='sheet-picker',options=year_options,value="None"),
    html.Div(id="table")
    ])

@app.callback(Output('table','children'),
            [Input('sheet-picker', 'value')])

def update_datatable(sheet):

    if sheet == Sheets[0]:
        df = pd.read_csv("State Vs LLC Count & Amount.csv",index_col=0)
        df = DataframeFormatter(df)
        data = df.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns)
    if sheet == Sheets[1]:
        df1 = pd.read_csv("Product Vs DisbursedAmount.csv",index_col=0)
        df1 = DataframeFormatter(df1)
        data = df1.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df1.columns)]
        return dt.DataTable(data=data, columns=columns)
    if sheet == Sheets[2]:
        df2 = pd.read_csv("Lender Vs DisbursedAmount.csv",index_col=0)
        df2 = DataframeFormatter(df2)
        data = df2.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df2.columns)]
        return dt.DataTable(data=data, columns=columns)
 
if __name__ == '__main__':
    app.run_server()
