from enum import Enum


class ContentType(Enum):
    kImage = 0
    kVideo = 1
    # Reserved content type, do not use this
    kReserved = 127


class ImageFormat(Enum):
    kJpeg = 0
    kReserved = 127


class OpenChannelParam(object):
    def __init__(self):
        self.host_ip
        self.port
        self.channel_name
        self.content_type


class Point(object):
        def __init__(self):
            self.x = 0
            self.y = 0


class DetectionResult(object):
    def __init__(self):
        self.lt = Point()
        self.rb = Point()
        self.result_text = None


class ImageFrame(object):
    def __init__(self):
        self.format = ImageFormat.kJpeg
        self.width = 0
        self.height = 0
        self.size = 0
        self.data = b''
        self.detection_results = []
