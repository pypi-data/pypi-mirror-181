import krakenex
from pykrakenapi import KrakenAPI
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc

class Graph:
    
    def __init__(self, df, value_m, pair_name):
        self.df = df
        self.value_m = value_m
        self.pair_name = pair_name
        
    def graphic(self):
        try:
            specs = [[{"secondary_y": True}], [{"secondary_y": False}], [{"secondary_y": True}]]
            
            if len(self.value_m) == 0:
                fig = make_subplots(rows=3, cols=1, 
                                    shared_xaxes= True, 
                                    specs=specs, 
                                    subplot_titles=("<b>" + self.pair_name + " Graph<b>", "<b>RSI<b>", ""))
            else:
                fig = make_subplots(rows=3, cols=1, 
                                    shared_xaxes= True, 
                                    specs=specs, 
                                    subplot_titles=("<b>" + self.pair_name + " Graph<b>", "<b>RSI<b>", "<b>Moving Average<b>"))
            
            fig.add_trace(go.Candlestick(x = self.df.index,
                                         open = self.df['open'],
                                         close = self.df['close'],
                                         low = self.df['low'],
                                         high = self.df['high']),
                                         secondary_y = False,
                                         row = 1, col = 1)
        
            for m in self.value_m:
                fig.add_trace(go.Scatter(x = self.df.index, y = self.df['moving_average_' + str(m)]), secondary_y = True, row = 1, col = 1)
                fig.add_trace(go.Scatter(x = self.df.index, y = self.df['moving_average_' + str(m)]), secondary_y= False, row = 3, col = 1)
            
            fig.add_trace(go.Scatter(x = self.df.index, y = self.df.RSI, line=dict(color="black")), secondary_y= False, row = 2, col = 1)
            fig.add_hline(y=70, row=2, col=1, secondary_y = False, line_color="red")
            fig.add_hline(y=30, row=2, col=1, secondary_y = False, line_color="green")
            fig.update_xaxes(row=1, col=1, rangeslider_thickness=0.05)
            fig.update_layout(width=1000, height=900)
            fig.update_layout(xaxis_showticklabels=True, xaxis2_showticklabels=True)
            return fig
        
        except Exception as e:
            print(str(e) + 'has occurred')
            return

class Moving_Average:
    
    def __init__(self,slot,df):
        self.slot = slot
        self.df = df
        
    def calculate(self):
        try:
            self.df['moving_average_{}'.format(self.slot)] = self.df['close'].rolling(window=int(self.slot),min_periods=1).mean()
            return self.df
        
        except Exception as e:
            print(str(e) + 'has occurred')
            return

class RSI:
    
    def __init__(self,df):
        self.df = df
    
    def calculate(self):
        try:
            self.df['diff'] = self.df.close - self.df.open
            self.df['up'] = self.df['diff'][self.df['diff']>0]
            self.df['down'] = abs(self.df['diff'][self.df['diff']<=0])
            self.df.fillna(value = 0, inplace = True)
            
            self.df['media_up'] = self.df['up'].rolling(window = 14).mean()
            self.df['media_down'] = self.df['down'].rolling(window = 14).mean()
            self.df['RSI'] = 100-(100/(1+(self.df.media_up/self.df.media_down)))
            self.df.dropna(inplace = True)
            
            return self.df
        
        except Exception as e:
            print(str(e) + 'has occurred')
            return
            
def krakenex_data_import():
    try:
        api = krakenex.API()
        k = KrakenAPI(api)

        data = k.get_tradable_asset_pairs()
        pairs = data['altname'].values.tolist()
        
        return k, pairs

    except Exception as e:
        print('This problem has occurred with the API: ' + str(e))
        
k, pairs = krakenex_data_import()

try:
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    
    app.layout = html.Div([
        html.Div(children=[
            html.Label('Select an asset'),
            dcc.Dropdown(pairs, id='demo-dropdown', style = {'width':'1000px'}),
            
            html.Div(id='dd-output-container')
            
        ], style={'padding': 10, 'flex': 1}),
    
        html.Div(children=[
    
            html.Label('Select the average moving'),
            dcc.Dropdown([10,20,30,40,50,60],
                         multi=True, id = 'average-dropdown'),
            
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div(children=[
    
            html.Label('Select the pair interval'),
            dcc.Dropdown([1, 5, 15, 30, 60, 240, 1440, 10080, 21600], 60, 
                         multi=False, id = 'interval-dropdown'),
            
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'})
    
    @app.callback(
        Output('dd-output-container', 'children'),
        [Input('demo-dropdown', 'value'),
         Input('average-dropdown', 'value'),
         Input('interval-dropdown', 'value')]
    )

    def update_figure(value,value_m, value_i):
        try:
            if value is None:
                return ""
            else:
                df, last = k.get_ohlc_data(value, interval = value_i)
                
                if (value_m is None) == False:
                    for m in value_m:
                        df = Moving_Average(m, df).calculate()
                else:
                    value_m = []
                
                df = RSI(df).calculate()
                 
                return html.Div([
                    dcc.Graph(
                    id='example-graph',
                    figure=Graph(df,value_m,value).graphic())
                ])
        except Exception as e:
            print('This problem has occurred in the figure update: ' + str(e))

except Exception as e:
    print('This problem has occurred with the App design: ' + str(e))

try:
    if __name__ == '__main__':
        app.run_server(debug=True, use_reloader = False)
        
except Exception as e:
    print('This problem has occurred at the start of the program: ' + str(e))
