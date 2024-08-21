import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
from dash import dcc, html, dash_table
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#datos
años=[1950+i for i in range(70)]
exportaciones=[918926,1124221,1081233,331817,251907,290708,761929,1241914,901796,1132872,969552,988644,1048114,1172249,1460307,1618603,1784027,1870889,1749940,1801349,1981132,1777934,1873370,2624568,3514784,2776191,3112502,3208219,2774112,2933342,3743201,3560467,4272614,3994456,3330135,2636894,2876456,2727796,2668729,3320499,3517480,3491780,3312385,3287535,3906703,4257121,4448787,4364980,4277889,3681611,4085550,4540209,5040338,6126106,7762197,9253267,11394869,11921804,13596729,11179129,10248692,10719430,12144641,12641952,14015558,13186019,12432525,11814068,12427220,12201083]
importaciones=[882169,1063453,1168900,448037,305635,352098,911682,1697686,1434141,1510496,1431625,1406869,1588921,1790772,1659092,2007488,2137147,2165218,2127787,2200712,1997019,2064870,2168633,2729943,2716277,3509865,3420860,3615436,3769097,3828313,3401039,3512679,4322532,3391024,3634925,3161911,3467736,3333886,3290335,3417650,3694970,4383654,4802750,4890850,4904730,5132116,5373253,6070490,7075814,5951189,6108409,5741296,6457155,6309494,6562531,8354093,8938245,9774116,11493604,10297201,10035269,11742291,12244967,13246528,15244475,14420424,13815823,14586841,14868769,15095467]
df=pd.DataFrame({
    'Año':años,
    'Exportaciones':exportaciones,
    'Importaciones':importaciones
})
df['Balanza comercial']=df['Exportaciones']-df['Importaciones']
df.set_index('Año', inplace=True)
# Deshabilitar la notación científica
pd.options.display.float_format = '{:,.2f}'.format
df.tail()
#tabla
#s por periodos
df_capestado=df.loc[1952:1985]
df_neolib=df.loc[1985:2005]
df_mas=df.loc[2005:2019]
dfc=df_capestado.describe()
dfn=df_neolib.describe()
df_m=df_mas.describe()
dfc_rounded = dfc.round(2).reset_index()
dfn_rounded = dfn.round(2).reset_index()
dfm_rounded = df_m.round(2).reset_index()
dfm_rounded
#tasas de crecimiento
df['Tdc exportaciones(%)'] = df['Exportaciones'].pct_change() * 100
df['Tdc importaciones(%)']= df['Importaciones'].pct_change() * 100
df['Tdc balanza comercial(%)']= df['Balanza comercial'].pct_change() * -100
df.loc[1970:1984,:]
app=dash.Dash()
server=app.server

# Crear una figura con múltiples trazas
fig = go.Figure()

# Agregar la primera traza (por ejemplo, una gráfica de líneas)
fig.add_trace(go.Scatter(
    x=df.index,
    y=exportaciones,
    mode='lines+markers',
    name='Exportaciones'
))

# Agregar la segunda traza (por ejemplo, una gráfica de barras)
fig.add_trace(go.Scatter(
    x=df.index,
    y=importaciones,
    mode='lines+markers',
    name='Importaciones'
))

# Agregar la tercera traza (por ejemplo, una gráfica de dispersión)
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['Balanza comercial'],
    mode='lines+markers',
    name='Balanza Comercial'
))

# Configurar el diseño de la figura
fig.update_layout(
    title='Gráfica con Múltiples Trazas',
    xaxis_title='X-axis',
    yaxis_title='Y-axis',
    barmode='group'  # Para mostrar barras agrupadas
)
fig1=go.Figure()
# Agregar la primera traza (por ejemplo, una gráfica de líneas)
fig1.add_trace(go.Scatter(
    x=df.index,
    y=df['Tdc exportaciones(%)'],
    mode='lines+markers',
    name='Exportaciones'
))

# Agregar la segunda traza (por ejemplo, una gráfica de barras)
fig1.add_trace(go.Scatter(
    x=df.index,
    y=df['Tdc importaciones(%)'],
    mode='lines+markers',
    name='Importaciones'
))

# Agregar la tercera traza (por ejemplo, una gráfica de dispersión)
fig1.add_trace(go.Scatter(
    x=df.index,
    y=df['Tdc balanza comercial(%)'],
    mode='lines+markers',
    name='Balanza Comercial'
))

# Configurar el diseño de la figura
fig1.update_layout(
    title='Tasas de crecimiento',
    xaxis_title='X-axis',
    yaxis_title='Y-axis',
    barmode='group'  # Para mostrar barras agrupadas
)
# Define el layout de la aplicación
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'padding': '20px'},
    children=[
        html.H1(
            'Hola Dash',
            style={'textAlign': 'center', 'color': '#2c3e50', 'font-family': 'Arial, sans-serif'}
        ),
        html.Div(
            'Exportaciones, Importaciones y Balanza comercial',
            style={'textAlign': 'center', 'margin-bottom': '30px', 'font-size': '18px', 'color': '#34495e'}
        ),
        # Botones para realizar zoom en los años (Gráfica de valores)
        html.Div(
            style={'textAlign': 'center', 'margin-bottom': '20px'},
            children=[
                html.Button('1952-1985', id='btn-1952-1985', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#1abc9c',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('1985-2005', id='btn-1985-2005', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#3498db',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('2005-2019', id='btn-2005-2019', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#e74c3c',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('Todo', id='btn-all', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#f39c12',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                })
            ]
        ),
        dcc.Graph(
            id='grafica-multiple',
            figure=fig,
            style={'backgroundColor': '#ffffff', 'border': '1px solid #ddd', 'padding': '10px'}
        ),
        # Botones para realizar zoom en los años (Gráfica de tasas de crecimiento)
        html.Div(
            style={'textAlign': 'center', 'margin-top': '30px', 'margin-bottom': '20px'},
            children=[
                html.Button('1952-1985', id='tdc-1952-1985', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#1abc9c',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('1985-2005', id='tdc-1985-2005', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#3498db',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('2005-2019', id='tdc-2005-2019', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#e74c3c',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                }),
                html.Button('Todo', id='tdc-all', style={
                    'margin': '5px', 'padding': '10px 20px', 'backgroundColor': '#f39c12',
                    'color': 'white', 'border': 'none', 'borderRadius': '5px',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)', 'cursor': 'pointer'
                })
            ]
        ),
        dcc.Graph(
            id='grafica-tasas',
            figure=fig1,
            style={'backgroundColor': '#ffffff', 'border': '1px solid #ddd', 'padding': '10px'}
        ),
        html.P('Resumen de estadígrafos clave para el período 1952-2019'),
        # Div con tablas descriptivas utilizando Dash DataTable
        # Div con tablas descriptivas utilizando Dash DataTable
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-around', 'margin-top': '30px'},
            children=[
                html.Div([
                    html.H3('1952-1985'),
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in dfc_rounded.columns],
                        data=dfc_rounded.to_dict('records'),
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center'},
                        style_header={
                            'backgroundColor': '#1abc9c',
                            'fontWeight': 'bold',
                            'color': 'white'
                        }
                    )
                ], style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'}),
                
                html.Div([
                    html.H3('1985-2005'),
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in dfn_rounded.columns],
                        data=dfn_rounded.to_dict('records'),
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center'},
                        style_header={
                            'backgroundColor': '#3498db',
                            'fontWeight': 'bold',
                            'color': 'white'
                        }
                    )
                ], style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'}),
                
                html.Div([
                    html.H3('2005-2019'),
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in dfm_rounded.columns],
                        data=dfm_rounded.to_dict('records'),
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center'},
                        style_header={
                            'backgroundColor': '#e74c3c',
                            'fontWeight': 'bold',
                            'color': 'white'
                        }
                    )
                ], style={'flex': '1', 'backgroundColor': '#ffffff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'}),
            ]
        )
])

@app.callback(
    Output('grafica-multiple', 'figure'),
    [Input('btn-1952-1985', 'n_clicks'),
     Input('btn-1985-2005', 'n_clicks'),
     Input('btn-2005-2019', 'n_clicks'),
     Input('btn-all', 'n_clicks')],
)
def update_figure(btn1952, btn1985, btn2005, btn_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'btn-all'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=exportaciones, mode='lines+markers', name='Exportaciones'))
    fig.add_trace(go.Scatter(x=df.index, y=importaciones, mode='lines+markers', name='Importaciones'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Balanza comercial'], mode='lines+markers', name='Balanza comercial'))
    fig.update_layout(title='Gráfica con Múltiples Trazas', xaxis_title='Año', yaxis_title='Valor')

    if button_id == 'btn-1952-1985':
        fig.update_xaxes(range=[1951.5, 1985])
    elif button_id == 'btn-1985-2005':
        fig.update_xaxes(range=[1984, 2005])
    elif button_id == 'btn-2005-2019':
        fig.update_xaxes(range=[2004, 2019])
    elif button_id == 'btn-all':
        fig.update_xaxes(range=[1952, 2019])
        

    return fig

# Callback para el gráfico de tasas de crecimiento
@app.callback(
    Output('grafica-tasas', 'figure'),
    [Input('tdc-1952-1985', 'n_clicks'),
     Input('tdc-1985-2005', 'n_clicks'),
     Input('tdc-2005-2019', 'n_clicks'),
     Input('tdc-all', 'n_clicks')]
)
def update_tdc_figure(tdc1952, tdc1985, tdc2005, tdc_all):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'tdc-all'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df.index, y=df['Tdc exportaciones(%)'], mode='lines+markers', name='Exportaciones'))
    fig1.add_trace(go.Scatter(x=df.index, y=df['Tdc importaciones(%)'], mode='lines+markers', name='Importaciones'))
    fig1.add_trace(go.Scatter(x=df.index, y=df['Tdc balanza comercial(%)'], mode='lines+markers', name='Balanza Comercial'))
    fig1.update_layout(title='Gráfica de Tasas de Crecimiento', xaxis_title='Año', yaxis_title='Tasa de Crecimiento (%)')

    if button_id == 'tdc-1952-1985':
        fig1.update_xaxes(range=[1951.5, 1985])
    elif button_id == 'tdc-1985-2005':
        fig1.update_xaxes(range=[1984, 2005])
    elif button_id == 'tdc-2005-2019':
        fig1.update_xaxes(range=[2004, 2019])
    elif button_id == 'tdc-all':
        fig1.update_xaxes(range=[1952, 2019])

    return fig1

if __name__=='__main__':
    app.run_server(port=10000)
