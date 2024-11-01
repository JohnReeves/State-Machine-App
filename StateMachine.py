# state_machine.py

import xml.etree.ElementTree as ET
import asyncio
import random
from datetime import datetime, timedelta

class StateMachine:
    def __init__(self, name, xml_file):
        self.name = name
        self.states = {}
        self.initial_state = None
        self.current_state = None
        self.events = {}
        self.guards = {}
        self.load_from_xml(xml_file)

    def load_from_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        machine = root.find(f".//state_machine[@name='{self.name}']")
        if not machine:
            raise ValueError(f"No state machine found for '{self.name}'")

        self.initial_state = machine.get("initial")
        self.current_state = self.initial_state  # Start in the initial state

        for state in machine.find("states"):
            self.states[state.get("name")] = {
                "transitions": [(t.get("event"), t.get("target")) for t in state.findall("transition")]
            }
        
        for event in machine.find("events"):
            self.events[event.get("name")] = event.get("target_machine")
        
        for guard in machine.find("guards"):
            self.guards[guard.get("name")] = {
                "threshold": float(guard.get("threshold")),
                "failure_probability": float(guard.get("failure_probability", 0))
            }

    def reset(self):
        """Reset the state machine to its initial state."""
        self.current_state = self.initial_state

    def goto(self, state_name):
        """Directly set the current state to a specified state."""
        if state_name in self.states:
            self.current_state = state_name
        else:
            raise ValueError(f"State '{state_name}' does not exist in {self.name}")
        
    async def process_event(self, event_name):
        """Process an event, handling inter-machine communication and transitions."""
        target_machine = self.events.get(event_name)
        if target_machine:
            print(f"{self.name}: Sending {event_name} to {target_machine}")
            # Notify other machine here if using an inter-process communication system
        else:
            print(f"{self.name}: Processing event {event_name}")
            await self.evaluate_transitions(event_name)

    async def evaluate_transitions(self, event_name):
        """Evaluate and perform transitions for the current state based on event and guards."""
        for transition_event, target_state in self.states[self.current_state]["transitions"]:
            if transition_event == event_name and await self.check_guards(event_name):
                self.current_state = target_state
                print(f"{self.name}: Transitioned to {self.current_state}")
                break

    async def check_guards(self, event_name):
        """Check guard conditions for sensors, timeouts, and thresholds."""
        if event_name.startswith("timeout"):
            timeout_secs = int(event_name.split("=")[1].strip("s"))
            deadline = datetime.now() + timedelta(seconds=timeout_secs)
            while datetime.now() < deadline:
                await asyncio.sleep(0.1)
            return True
        elif event_name == "pressure_sensor":
            return random.random() > self.guards["pressure_sensor"]["threshold"]
        elif event_name == "light_sensor":
            return random.random() > self.guards["light_sensor"]["threshold"]
        return True
