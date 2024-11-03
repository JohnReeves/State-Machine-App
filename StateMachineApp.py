# app.py

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import networkx as nx

from StateMachine import StateMachine

class LiftStateMachineApp:
    def __init__(self, state_machine1, state_machine2):
        self.state_machine1 = state_machine1
        self.state_machine2 = state_machine2
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = dbc.Container([

            html.H3("State Machines Interface"),
            dbc.Row([
                dbc.Col([
                    html.Div("Driving State Machine"),
                    dcc.Graph(id="state_machine_graph_1", figure=self.render_graph("Lift1")),
                ], width=6),
                dbc.Col([
                    html.Div("Responding State Machine"),
                    dcc.Graph(id="state_machine_graph_2", figure=self.render_graph("Lift2"))
                ], width=6),
            ]),

            dcc.Input(id="event_name", placeholder="Enter event"),
            dbc.Button("Trigger Event", id="trigger_event_button"),
            dcc.Dropdown(id="goto_state",
                        placeholder="Select state to go to",
                        options=[{"label": state, "value": state} for state in self.state_machine1.states.keys()]
                        ),
            dbc.Button("Goto State", id="goto_button"),
            dbc.Button("Reset", id="reset_button"),

            dbc.Textarea(id='xml_editor', value=self.load_xml(), style={'width': '100%', 'height': '300px'}),
            dbc.Button("Save XML", id="save_xml"),
        ])
        self.setup_callbacks()


    def setup_callbacks(self):
        @self.app.callback(
            [Output("state_machine_graph_1", "figure"), 
             Output("state_machine_graph_2", "figure")],
            Input("reset_button", "n_clicks")
        )
        def reset_state_machine(n_clicks):
            self.state_machine1.reset()
            self.state_machine2.reset()
            return self.render_graph("Lift1"), self.render_graph("Lift2")

        @self.app.callback(
            Input("goto_button", "n_clicks"),
            State("event_name", "value"),
            State("machine_name", "value")
        )
        def goto_state(n_clicks, event_name, machine_name):
            machine = self.state_machine1 if machine_name == "Lift1" else self.state_machine2
            if event_name:
                machine.goto(event_name)
            return self.render_graph("Lift1"), self.render_graph("Lift2")
       
        @self.app.callback(
            Input("trigger_event_button", "n_clicks"),
            State("event_name", "value")
        )
        async def trigger_event(n_clicks, event_name, machine_name):
            machine = self.state_machine1 if machine_name == "Lift1" else self.state_machine2
            await machine.process_event(event_name)
            return self.render_graph("Lift1"), self.render_graph("Lift2")

        @self.app.callback(
            Output("xml_editor", "value"),
            Input("save_xml", "n_clicks"),
            State("xml_editor", "value")
        )
        def save_xml(n_clicks, xml_content):
            with open("state_machines.xml", "w") as f:
                f.write(xml_content)
            self.state_machine1.load_from_xml("state_machines.xml")
            self.state_machine2.load_from_xml("state_machines.xml")
            return xml_content
        
    def load_xml(self):
        with open("state_machines.xml", "r") as file:
            return file.read()

    def render_graph(self, machine_name):
        # Select the appropriate state machine
        machine = self.state_machine1 if machine_name == "Lift1" else self.state_machine2

        # Initialize a directed graph with NetworkX
        G = nx.DiGraph()

        # Add states as nodes and transitions as directed edges
        for state, data in machine.states.items():
            G.add_node(state)
            for event, target in data["transitions"]:
                G.add_edge(state, target, label=event)

        # Layout for positioning nodes
        pos = nx.spring_layout(G, seed=42)

        # Extract node positions and labels
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        edge_x = []
        edge_y = []

        # Build edges for plotly
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=3, color="#888"),
            hoverinfo="none",
            mode="lines"
        )

        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            text=list(G.nodes()),
            textposition="top center",
            marker=dict(size=40, color="skyblue", line=dict(width=2, color="DarkSlateGrey")),
            hoverinfo="text"
        )

        # Create figure with edges and nodes
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f"{machine_name} State Machine",
                            showlegend=False,
                            hovermode="closest",
                            margin=dict(b=0, l=0, r=0, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        ))
        return fig
    
    def run(self):
        self.app.run_server(debug=True)

if __name__ == "__main__":
    state_machine1 = StateMachine("Lift1", "state_machines.xml")
    state_machine2 = StateMachine("Lift2", "state_machines.xml")

    app = LiftStateMachineApp(state_machine1, state_machine2)
    app.run()
