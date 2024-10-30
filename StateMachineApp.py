import dash
from dash import dcc, html
from dash.dependencies import Input, Output

class StateMachineApp:
    def __init__(self, state_machine, graph_interface):
        self.state_machine = state_machine
        self.graph_interface = graph_interface
        self.app = dash.Dash(__name__)

    def layout(self):
        return html.Div([
            html.Div([
                html.Label('Add State:'),
                dcc.Input(id='state-input', type='text'),
                html.Button('Add', id='add-state-button')
            ]),
            html.Div([
                dcc.Graph(id='state-machine-graph')
            ])
        ])

    def run(self):
        self.app.layout = self.layout()
        
        @self.app.callback(
            Output('state-machine-graph', 'figure'),
            [Input('add-state-button', 'n_clicks')],
            [Input('state-input', 'value')]
        )
        def update_graph(n_clicks, state_name):
            if n_clicks:
                self.state_machine.add_state(state_name)
            return self.graph_interface.draw_graph()

        self.app.run_server(debug=True)

# Usage Example
state_machine = StateMachine()
graph_interface = GraphInterface(state_machine)
app = StateMachineApp(state_machine, graph_interface)
app.run()
