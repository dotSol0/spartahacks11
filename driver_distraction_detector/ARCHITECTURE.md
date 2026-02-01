# Project Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN SYSTEM COORDINATOR                       │
│                    (main.py)                                     │
└────────┬──────────────┬──────────────┬──────────────┬────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
    ┌────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐
    │ HARDWARE│   │ VISION   │   │ ANALYSIS │   │ALERTING │
    │ LAYER   │   │ PIPELINE │   │ ENGINE   │   │ SYSTEM  │
    └────────┘   └──────────┘   └──────────┘   └─────────┘
         │              │              │              │
    ┌────┴────┐    ┌────┴────┐   ┌────┴────┐   ┌───┴────┐
    │  RasPi  │    │ MediaPipe   │Distraction   │Visual  │
    │ Bluetooth   │Face Mesh     │Analysis     │Audible │
    │ Connection  │Analysis      │Engine       │System  │
    │             │              │             │Alerts  │
    │  Camera     │              │             │        │
    │Stream       │              │             │        │
    │ Handler     │              │             │        │
    └────────────┘ └──────────────┘ └──────────┘ └───────┘
```

## Data Flow

```
Raspberry Pi Camera
        │ (1 frame/second via Bluetooth)
        ▼
Camera Manager (buffers frames)
        │
        ▼
Face Mesh Analyzer
        │
        ├─ Head Orientation Analysis (pitch, yaw, roll)
        │
        ├─ Eye Gaze Estimation
        │
        └─ Landmarks & Confidence
                │
                ▼
        ┌──────────────────┐
        │  Face Forward?   │◄─────┐
        │  Eyes Forward?   │      │
        └────────┬─────────┘      │
                │ (failures)      │
                ▼                 │
        ┌──────────────────┐      │
        │  Distraction     │──────┘
        │  Analyzer        │
        │                  │
        │ Tracks:          │
        │ - Face Failures  │
        │ - Eye Failures   │
        │ - Patterns       │
        │ - Levels         │
        └────────┬─────────┘
                │
                ▼
        ┌──────────────────┐
        │  Alert Manager   │
        │                  │
        │ Triggers:        │
        │ - Visual Alerts  │
        │ - Audible Alerts │
        │ - System Actions │
        └──────────────────┘
```

## File Structure Details

### Hardware Interface (`hardware/`)
- **raspberry_pi_manager.py**: Bluetooth connection management
  - `connect()`: Establish Bluetooth connection
  - `send_command()`: Send commands to Pi
  - `receive_data()`: Receive camera stream data
  
- **camera_manager.py**: Camera stream handling
  - `get_frame()`: Retrieve latest frame
  - `_capture_frames()`: Background frame capture thread
  - Maintains 1 FPS frame rate

### Vision Pipeline (`vision/`)
- **face_mesh_analyzer.py**: MediaPipe-based face analysis
  - `analyze_frame()`: Process single frame
  - `_calculate_head_orientation()`: Calculate head pose angles
  - `_calculate_eye_gaze()`: Estimate eye direction
  - `is_face_forward()`: Check if face points to road
  - `are_eyes_forward()`: Check if eyes look forward

### Analysis Engine (`analysis/`)
- **distraction_analyzer.py**: Distraction pattern analysis
  - `process_frame_result()`: Process analysis results
  - `_determine_distraction_level()`: Calculate overall level
  - `_determine_consequence()`: Map level to consequence
  - Tracks failure counts and events over time

### Alerting System (`alerting/`)
- **alert_manager.py**: Alert coordination
  - `VisualAlertHandler`: Screen/dashboard alerts
  - `AudibleAlertHandler`: Sound/voice alerts
  - `SystemAlertHandler`: Emergency system interventions

### Configuration (`config/`)
- **settings.py**: Configuration loader
- **config.yaml**: Configuration file (editable)

### Utilities (`utils/`)
- **metrics.py**: Performance monitoring and data recording
  - `MetricsRecorder`: Records frame analysis results
  - `PerformanceMonitor`: Tracks FPS and latency

### Testing (`tests/`)
- **test_components.py**: Unit tests (templates)
- **mocks.py**: Mock objects for testing

## Key Implementation Areas

### 1. Head Pose Estimation
**File**: `vision/face_mesh_analyzer.py` - `_calculate_head_orientation()`
- Use 3D face landmarks from MediaPipe
- Calculate euler angles (pitch, yaw, roll)
- Reference points: nose, chin, ears, eyes

### 2. Eye Gaze Detection
**File**: `vision/face_mesh_analyzer.py` - `_calculate_eye_gaze()`
- Analyze iris landmarks or eye corner positions
- Estimate gaze direction relative to face
- Convert to angular measurements

### 3. Distraction Level Logic
**File**: `analysis/distraction_analyzer.py` - `_determine_distraction_level()`
- SAFE: 0-4 failures
- WARNING: 5-9 failures
- CRITICAL: 10-19 failures
- SEVERE: 20+ failures
- Consider consecutive failures and frequency

### 4. Real-time Processing Loop
**File**: `main.py` - `run_detection_loop()`
- Get frame every 1 second
- Process through vision pipeline
- Analyze results for distraction
- Trigger alerts if needed
- Log metrics

## Configuration Parameters

Edit `config/config.yaml`:

```yaml
raspberry_pi:
  bluetooth_address: "B8:27:EB:XX:XX:XX"  # Your Pi's address
  bluetooth_port: 1

camera:
  target_fps: 1              # 1 frame per second
  width: 640
  height: 480

vision:
  yaw_threshold: 20          # Head left/right degrees
  pitch_threshold: 15        # Head up/down degrees
  roll_threshold: 20         # Head tilt degrees

analysis:
  warning_threshold: 5       # Failures to trigger warning
  critical_threshold: 10     # Failures to trigger critical
  severe_threshold: 20       # Failures to trigger severe
  history_window: 300        # 5 minute tracking window

alerting:
  enabled: true
  visual_alerts_enabled: true
  audible_alerts_enabled: true
  system_alerts_enabled: true
  cooldown: 5                # Seconds between alerts
```

## Testing Strategy

1. **Unit Tests**: Test individual components
   ```bash
   python -m unittest tests/test_components.py
   ```

2. **Integration Tests**: Test component interactions

3. **End-to-End Tests**: Test with real camera/Pi

4. **Performance Tests**: Validate real-time performance

## Development Roadmap

- [ ] Phase 1: Hardware Integration
  - [ ] Implement Bluetooth connection
  - [ ] Stream camera frames from Pi
  
- [ ] Phase 2: Vision Pipeline
  - [ ] Head pose estimation
  - [ ] Eye gaze detection
  - [ ] Classification logic
  
- [ ] Phase 3: Analysis Engine
  - [ ] Failure tracking
  - [ ] Distraction level calculation
  - [ ] Consequence assignment
  
- [ ] Phase 4: Alerting System
  - [ ] Visual alerts
  - [ ] Audible alerts
  - [ ] System interventions
  
- [ ] Phase 5: Optimization & Testing
  - [ ] Performance optimization
  - [ ] Comprehensive testing
  - [ ] Edge case handling
  - [ ] Production deployment

## Getting Started

1. Read [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions
2. Activate virtual environment: `source venv/bin/activate`
3. Update `config/config.yaml` with your hardware info
4. Start implementing TODO functions
5. Run tests frequently to validate work
6. Check [README.md](README.md) for detailed component documentation
