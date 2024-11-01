# app.py

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import networkx as nx

from StateMachine import StateMachine

class LiftStateMachineApp:
    def __init__(self):
        self.state_machine1 = StateMachine("Lift1", "state_machines.xml")
        self.state_machine2 = StateMachine("Lift2", "state_machines.xml")
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([dbc.Col(html.H3("Lift State Machines"), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div("Lift 1 State Machine"),
                    dcc.Graph(id="state_machine_graph_1", figure=self.render_graph("Lift1")),
                    # Control Column for Lift 1 (Trigger, Goto, Reset)
                    dbc.Row([
                        dbc.Col(dcc.Input(id="event_name", placeholder="Enter event"), width=8),
                        dbc.Col(dbc.Button("Trigger Event", id="trigger_event_button"), width=4)
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Dropdown(
                            id="goto_state",
                            placeholder="Select state to go to",
                            options=[{"label": state, "value": state} for state in self.state_machine1.states.keys()]
                        )),
                        dbc.Col(dbc.Button("Goto State", id="goto_button"))
                    ]),
                    dbc.Row([dbc.Col(dbc.Button("Reset", id="reset_button"))])
                ], width=6),
                dbc.Col([
                    html.Div("Lift 2 State Machine"),
                    dcc.Graph(id="state_machine_graph_2", figure=self.render_graph("Lift2"))
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col(dbc.Textarea(id='xml_editor', value=self.load_xml(), style={'width': '100%', 'height': '300px'})),
                dbc.Col(dbc.Button("Save XML", id="save_xml")),
            ])
        ])
        self.setup_callbacks()


    def setup_callbacks(self):
        @self.app.callback(
            Output("state_machine_graph_1", "figure"),
            Input("state_machine_selector", "value")
        )
        def update_graph_1(machine_name):
            return self.render_graph("Lift1")

        @self.app.callback(
            Output("state_machine_graph_2", "figure"),
            Input("state_machine_selector", "value")
        )
        def update_graph_2(machine_name):
            return self.render_graph("Lift2")

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

        @self.app.callback(
            [Output("state_machine_graph_1", "figure"), Output("state_machine_graph_2", "figure")],
            Input("trigger_event_button", "n_clicks"),
            State("event_name", "value"),
            State("state_machine_selector", "value")
        )
        @self.app.callback(
            [Output("state_machine_graph_1", "figure"), Output("state_machine_graph_2", "figure")],
            Input("reset_button", "n_clicks"),
        )
        def reset_state_machine(n_clicks):
            self.state_machine1.reset()
            self.state_machine2.reset()
            return self.render_graph("Lift1"), self.render_graph("Lift2")

        @self.app.callback(
            [Output("state_machine_graph_1", "figure"), Output("state_machine_graph_2", "figure")],
            Input("goto_button", "n_clicks"),
            State("goto_state", "value"),
            State("state_machine_selector", "value")
        )
        def goto_state(n_clicks, state_name, machine_name):
            machine = self.state_machine1 if machine_name == "Lift1" else self.state_machine2
            if state_name:
                machine.goto(state_name)
            return self.render_graph("Lift1"), self.render_graph("Lift2")

        async def trigger_event(n_clicks, event_name, machine_name):
            machine = self.state_machine1 if machine_name == "Lift1" else self.state_machine2
            await machine.process_event(event_name)
            return self.render_graph("Lift1"), self.render_graph("Lift2")

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
    app = LiftStateMachineApp()
    app.run()
