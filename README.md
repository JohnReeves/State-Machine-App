# State-Machine-App
A state machine app made with dash, networkx, plotly and etree

## Main Components Overview
* Dash: Used for building the web-based GUI, allowing users to interact with the state machine, edit states, transitions, and visualize it
* NetworkX: Used for representing the state machine graph, where nodes represent states and edges represent transitions
* Plotly: Integrates with Dash to visualize the state machine graph interactively

## Class Structure
* StateMachineEditor: Handles user input, editing states, transitions, and managing interactions between the components
* StateMachine: Encapsulates the data structure (e.g., states, transitions, current state), possibly using a NetworkX graph to model the relationships
* GraphInterface: Handles rendering the graph using Plotly, and updating it in response to changes in the state machine
