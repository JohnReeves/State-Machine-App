import plotly.graph_objects as go

class GraphInterface:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def draw_graph(self):
        pos = nx.spring_layout(self.state_machine.graph)
        edge_x = []
        edge_y = []

        for edge in self.state_machine.get_transitions():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='blue'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        for node in self.state_machine.get_states():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color='green',
                size=10,
            )
        )

        return go.Figure(data=[edge_trace, node_trace])
