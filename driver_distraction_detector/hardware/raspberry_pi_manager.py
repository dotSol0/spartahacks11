"""
Raspberry Pi connection and management module.
Handles Bluetooth connection to Raspberry Pi device.
"""

import logging
from typing import Optional, Dict, Any
import bluetooth

logger = logging.getLogger(__name__)


class RaspberryPiManager:
    """Manages connection and communication with Raspberry Pi via Bluetooth."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Raspberry Pi manager.
        
        Args:
            config: Configuration dictionary containing connection parameters
        """
        self.config = config
        self.socket = None
        self.connected = False
        self.pi_address = config.get('raspberry_pi', {}).get('bluetooth_address')
        self.pi_port = config.get('raspberry_pi', {}).get('bluetooth_port', 1)
        
    def connect(self) -> bool:
        """
        Establish Bluetooth connection to Raspberry Pi.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to Raspberry Pi at {self.pi_address}...")
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.pi_address, self.pi_port))
            self.connected = True
            logger.info("Successfully connected to Raspberry Pi")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Raspberry Pi: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from Raspberry Pi."""
        try:
            if self.socket:
                self.socket.close()
            self.connected = False
            logger.info("Disconnected from Raspberry Pi")
        except Exception as e:
            logger.error(f"Error disconnecting from Raspberry Pi: {e}")
    
    def send_command(self, command: str) -> bool:
        """
        Send command to Raspberry Pi.
        
        Args:
            command: Command string to send
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.connected:
            logger.error("Not connected to Raspberry Pi")
            return False
        
        try:
            self.socket.send(command.encode())
            logger.debug(f"Sent command: {command}")
            return True
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    def receive_data(self, buffer_size: int = 1024) -> Optional[bytes]:
        """
        Receive data from Raspberry Pi.
        
        Args:
            buffer_size: Size of receive buffer
            
        Returns:
            bytes: Received data or None if error
        """
        if not self.connected:
            logger.error("Not connected to Raspberry Pi")
            return None
        
        try:
            data = self.socket.recv(buffer_size)
            return data if data else None
        except Exception as e:
            logger.error(f"Failed to receive data: {e}")
            return None
    
    def is_connected(self) -> bool:
        """
        Check if connected to Raspberry Pi.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected
