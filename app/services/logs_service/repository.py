"""
Repository for log event persistence.

Handles database operations for log events.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from app.common.db import get_db_session, is_db_available, SQLALCHEMY_AVAILABLE
from app.common.middleware import get_logger

logger = get_logger(__name__)

# Try to import SQLAlchemy (optional dependency)
if SQLALCHEMY_AVAILABLE:
    try:
        from sqlalchemy import and_, func
        from app.common.models import LogEventORM
    except ImportError:
        LogEventORM = None
        func = None
else:
    LogEventORM = None
    func = None


class LogEventRepository:
    """Repository for log event database operations."""
    
    @staticmethod
    def create_log_event(
        timestamp: datetime,
        stage: str,
        service: str,
        level: str,
        message: Optional[str],
        context: Optional[Dict[str, Any]],
        correlation_id: Optional[str] = None,
        success: bool = True
    ) -> Optional[str]:
        """
        Create a new log event in the database.
        
        Args:
            timestamp: Event timestamp
            stage: Workflow stage
            service: Service name
            level: Log level (INFO, ERROR, WARNING)
            message: Event message
            context: Merged request/response/metadata
            correlation_id: Optional correlation ID
            success: Whether operation was successful
            
        Returns:
            Event ID (UUID string) if successful, None otherwise
        """
        if not is_db_available() or not SQLALCHEMY_AVAILABLE or LogEventORM is None:
            logger.warning("Database not available, skipping log event persistence")
            return None
        
        try:
            with get_db_session() as db:
                if db is None:
                    return None
                
                log_event = LogEventORM(
                    timestamp=timestamp,
                    stage=stage,
                    service=service,
                    level=level,
                    message=message,
                    context=context,
                    correlation_id=correlation_id,
                    success=success
                )
                
                db.add(log_event)
                db.commit()
                db.refresh(log_event)
                
                event_id = str(log_event.id)
                logger.debug(f"Created log event in database: {event_id}")
                return event_id
                
        except Exception as e:
            logger.error(f"Error creating log event in database: {e}", exc_info=True)
            return None
    
    @staticmethod
    def query_logs(
        stage: Optional[str] = None,
        service: Optional[str] = None,
        correlation_id: Optional[str] = None,
        level: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Query log events with filters.
        
        Args:
            stage: Filter by stage
            service: Filter by service
            correlation_id: Filter by correlation ID
            level: Filter by log level
            start_time: Filter by start time
            end_time: Filter by end time
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            Tuple of (list of log events as dicts, total count)
        """
        if not is_db_available() or not SQLALCHEMY_AVAILABLE or LogEventORM is None:
            logger.warning("Database not available, returning empty results")
            return [], 0
        
        try:
            with get_db_session() as db:
                if db is None:
                    return [], 0
                
                # Build query with filters
                query = db.query(LogEventORM)
                
                if stage:
                    query = query.filter(LogEventORM.stage == stage)
                
                if service:
                    query = query.filter(LogEventORM.service == service)
                
                if correlation_id:
                    query = query.filter(LogEventORM.correlation_id == correlation_id)
                
                if level:
                    query = query.filter(LogEventORM.level == level)
                
                if start_time:
                    query = query.filter(LogEventORM.timestamp >= start_time)
                
                if end_time:
                    query = query.filter(LogEventORM.timestamp <= end_time)
                
                # Get total count
                total_count = query.count()
                
                # Apply pagination
                query = query.order_by(LogEventORM.timestamp.desc())
                query = query.limit(limit).offset(offset)
                
                # Execute query
                log_events = query.all()
                
                # Convert to dicts
                results = []
                for event in log_events:
                    results.append({
                        "id": str(event.id),
                        "timestamp": event.timestamp.isoformat(),
                        "stage": event.stage,
                        "service": event.service,
                        "level": event.level,
                        "message": event.message,
                        "context": event.context,
                        "correlation_id": event.correlation_id,
                        "success": event.success
                    })
                
                logger.debug(f"Queried {len(results)} log events (total: {total_count})")
                return results, total_count
                
        except Exception as e:
            logger.error(f"Error querying log events: {e}", exc_info=True)
            return [], 0
    
    @staticmethod
    def get_analytics() -> Dict[str, Dict[str, int]]:
        """
        Get aggregated analytics from log events.
        
        Returns:
            Dictionary with by_stage, by_service, and levels counts
        """
        if not is_db_available() or not SQLALCHEMY_AVAILABLE or LogEventORM is None or func is None:
            logger.warning("Database not available, returning empty analytics")
            return {
                "by_stage": {},
                "by_service": {},
                "levels": {}
            }
        
        try:
            with get_db_session() as db:
                if db is None:
                    return {
                        "by_stage": {},
                        "by_service": {},
                        "levels": {}
                    }
                
                # Count by stage
                stage_counts = db.query(
                    LogEventORM.stage,
                    func.count(LogEventORM.id)
                ).group_by(LogEventORM.stage).all()
                
                by_stage = {stage: count for stage, count in stage_counts}
                
                # Count by service
                service_counts = db.query(
                    LogEventORM.service,
                    func.count(LogEventORM.id)
                ).group_by(LogEventORM.service).all()
                
                by_service = {service: count for service, count in service_counts}
                
                # Count by level
                level_counts = db.query(
                    LogEventORM.level,
                    func.count(LogEventORM.id)
                ).group_by(LogEventORM.level).all()
                
                levels = {level: count for level, count in level_counts}
                
                logger.debug(f"Generated analytics: {len(by_stage)} stages, {len(by_service)} services, {len(levels)} levels")
                
                return {
                    "by_stage": by_stage,
                    "by_service": by_service,
                    "levels": levels
                }
                
        except Exception as e:
            logger.error(f"Error generating analytics: {e}", exc_info=True)
            return {
                "by_stage": {},
                "by_service": {},
                "levels": {}
            }

