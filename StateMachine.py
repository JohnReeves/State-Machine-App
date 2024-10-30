import networkx as nx

class StateMachine:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_state(self, state_name):
        self.graph.add_node(state_name)

    def add_transition(self, from_state, to_state, action):
        self.graph.add_edge(from_state, to_state, action=action)

    def get_states(self):
        return list(self.graph.nodes)

    def get_transitions(self):
        return list(self.graph.edges(data=True))

    def save(self, filename):
        nx.write_gpickle(self.graph, filename)

    def load(self, filename):
        self.graph = nx.read_gpickle(filename)
