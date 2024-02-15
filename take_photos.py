from picamera import PiCamera
from time import sleep
cam = PiCamera()
cam.resolution = (4056, 3040)

def take_5_photos():
    for i in range(5):
        print("HI WHAT'S UP HERE?")
        print('photos_for_speed/image_%s.jpg' % i)
        cam.capture('photos_for_speed/image_%s.jpg' % i)
        sleep(1)


# take_5_photos()
