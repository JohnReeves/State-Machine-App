class StateMachineEditor:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def add_state(self, state_name):
        self.state_machine.add_state(state_name)

    def add_transition(self, from_state, to_state, action):
        self.state_machine.add_transition(from_state, to_state, action)

    def save_to_file(self, filename):
        self.state_machine.save(filename)

    def load_from_file(self, filename):
        self.state_machine.load(filename)
