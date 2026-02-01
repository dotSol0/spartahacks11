"""
Camera stream management module.
Handles receiving and processing image frames from Raspberry Pi camera.
OPTIMIZED FOR LOW MEMORY SYSTEMS (4GB Pi)
"""

import logging
from typing import Optional, Dict, Any
import cv2
import numpy as np
from threading import Thread, Event
from queue import Queue
import time

logger = logging.getLogger(__name__)


class CameraManager:
    """Manages camera stream reception and frame buffering - LOW MEMORY VERSION."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize camera manager with minimal memory overhead.
        
        Args:
            config: Configuration dictionary with camera settings
        """
        self.config = config
        # Use small queue size for minimal memory
        self.frame_queue = Queue(maxsize=1)  # Only keep 1 frame (down from 2)
        self.capture_thread = None
        self.is_streaming = False
        self.target_fps = config.get('camera', {}).get('target_fps', 1)
        self.frame_width = config.get('camera', {}).get('width', 320)
        self.frame_height = config.get('camera', {}).get('height', 240)
        self.frame_skip = config.get('camera', {}).get('frame_skip', 1)
        self.compress_frames = config.get('raspberry_pi', {}).get('compress_frames', True)
        self.compression_quality = config.get('raspberry_pi', {}).get('compression_quality', 70)
        self.stop_event = Event()
        self.frame_counter = 0
        
    def connect(self) -> bool:
        """
        Connect to camera stream.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to camera stream ({self.frame_width}x{self.frame_height})...")
            self.is_streaming = True
            self.start_frame_capture()
            logger.info("Camera connected successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to camera: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from camera."""
        try:
            self.is_streaming = False
            self.stop_event.set()
            if self.capture_thread:
                self.capture_thread.join(timeout=5)
            logger.info("Camera disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting camera: {e}")
    
    def start_frame_capture(self) -> None:
        """Start background thread for frame capture."""
        if self.capture_thread is None or not self.capture_thread.is_alive():
            self.stop_event.clear()
            self.capture_thread = Thread(target=self._capture_frames, daemon=True)
            self.capture_thread.start()
            logger.info("Frame capture thread started")
    
    def _capture_frames(self) -> None:
        """
        Capture frames from camera stream in background thread.
        Maintains target FPS and buffers frames with frame skipping.
        """
        frame_interval = 1.0 / self.target_fps
        last_frame_time = time.time()
        
        while not self.stop_event.is_set():
            try:
                current_time = time.time()
                elapsed = current_time - last_frame_time
                
                if elapsed >= frame_interval:
                    self.frame_counter += 1
                    
                    # Skip frames if configured
                    if self.frame_counter % self.frame_skip == 0:
                        frame = self._get_frame_from_stream()
                        
                        if frame is not None:
                            # Compress frame if enabled (reduce memory)
                            if self.compress_frames:
                                frame = self._compress_frame(frame)
                            
                            # Discard old frame and add new one
                            try:
                                self.frame_queue.put_nowait(frame)
                            except:
                                try:
                                    self.frame_queue.get_nowait()
                                    self.frame_queue.put_nowait(frame)
                                except:
                                    pass
                    
                    last_frame_time = current_time
                else:
                    time.sleep(0.01)
                    
            except Exception as e:
                logger.error(f"Error in frame capture: {e}")
    
    def _compress_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Compress frame to reduce memory footprint.
        
        Args:
            frame: Input frame
            
        Returns:
            np.ndarray: Compressed frame
        """
        # Encode to JPEG and decode to simulate transmission compression
        _, compressed = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.compression_quality])
        frame = cv2.imdecode(compressed, cv2.IMREAD_COLOR)
        return frame
    
    def _get_frame_from_stream(self) -> Optional[np.ndarray]:
        """
        Get a frame from the camera stream.
        
        Returns:
            np.ndarray: Frame or None if unavailable
        """
        # TODO: Implement actual frame retrieval from Raspberry Pi
        return None
    
    def get_frame(self, timeout: float = 0.5) -> Optional[np.ndarray]:
        """
        Get latest frame from queue (reduced timeout for efficiency).
        
        Args:
            timeout: Timeout in seconds to wait for frame
            
        Returns:
            np.ndarray: Latest frame or None if not available
        """
        try:
            frame = self.frame_queue.get(timeout=timeout)
            return frame
        except:
            return None
    
    def get_frame_specs(self) -> Dict[str, int]:
        """
        Get camera frame specifications.
        
        Returns:
            dict: Frame width, height, and target FPS
        """
        return {
            'width': self.frame_width,
            'height': self.frame_height,
            'fps': self.target_fps
        }
