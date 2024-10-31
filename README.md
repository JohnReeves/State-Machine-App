# State-Machine-App
A state machine app made with dash, networkx, plotly and etree

## Main Components
* Dash: Used for building the web-based GUI, allowing users to interact with the state machine, edit states, transitions, and visualize it
* NetworkX: Used for representing the state machine graph, where nodes represent states and edges represent transitions
* Plotly: Integrates with Dash to visualize the state machine graph interactively
* Etree: Used for processing the state machine data structure in xml format

## Class Structure
* StateMachine: Encapsulates the data structure states, transitions, current state, using a NetworkX graph to model the relationships
* StateMachine.xml: contains the state machine data structure, including states, transitions, current state, guards and timeout / watchdog timers
* StateMachineApp: Handles rendering the graph using Plotly, and updating it in response to changes in the state machine

## Deleted files
* StateMachineEditor: Handles user input, editing states, transitions, and managing interactions between the components
* GraphInterface: Handles rendering the graph using Plotly, and updating it in response to changes in the state machine
