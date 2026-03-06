# None

<a id="camera_class"></a>

# camera\_class

A module for managing video camera streams and configurations.

This module provides the `VideoCameraObject` class, which implements functionalities for initializing video
camera streams, obtaining frames, and encoding them for streaming. The module leverages `cv2` for video
capture and incorporates adjustable properties for various camera settings such as resolution, FPS,
brightness, contrast, and more. Logging is used for monitoring camera actions and configurations.

<a id="camera_class.cv2"></a>

## cv2

<a id="camera_class.logger"></a>

## logger

<a id="camera_class.settings"></a>

## settings

<a id="camera_class.VideoCameraObject"></a>

## VideoCameraObject Objects

```python
class VideoCameraObject()
```

Initializes the VideoCamera class.

The constructor creates a VideoCapture object, which represents the video source. It sets the video source
properties, such as frame rate, width, height, brightness, and contrast. If no video camera is found, an
error message is logged.

<a id="camera_class.VideoCameraObject.__init__"></a>

#### \_\_init\_\_

```python
def __init__(camera_index, camera_config)
```

<a id="camera_class.VideoCameraObject.__del__"></a>

#### \_\_del\_\_

```python
def __del__()
```

Releases resources when app is closed down

<a id="camera_class.VideoCameraObject.get_frame"></a>

#### get\_frame

```python
def get_frame()
```

Get a stream of raw images and encode as jpg files

<a id="camera_class.VideoCameraObject.mpeg_stream"></a>

#### mpeg\_stream

```python
def mpeg_stream()
```

Image processor, converts the stream of jpegs into an m-jpeg format for the browser

<a id="camera_class.video_camera_instance_0"></a>

#### video\_camera\_instance\_0

