import os
from pypylon import pylon
from imageio import get_writer

while True:
    try:
        fsamp = float(input('Sampling rate (Hz): '))
        break
    except ValueError:
        print('Invalid input.')

time_exposure = 1000000 / fsamp

available_cameras = pylon.TlFactory.find_devices()
cam = pylon.TlFactory.create_device(available_cameras[0])
cam.open()

cam.properties['ExposureTime'] = time_exposure

buffer = tuple(cam.grab_images(2000))
with get_writer(
       'output-filename.mkv',  # mkv players often support H.264
        fps=fsamp,  # FPS is in units Hz; should be real-time.
        codec='libx264',  # When used properly, this is basically
                          # "PNG for video" (i.e. lossless)
        quality=None,  # disables variable compression60
        pixelformat='rgb24',  # keep it as RGB colours
        ffmpeg_params=[  # compatibility with older library versions
            '-preset',  # set to faster, veryfast, superfast, ultrafast
            'fast',     # for higher speed but worse compression
            '-crf',  # quality; set to 0 for lossless, but keep in mind
            '11'     # that the camera probably adds static anyway
        ]
) as writer:
    for image in buffer:
        writer.append_data(image)
del buffer