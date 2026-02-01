# Driver Distraction Detector

A real-time computer vision system for detecting driver distraction using Raspberry Pi and MediaPipe Face Mesh.

## Project Structure

```
driver_distraction_detector/
├── main.py                          # Main entry point
├── hardware/
│   ├── raspberry_pi_manager.py     # Bluetooth connection to Raspberry Pi
│   └── camera_manager.py           # Camera stream management
├── vision/
│   └── face_mesh_analyzer.py       # MediaPipe face mesh analysis
├── analysis/
│   └── distraction_analyzer.py     # Distraction tracking and analysis
├── alerting/
│   └── alert_manager.py            # Alert triggering and notifications
├── config/
│   ├── settings.py                 # Configuration management
│   └── config.yaml                 # Configuration file
├── utils/
│   └── metrics.py                  # Metrics recording and analysis
├── tests/
│   ├── test_components.py          # Unit tests
│   └── mocks.py                    # Mock objects for testing
└── requirements.txt                # Python dependencies
```

## Components Overview

### Hardware Layer
- **RaspberryPiManager**: Manages Bluetooth connection to Raspberry Pi
- **CameraManager**: Receives and buffers camera frames (1 FPS)

### Vision Pipeline
- **FaceMeshAnalyzer**: Uses MediaPipe to:
  - Detect facial landmarks
  - Calculate head orientation (pitch, yaw, roll)
  - Estimate eye gaze direction
  - Classify face pointing direction (forward/left/right/up/down)
  - Classify eye gaze direction (forward/left/right/up/down)

### Analysis Layer
- **DistractionAnalyzer**: Tracks distraction patterns
  - Counts face failures (not pointing towards road)
  - Counts eye failures (not looking forward)
  - Determines distraction level based on thresholds
  - Generates consequences and recommendations

### Alerting System
- **AlertManager**: Manages alerts based on distraction level
  - Visual alerts (warning level)
  - Audible alerts (critical level)
  - System interventions (severe level)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Raspberry Pi Bluetooth address in `config/config.yaml`

3. Update other settings as needed (thresholds, alert preferences, etc.)

## Usage

Run the main program:
```bash
python main.py
```

## Key Features to Implement

- [ ] Bluetooth connection to Raspberry Pi
- [ ] Camera stream reception and buffering
- [ ] Head pose estimation (pitch, yaw, roll calculation)
- [ ] Eye gaze direction estimation
- [ ] Distraction level determination logic
- [ ] Consequence assignment based on failure patterns
- [ ] Visual alert display system
- [ ] Audible alert generation
- [ ] System intervention triggers
- [ ] Performance optimization for real-time processing
- [ ] Metrics and logging system
- [ ] Testing and validation

## Configuration

Edit `config/config.yaml` to customize:
- Raspberry Pi Bluetooth address
- Camera resolution and FPS
- Face orientation thresholds
- Distraction level thresholds
- Alert preferences

## Development Notes

### Function Stubs to Implement

1. **FaceMeshAnalyzer._calculate_head_orientation()**: Use 3D landmarks for head pose estimation
2. **FaceMeshAnalyzer._calculate_eye_gaze()**: Calculate gaze direction from iris/eye landmarks
3. **FaceMeshAnalyzer._classify_face_orientation()**: Classify based on angle thresholds
4. **DistractionAnalyzer._determine_distraction_level()**: Complex logic for level determination
5. **CameraManager._get_frame_from_stream()**: Implement actual frame reception from Pi
6. **RaspberryPiManager.connect()**: Implement Bluetooth connection
7. **Main.run_detection_loop()**: Implement main processing loop

### Testing

Run unit tests:
```bash
python -m unittest tests/test_components.py
```

Mock objects available in `tests/mocks.py` for development.
