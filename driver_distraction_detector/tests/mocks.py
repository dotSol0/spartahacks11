"""
Mock objects and fixtures for testing.
"""

import numpy as np
from typing import Dict, Any


class MockCameraManager:
    """Mock camera manager for testing."""
    
    def __init__(self):
        self.connected = False
    
    def get_frame(self):
        """Get mock frame."""
        return np.zeros((480, 640, 3), dtype=np.uint8)


class MockFaceMeshAnalyzer:
    """Mock face mesh analyzer for testing."""
    
    def analyze_frame(self, frame):
        """Analyze mock frame."""
        from vision.face_mesh_analyzer import FaceAnalysisResult
        return FaceAnalysisResult(
            face_detected=True,
            face_orientation='forward',
            eye_gaze='forward',
            face_confidence=0.95,
            landmarks=np.random.rand(468, 3),
            raw_angles={'head_pitch': 0, 'head_yaw': 0, 'eye_gaze_x': 0, 'eye_gaze_y': 0},
            timestamp=0
        )
