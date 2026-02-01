# Installation and Setup Guide

## Dependencies Installed

Successfully installed the following core dependencies:

- **numpy**: Numerical arrays and operations
- **opencv-python**: Image processing and computer vision
- **mediapipe**: Face mesh detection and landmark tracking  
- **PyYAML**: Configuration file parsing

### Note on PyBluez (Bluetooth)

PyBluez is included in the codebase structure but requires special setup:
- **On Linux**: `sudo apt-get install python3-bluez` or compile from source
- **On Windows**: Use windows-curses compatible version
- **On macOS**: Use homebrew

Since PyBluez has compatibility issues with modern Python, we've kept it optional. The `RaspberryPiManager` class uses it but has try-except error handling.

## Virtual Environment

A Python virtual environment has been created at:
```
driver_distraction_detector/venv/
```

### Activating the Virtual Environment

**On Linux/macOS:**
```bash
cd driver_distraction_detector
source venv/bin/activate
```

**On Windows:**
```bash
cd driver_distraction_detector
venv\Scripts\activate
```

### Deactivating the Virtual Environment

```bash
deactivate
```

## Running the System

With the virtual environment activated:

```bash
# From inside driver_distraction_detector directory
python main.py
```

## Troubleshooting Installation

### MediaPipe Issues

If you get errors related to MediaPipe, you may need system libraries:

**On Ubuntu/Debian:**
```bash
sudo apt-get install libopenblas0 libopenblas-base libopenblas-dev
sudo apt-get install liblapack3 liblapack-dev
```

**On macOS:**
```bash
brew install openblas lapack
```

### OpenCV Display Issues

If you can't display images, install:

**On Ubuntu/Debian:**
```bash
sudo apt-get install libsm6 libxext6 libxrender-dev
```

## Project Ready

The project structure is now ready for development. See [README.md](README.md) for architecture details and [DEVELOPMENT.md](DEVELOPMENT.md) for implementation guidelines.

## Next Steps

1. Install PyBluez (if developing Bluetooth functionality):
   ```bash
   # May require system dependencies and compilation
   pip install pybluez
   ```

2. Update `config/config.yaml` with your Raspberry Pi's Bluetooth address

3. Implement the TODO functions in:
   - `vision/face_mesh_analyzer.py`
   - `analysis/distraction_analyzer.py`
   - `hardware/camera_manager.py`
   - `main.py`

4. Run tests to validate implementations:
   ```bash
   python -m unittest tests/test_components.py
   ```
