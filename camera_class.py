"""
A module for managing video camera streams and configurations.

This module provides the `VideoCameraObject` class, which implements functionalities for initializing video
camera streams, obtaining frames, and encoding them for streaming. The module leverages `cv2` for video
capture and incorporates adjustable properties for various camera settings such as resolution, FPS,
brightness, contrast, and more. Logging is used for monitoring camera actions and configurations.
"""

# pylint: disable=E1101

import cv2
from logmanager import logger
from app_control import settings


class VideoCameraObject:
    """
    Initializes the VideoCamera class.

    The constructor creates a VideoCapture object, which represents the video source. It sets the video source
    properties, such as frame rate, width, height, brightness, and contrast. If no video camera is found, an
    error message is logged.

    """
    def __init__(self, camera_index, camera_config):
        self.video = cv2.VideoCapture(camera_config['cameraID'])
        if not self.video.isOpened():
            logger.error('VideoCameraClass: No video camera found instance=%s', camera_index)
        else:
            logger.info('VideoCameraClass: Starting video camera %s as video_camera_instance_%s', camera_config['cameraID'], camera_index)
            self.video.set(cv2.CAP_PROP_FPS, camera_config['cameraFPS'])
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, camera_config['cameraWidth'])
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_config['cameraHeight'])
            self.video.set(cv2.CAP_PROP_BRIGHTNESS, camera_config['cameraBrightness'])
            self.video.set(cv2.CAP_PROP_CONTRAST, camera_config['cameraContrast'])
            self.video.set(cv2.CAP_PROP_SATURATION, camera_config['cameraSaturation'])
            self.video.set(cv2.CAP_PROP_HUE, camera_config['cameraHue'])
            self.video.set(cv2.CAP_PROP_GAMMA, camera_config['cameraGamma'])
            self.video.set(cv2.CAP_PROP_GAIN, camera_config['cameraGain'])
            self.video.set(cv2.CAP_PROP_SHARPNESS, camera_config['cameraSharpness'])
            logger.info('camera%s Video FPS %s', camera_index, self.video.get(cv2.CAP_PROP_FPS))
            logger.info('camera%s Video Width %s', camera_index, self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            logger.info('camera%s Video Height %s', camera_index, self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info('camera%s Video Backend %i', camera_index, self.video.get(cv2.CAP_PROP_BACKEND))
            logger.info('camera%s Video Brightness %i', camera_index, self.video.get(cv2.CAP_PROP_BRIGHTNESS))
            logger.info('camera%s Video Contrast %i', camera_index, self.video.get(cv2.CAP_PROP_CONTRAST))
            logger.info('camera%s Video Saturation %i', camera_index, self.video.get(cv2.CAP_PROP_SATURATION))
            logger.info('camera%s Video Sharpness %i', camera_index, self.video.get(cv2.CAP_PROP_SHARPNESS))
            logger.info('camera%s Video Hue %i', camera_index, self.video.get(cv2.CAP_PROP_HUE))
            logger.info('camera%s Video Gamma %i', camera_index, self.video.get(cv2.CAP_PROP_GAMMA))
            logger.info('camera%s Video Gain %i', camera_index, self.video.get(cv2.CAP_PROP_GAIN))


    def __del__(self):
        """Releases resources when app is closed down"""
        self.video.release()

    def get_frame(self):
        """Get a stream of raw images and encode as jpg files"""
        _ , frame = self.video.read()
        _ , jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def mpeg_stream(self):
        """Image processor, converts the stream of jpegs into an m-jpeg format for the browser"""
        while True:
            frame = self.get_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


video_camera_instance_0 = VideoCameraObject(0, settings['camera0'])
