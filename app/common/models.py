"""
SQLAlchemy ORM models for database persistence.

This module defines all database models used across services.
"""

from app.common.db import Base, SQLALCHEMY_AVAILABLE
from app.common.middleware import get_logger

logger = get_logger(__name__)

if SQLALCHEMY_AVAILABLE:
    from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, Index
    from sqlalchemy.dialects.postgresql import UUID
    import uuid
    
    class LogEventORM(Base):
        """SQLAlchemy ORM model for log events."""
        __tablename__ = "log_events"
        
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
        timestamp = Column(DateTime, nullable=False, index=True)
        stage = Column(String(50), nullable=False, index=True)
        service = Column(String(100), nullable=False, index=True)
        level = Column(String(20), nullable=False, index=True)  # INFO, ERROR, WARNING
        message = Column(Text, nullable=True)
        context = Column(JSON, nullable=True)  # Merged request/response/metadata
        correlation_id = Column(String(100), nullable=True, index=True)
        success = Column(Boolean, nullable=False, default=True)
        created_at = Column(DateTime, nullable=False, server_default='now()')
        
        # Composite indexes for common queries
        __table_args__ = (
            Index('idx_stage_service', 'stage', 'service'),
            Index('idx_timestamp_stage', 'timestamp', 'stage'),
            Index('idx_correlation_id', 'correlation_id'),
        )
        
        def __repr__(self):
            return f"<LogEventORM(id={self.id}, stage={self.stage}, service={self.service}, level={self.level})>"
else:
    LogEventORM = None

