import threading

import cv2


class VideoCamera:
    """
    Process video stream.
    Collect same urls to process video and
    to not process same streams at the same time.
    """

    class __VideoCamera:
        active = True

        def __init__(self, camera_url, fps, size, *args, **kwargs):
            """
            Initialize thread with camera images.
            :param camera_url: url to camera stream
            """
            self.camera_url = camera_url
            self.video = cv2.VideoCapture(camera_url)
            self.video.set(cv2.CAP_PROP_FPS, fps)
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
            (self.grabbed, self.frame) = self.video.read()
            # threading.Thread(target=self.update, args=()).start()
            self.start()

        def start(self):
            # start a thread to read frames from the file video stream
            thd = threading.Thread(target=self.update, args=())
            thd.daemon = True
            thd.start()
            return self

        def __del__(self):
            self.video.release()
            cv2.destroyAllWindows()

        def get_frame(self):
            image = self.frame
            try:
                ret, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()
            except:
                return b''

        def update(self):
            while self.active:
                (self.grabbed, self.frame) = self.video.read()
            self.__del__()

    instances = []

    def __new__(cls, camera_url, *args, **kwargs):
        matches = [item for item in cls.instances
                   if item.camera_url == camera_url]
        for match in matches:
            match.active = False
        instance = VideoCamera.__VideoCamera(camera_url, *args, **kwargs)
        cls.instances.append(instance)
        return instance


def gen(camera):
    """Generate images from video."""
    while True:
        frame = camera.get_frame()
        if frame is b'':
            del camera
            raise StopIteration
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n\r\n')
