from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from videoopencv import IteraVideo, AbreVideo

class KivyCV(Image):
    def __init__(self, capture, fps, **kwargs):
        Image.__init__(self, **kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            
            IteraVideo()
            
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class OpenCVApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        my_camera = KivyCV(capture=self.capture, fps=60)
        return my_camera

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    OpenCVApp().run()