"""
Main entry point for the Driver Distraction Detector system.
Orchestrates the hardware connection, camera stream, vision pipeline, and alerting.
"""

from hardware.raspberry_pi_manager import RaspberryPiManager
from hardware.camera_manager import CameraManager
from vision.face_mesh_analyzer import FaceMeshAnalyzer
from analysis.distraction_analyzer import DistractionAnalyzer
from alerting.alert_manager import AlertManager
from config.settings import load_config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DriverDistractionDetectorSystem:
    """Main system coordinator for driver distraction detection."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the distraction detector system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.pi_manager = None
        self.camera_manager = None
        self.face_mesh_analyzer = None
        self.distraction_analyzer = None
        self.alert_manager = None
        
    def initialize(self) -> bool:
        """
        Initialize all system components.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing Raspberry Pi connection...")
            self.pi_manager = RaspberryPiManager(self.config)
            
            logger.info("Initializing camera manager...")
            self.camera_manager = CameraManager(self.config)
            
            logger.info("Initializing face mesh analyzer...")
            self.face_mesh_analyzer = FaceMeshAnalyzer(self.config)
            
            logger.info("Initializing distraction analyzer...")
            self.distraction_analyzer = DistractionAnalyzer(self.config)
            
            logger.info("Initializing alert manager...")
            self.alert_manager = AlertManager(self.config)
            
            logger.info("System initialized successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize system: {e}")
            return False
    
    def start(self) -> None:
        """Start the main detection loop."""
        try:
            logger.info("Starting driver distraction detection system...")
            self.run_detection_loop()
        except KeyboardInterrupt:
            logger.info("System interrupted by user")
            self.shutdown()
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
            self.shutdown()
    
    def run_detection_loop(self) -> None:
        """
        Main detection loop.
        Continuously captures frames and analyzes them for distraction.
        """
        # TODO: Implement detection loop
        # 1. Get frame from camera at 1 FPS
        # 2. Pass to face mesh analyzer
        # 3. Check results and pass to distraction analyzer
        # 4. Alert if necessary
        pass
    
    def shutdown(self) -> None:
        """Shutdown all system components gracefully."""
        logger.info("Shutting down system...")
        if self.camera_manager:
            self.camera_manager.disconnect()
        if self.pi_manager:
            self.pi_manager.disconnect()
        logger.info("System shutdown complete")


def main():
    """Entry point for the application."""
    system = DriverDistractionDetectorSystem()
    if system.initialize():
        system.start()
    else:
        logger.error("Failed to initialize system")


if __name__ == "__main__":
    main()
