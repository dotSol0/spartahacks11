"""
Utility functions for logging, metrics, and data processing.
"""

import logging
from typing import Dict, Any
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MetricsRecorder:
    """Records and exports metrics for analysis."""
    
    def __init__(self, output_dir: str = "logs/metrics"):
        """
        Initialize metrics recorder.
        
        Args:
            output_dir: Directory to save metrics
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = []
        
    def record_frame_analysis(self, timestamp: float, face_forward: bool, eyes_forward: bool,
                             distraction_level: str, details: Dict[str, Any]) -> None:
        """
        Record frame analysis results.
        
        Args:
            timestamp: Frame timestamp
            face_forward: Whether face is forward
            eyes_forward: Whether eyes are forward
            distraction_level: Current distraction level
            details: Additional details
        """
        metric = {
            'timestamp': timestamp,
            'face_forward': face_forward,
            'eyes_forward': eyes_forward,
            'distraction_level': distraction_level,
            'details': details
        }
        self.metrics.append(metric)
    
    def export_metrics(self, filename: str = None) -> str:
        """
        Export metrics to JSON file.
        
        Args:
            filename: Output filename (auto-generated if None)
            
        Returns:
            str: Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            logger.info(f"Metrics exported to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return ""
    
    def clear_metrics(self) -> None:
        """Clear recorded metrics."""
        self.metrics = []


class FrameRecorder:
    """Records frames for debugging and analysis."""
    
    def __init__(self, output_dir: str = "logs/frames", max_frames: int = 1000):
        """
        Initialize frame recorder.
        
        Args:
            output_dir: Directory to save frames
            max_frames: Maximum frames to keep
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_frames = max_frames
        self.frame_count = 0
    
    def save_frame(self, frame, frame_type: str = "analysis") -> bool:
        """
        Save a frame to disk.
        
        Args:
            frame: Frame to save (numpy array)
            frame_type: Type of frame (analysis, raw, debug)
            
        Returns:
            bool: True if saved successfully
        """
        # TODO: Implement frame saving
        # Use OpenCV to save frames
        # Implement frame cleanup when max_frames exceeded
        return False


class PerformanceMonitor:
    """Monitors system performance metrics."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.frame_times = []
        self.analysis_times = []
        
    def record_frame_time(self, frame_time: float) -> None:
        """Record frame processing time."""
        self.frame_times.append(frame_time)
        
    def record_analysis_time(self, analysis_time: float) -> None:
        """Record analysis processing time."""
        self.analysis_times.append(analysis_time)
    
    def get_fps(self) -> float:
        """
        Calculate average FPS.
        
        Returns:
            float: Average frames per second
        """
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = sum(self.frame_times[-100:]) / len(self.frame_times[-100:])
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def get_stats(self) -> Dict[str, float]:
        """
        Get performance statistics.
        
        Returns:
            dict: Statistics including avg times and FPS
        """
        if not self.frame_times or not self.analysis_times:
            return {}
        
        return {
            'avg_frame_time': sum(self.frame_times) / len(self.frame_times),
            'avg_analysis_time': sum(self.analysis_times) / len(self.analysis_times),
            'fps': self.get_fps(),
            'total_frames': len(self.frame_times)
        }
