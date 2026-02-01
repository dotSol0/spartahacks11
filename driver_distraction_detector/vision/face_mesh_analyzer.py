"""
Face Mesh analysis using MediaPipe.
Detects facial landmarks and determines if face is oriented towards road and eyes are forward.
OPTIMIZED FOR LOW MEMORY SYSTEMS (4GB Pi)
"""

from __future__ import annotations
import logging
from typing import Optional, Dict, Any, Tuple, List
import cv2
import numpy as np
import mediapipe as mp
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FaceAnalysisResult:
    """Result of face analysis."""
    face_detected: bool
    face_orientation: Optional[str]  # 'forward', 'left', 'right', 'down', 'up'
    eye_gaze: Optional[str]  # 'forward', 'left', 'right', 'down', 'up'
    face_confidence: float
    landmarks: Optional[np.ndarray]
    raw_angles: Optional[Dict[str, float]]  # head_pitch, head_yaw, eye_gaze_x, eye_gaze_y
    timestamp: float


class FaceMeshAnalyzer:
    """Analyzes face orientation and eye gaze using MediaPipe Face Mesh - OPTIMIZED."""
    
    # MediaPipe Face Mesh landmark indices
    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    FACE_OVAL_INDICES = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Face Mesh analyzer with low memory settings.
        
        Args:
            config: Configuration dictionary with model parameters
        """
        self.config = config
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # Use lite model if available (much smaller memory footprint)
        use_lite = config.get('vision', {}).get('use_lite_model', True)
        model_name = 'face_landmarker_lite.task' if use_lite else 'face_landmarker.task'
        
        # Initialize with minimal resource usage
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=config.get('vision', {}).get('static_image_mode', False),
            max_num_faces=config.get('vision', {}).get('max_num_faces', 1),
            refine_landmarks=False,  # Disable refinement to save memory
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Thresholds for orientation detection (in degrees)
        self.yaw_threshold = config.get('vision', {}).get('yaw_threshold', 20)
        self.pitch_threshold = config.get('vision', {}).get('pitch_threshold', 15)
        self.roll_threshold = config.get('vision', {}).get('roll_threshold', 20)
        
        logger.info("Face Mesh analyzer initialized (LOW MEMORY MODE)")
    
    def analyze_frame(self, frame: np.ndarray) -> FaceAnalysisResult:
        """
        Analyze a single frame for face orientation and eye gaze.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            FaceAnalysisResult: Analysis results
        """
        try:
            import time
            timestamp = time.time()
            
            # Keep frame as-is if already correct size, else resize minimally
            if frame.shape[:2] != (240, 320):
                frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_LINEAR)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks or len(results.multi_face_landmarks) == 0:
                return FaceAnalysisResult(
                    face_detected=False,
                    face_orientation=None,
                    eye_gaze=None,
                    face_confidence=0.0,
                    landmarks=None,
                    raw_angles=None,
                    timestamp=timestamp
                )
            
            # Get first face landmarks
            face_landmarks = results.multi_face_landmarks[0]
            landmarks_array = self._landmarks_to_array(face_landmarks)
            
            # Calculate head orientation
            head_pitch, head_yaw, head_roll = self._calculate_head_orientation(landmarks_array)
            
            # Calculate eye gaze direction
            eye_gaze_x, eye_gaze_y = self._calculate_eye_gaze(landmarks_array)
            
            # Determine face orientation classification
            face_orientation = self._classify_face_orientation(head_pitch, head_yaw, head_roll)
            
            # Determine eye gaze classification
            eye_gaze = self._classify_eye_gaze(eye_gaze_x, eye_gaze_y)
            
            # Calculate confidence (0-1)
            face_confidence = self._calculate_face_confidence(landmarks_array)
            
            raw_angles = {
                'head_pitch': head_pitch,
                'head_yaw': head_yaw,
                'head_roll': head_roll,
                'eye_gaze_x': eye_gaze_x,
                'eye_gaze_y': eye_gaze_y
            }
            
            return FaceAnalysisResult(
                face_detected=True,
                face_orientation=face_orientation,
                eye_gaze=eye_gaze,
                face_confidence=face_confidence,
                landmarks=landmarks_array,
                raw_angles=raw_angles,
                timestamp=timestamp
            )
            
        except Exception as e:
            logger.error(f"Error analyzing frame: {e}")
            return FaceAnalysisResult(
                face_detected=False,
                face_orientation=None,
                eye_gaze=None,
                face_confidence=0.0,
                landmarks=None,
                raw_angles=None,
                timestamp=None
            )
    
    def _landmarks_to_array(self, face_landmarks) -> np.ndarray:
        """
        Convert MediaPipe landmarks to numpy array (using float32 to save memory).
        
        Args:
            face_landmarks: MediaPipe face landmarks
            
        Returns:
            np.ndarray: Landmarks as (468, 3) array with normalized coordinates
        """
        landmarks = np.array([[lm.x, lm.y, lm.z] for lm in face_landmarks.landmark], dtype=np.float32)
        return landmarks
    
    def _calculate_head_orientation(self, landmarks: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate head orientation angles (pitch, yaw, roll) in degrees.
        
        Args:
            landmarks: Face landmarks array
            
        Returns:
            Tuple[float, float, float]: pitch, yaw, roll angles in degrees
        """
        # TODO: Implement head pose estimation
        # Use 3D landmarks and reference points to calculate head orientation
        # Return: pitch (up/down), yaw (left/right), roll (tilt)
        pitch = 0.0  # Placeholder
        yaw = 0.0    # Placeholder
        roll = 0.0   # Placeholder
        return pitch, yaw, roll
    
    def _calculate_eye_gaze(self, landmarks: np.ndarray) -> Tuple[float, float]:
        """
        Calculate eye gaze direction.
        
        Args:
            landmarks: Face landmarks array
            
        Returns:
            Tuple[float, float]: gaze_x, gaze_y (in degrees or normalized units)
        """
        # TODO: Implement eye gaze estimation
        # Use iris landmarks or eye corner positions to determine gaze direction
        gaze_x = 0.0  # Placeholder
        gaze_y = 0.0  # Placeholder
        return gaze_x, gaze_y
    
    def _classify_face_orientation(self, pitch: float, yaw: float, roll: float) -> str:
        """
        Classify face orientation based on angles.
        
        Args:
            pitch: Head pitch angle (up/down)
            yaw: Head yaw angle (left/right)
            roll: Head roll angle (tilt)
            
        Returns:
            str: Orientation classification ('forward', 'left', 'right', 'down', 'up')
        """
        # TODO: Implement classification logic based on thresholds
        # If yaw > yaw_threshold: 'right'
        # If yaw < -yaw_threshold: 'left'
        # If pitch > pitch_threshold: 'down'
        # If pitch < -pitch_threshold: 'up'
        # Else: 'forward'
        return 'forward'  # Placeholder
    
    def _classify_eye_gaze(self, gaze_x: float, gaze_y: float) -> str:
        """
        Classify eye gaze direction.
        
        Args:
            gaze_x: Eye gaze X component
            gaze_y: Eye gaze Y component
            
        Returns:
            str: Gaze classification ('forward', 'left', 'right', 'down', 'up')
        """
        # TODO: Implement eye gaze classification
        return 'forward'  # Placeholder
    
    def _calculate_face_confidence(self, landmarks: np.ndarray) -> float:
        """
        Calculate confidence in face detection.
        
        Args:
            landmarks: Face landmarks array
            
        Returns:
            float: Confidence score 0-1
        """
        # TODO: Calculate confidence based on landmark quality
        return 1.0  # Placeholder
    
    def is_face_forward(self, result: FaceAnalysisResult) -> bool:
        """
        Check if face is pointing towards road.
        
        Args:
            result: FaceAnalysisResult from analyze_frame
            
        Returns:
            bool: True if face is forward-facing
        """
        if not result.face_detected:
            return False
        return result.face_orientation == 'forward'
    
    def are_eyes_forward(self, result: FaceAnalysisResult) -> bool:
        """
        Check if eyes are looking forward.
        
        Args:
            result: FaceAnalysisResult from analyze_frame
            
        Returns:
            bool: True if eyes are looking forward
        """
        if not result.face_detected:
            return False
        return result.eye_gaze == 'forward'
    
    def shutdown(self) -> None:
        """Shutdown the face mesh detector."""
        if self.face_mesh:
            self.face_mesh.close()
            logger.info("Face Mesh analyzer shutdown")
