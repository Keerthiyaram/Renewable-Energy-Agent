from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base


class WorkflowRun(Base):
    """Workflow execution tracking model."""
    
    __tablename__ = "workflow_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    trigger_type = Column(String)  # manual, scheduled, event_driven
    trigger_details = Column(Text)  # JSON string
    input_state = Column(Text)  # JSON string
    output_state = Column(Text)  # JSON string
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<WorkflowRun {self.workflow_id}: {self.status}>"
