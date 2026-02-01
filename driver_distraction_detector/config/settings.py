"""
Configuration loader and settings management.
"""

import logging
import yaml
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return get_default_config()
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config if config else get_default_config()
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration.
    
    Returns:
        dict: Default configuration dictionary
    """
    return {
        'raspberry_pi': {
            'bluetooth_address': 'B8:27:EB:XX:XX:XX',  # Update with your Pi's address
            'bluetooth_port': 1,
        },
        'camera': {
            'target_fps': 1,
            'width': 640,
            'height': 480,
        },
        'vision': {
            'yaw_threshold': 20,
            'pitch_threshold': 15,
            'roll_threshold': 20,
        },
        'analysis': {
            'warning_threshold': 5,
            'critical_threshold': 10,
            'severe_threshold': 20,
            'history_window': 300,  # 5 minutes
        },
        'alerting': {
            'enabled': True,
            'visual_alerts_enabled': True,
            'audible_alerts_enabled': True,
            'system_alerts_enabled': True,
            'cooldown': 5,
            'alert_sound_path': 'resources/alert_sound.wav',
        }
    }


def save_config(config: Dict[str, Any], config_path: str = "config/config.yaml") -> bool:
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration file
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        logger.info(f"Configuration saved to {config_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False
