"""
Distraction analysis module.
Tracks face and eye failures over time and determines consequences.
OPTIMIZED FOR LOW MEMORY SYSTEMS (4GB Pi)
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class DistractionLevel(Enum):
    """Levels of driver distraction."""
    SAFE = 0
    WARNING = 1
    CRITICAL = 2
    SEVERE = 3


@dataclass
class DistractionEvent:
    """Record of a distraction event."""
    event_type: str  # 'face_failure', 'eye_failure'
    timestamp: float
    severity: DistractionLevel
    details: Dict[str, Any]


@dataclass
class AnalysisResult:
    """Result of distraction analysis."""
    current_level: DistractionLevel
    face_failure_count: int
    eye_failure_count: int
    total_failure_count: int
    consequence: str
    recommendation: str
    events: List[DistractionEvent]


class DistractionAnalyzer:
    """Analyzes distraction patterns and determines consequences - OPTIMIZED."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize distraction analyzer with low memory footprint.
        
        Args:
            config: Configuration dictionary with thresholds
        """
        self.config = config
        self.face_failure_count = 0
        self.eye_failure_count = 0
        self.total_failure_count = 0
        self.recent_events: List[DistractionEvent] = []
        
        # Load configuration thresholds
        analysis_config = config.get('analysis', {})
        self.warning_threshold = analysis_config.get('warning_threshold', 5)
        self.critical_threshold = analysis_config.get('critical_threshold', 10)
        self.severe_threshold = analysis_config.get('severe_threshold', 20)
        self.history_window = analysis_config.get('history_window', 120)  # 2 min (reduced from 5 min)
        self.max_events_buffer = analysis_config.get('max_events_buffer', 100)  # Cap memory usage
        
        logger.info(f"Distraction analyzer initialized (MAX_EVENTS: {self.max_events_buffer})")
    
    def process_frame_result(self, face_forward: bool, eyes_forward: bool, timestamp: float) -> AnalysisResult:
        """
        Process face mesh analysis results and track distraction.
        
        Args:
            face_forward: Whether face is pointing towards road
            eyes_forward: Whether eyes are looking forward
            timestamp: Timestamp of analysis
            
        Returns:
            AnalysisResult: Current distraction analysis
        """
        # Track failures
        if not face_forward:
            self.face_failure_count += 1
            self.total_failure_count += 1
            event = DistractionEvent(
                event_type='face_failure',
                timestamp=timestamp,
                severity=self._get_severity_level(),
                details={'reason': 'face not pointing towards road'}
            )
            self._add_event(event)
            logger.warning("Face failure detected")
        
        if not eyes_forward:
            self.eye_failure_count += 1
            self.total_failure_count += 1
            event = DistractionEvent(
                event_type='eye_failure',
                timestamp=timestamp,
                severity=self._get_severity_level(),
                details={'reason': 'eyes not looking forward'}
            )
            self._add_event(event)
            logger.warning("Eye failure detected")
        
        # Clean old events outside history window
        self._cleanup_old_events(timestamp)
        
        # Determine distraction level
        current_level = self._determine_distraction_level()
        
        # Generate consequence and recommendation
        consequence = self._determine_consequence(current_level)
        recommendation = self._get_recommendation(current_level)
        
        return AnalysisResult(
            current_level=current_level,
            face_failure_count=self.face_failure_count,
            eye_failure_count=self.eye_failure_count,
            total_failure_count=self.total_failure_count,
            consequence=consequence,
            recommendation=recommendation,
            events=self.recent_events.copy()
        )
    
    def _add_event(self, event: DistractionEvent) -> None:
        """Add event with memory cap."""
        self.recent_events.append(event)
        # Cap event buffer to prevent memory bloat
        if len(self.recent_events) > self.max_events_buffer:
            self.recent_events = self.recent_events[-self.max_events_buffer:]
    
    def _get_severity_level(self) -> DistractionLevel:
        """
        Determine severity level based on current failure counts.
        
        Returns:
            DistractionLevel: Current severity level
        """
        return self._determine_distraction_level()
    
    def _determine_distraction_level(self) -> DistractionLevel:
        """
        Determine overall distraction level based on failure counts.
        
        Returns:
            DistractionLevel: Current distraction level
        """
        # TODO: Implement logic to determine distraction level
        # Consider:
        # - Consecutive failures
        # - Failure frequency
        # - Failure type combinations
        
        if self.total_failure_count >= self.severe_threshold:
            return DistractionLevel.SEVERE
        elif self.total_failure_count >= self.critical_threshold:
            return DistractionLevel.CRITICAL
        elif self.total_failure_count >= self.warning_threshold:
            return DistractionLevel.WARNING
        else:
            return DistractionLevel.SAFE
    
    def _determine_consequence(self, level: DistractionLevel) -> str:
        """
        Determine consequence based on distraction level.
        
        Args:
            level: Current distraction level
            
        Returns:
            str: Consequence action
        """
        # TODO: Implement consequence logic
        # SAFE: No action
        # WARNING: Visual alert to driver
        # CRITICAL: Audible alert + system slowdown
        # SEVERE: Emergency intervention (brake assist, lane assist)
        
        consequences = {
            DistractionLevel.SAFE: "No action required",
            DistractionLevel.WARNING: "Visual alert to driver",
            DistractionLevel.CRITICAL: "Audible alert + enhanced monitoring",
            DistractionLevel.SEVERE: "Emergency intervention active"
        }
        
        return consequences.get(level, "Unknown")
    
    def _get_recommendation(self, level: DistractionLevel) -> str:
        """
        Get recommendation for driver.
        
        Args:
            level: Current distraction level
            
        Returns:
            str: Recommendation message
        """
        # TODO: Implement recommendation logic
        recommendations = {
            DistractionLevel.SAFE: "Stay focused on the road",
            DistractionLevel.WARNING: "Keep your eyes on the road",
            DistractionLevel.CRITICAL: "Pull over safely if possible",
            DistractionLevel.SEVERE: "Immediate driver attention required"
        }
        
        return recommendations.get(level, "Unknown")
    
    def _cleanup_old_events(self, current_timestamp: float) -> None:
        """
        Remove events older than history window.
        
        Args:
            current_timestamp: Current timestamp
        """
        cutoff_time = current_timestamp - self.history_window
        self.recent_events = [
            event for event in self.recent_events
            if event.timestamp > cutoff_time
        ]
    
    def reset_counters(self) -> None:
        """Reset failure counters."""
        self.face_failure_count = 0
        self.eye_failure_count = 0
        self.total_failure_count = 0
        self.recent_events = []
        logger.info("Distraction counters reset")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics.
        
        Returns:
            dict: Statistics including failure counts and rates
        """
        return {
            'face_failures': self.face_failure_count,
            'eye_failures': self.eye_failure_count,
            'total_failures': self.total_failure_count,
            'recent_events': len(self.recent_events),
            'distraction_level': self._determine_distraction_level().name
        }
