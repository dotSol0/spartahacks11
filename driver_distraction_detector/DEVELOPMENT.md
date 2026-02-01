# Development Setup

This guide helps you set up the development environment for the Driver Distraction Detector.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (optional but recommended)

## Step 1: Create Virtual Environment (Optional)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependency Breakdown

- **numpy**: Numerical computing and array operations
- **opencv-python**: Computer vision operations and image processing
- **mediapipe**: Face mesh detection and landmark tracking
- **pybluez**: Bluetooth communication with Raspberry Pi
- **PyYAML**: Configuration file parsing

## Step 3: Configure Hardware

1. Find your Raspberry Pi's Bluetooth address:
   ```bash
   hcitool scan
   ```

2. Update `config/config.yaml` with your Pi's address:
   ```yaml
   raspberry_pi:
     bluetooth_address: "YOUR:PI:ADDRESS:HERE"
   ```

## Step 4: Run the System

```bash
python main.py
```

## Troubleshooting

### Import Errors
If you get import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Bluetooth Connection Issues
- Ensure Raspberry Pi is powered on and in range
- Verify the Bluetooth address is correct
- Check Bluetooth adapter is enabled on your computer

### MediaPipe Issues
MediaPipe requires specific system libraries. On Ubuntu/Debian:
```bash
sudo apt-get install libopenblas0 libopenblas-base libopenblas-dev
```

## Next Steps

1. Review the architecture in [driver_distraction_detector/README.md](README.md)
2. Implement the TODO functions (see README for list)
3. Write tests for your implementations
4. Validate with real camera data

## Resources

- [MediaPipe Face Mesh Documentation](https://google.github.io/mediapipe/solutions/face_mesh)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyBluez Documentation](https://github.com/pybluez/pybluez)
