from state import InputState, OutputState, OverallState
from reasoner import Reasoner
from canonical_conversion import CanonicalConversion
from PineconeDBManager import PineconeDBManager
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from typing import Literal
from langgraph.types import interrupt, Command
import os
from langchain_community.tools import HumanInputRun

class WorkflowManager:
    def __init__(self):
        # Construct the path relative to the current file's directory.
        self.reasoner = Reasoner()
        self.PineconeDBManager = PineconeDBManager()
        self.canonical_conversion = CanonicalConversion()
    def create_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(OverallState, input=InputState, output=OutputState)
        
        # Add nodes to the graph
        workflow.add_node("Canonical_conversion", self.canonical_conversion.run)
        workflow.add_node("Reasoner", self.reasoner.run)
        workflow.add_node("save_example", self.PineconeDBManager.save_example)
        # Add edges to the graph
        workflow.add_edge(START, "Canonical_conversion")
        workflow.add_edge("Canonical_conversion", "Reasoner")
        workflow.add_edge("Reasoner", "save_example")
        workflow.add_edge("save_example", END)
        return workflow
    
    def returnGraph(self):
        return self.create_workflow().compile(interrupt_after=['Canonical_conversion', 'Reasoner'])