from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkflowState:
    state: str = "DRAFT"


class WorkflowManager:
    def __init__(self):
        self.state = WorkflowState()

    def trigger_replan(self):
        self.state.state = "PENDING_REVIEW"
        return {"status": "replanning", "state": self.state.state}

    def approve(self):
        self.state.state = "APPROVED"
        return {"status": "approved", "state": self.state.state}

    def reject(self):
        self.state.state = "REJECTED"
        return {"status": "rejected", "state": self.state.state}
