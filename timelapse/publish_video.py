import base64

import time

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from PIL import Image

from camera import Camera

PUBLISH_CHANNEL = "jpeg_stream"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-8b7c30cc-019d-11e7-8520-02ee2ddab7fe'
pnconfig.publish_key = 'pub-c-498bda69-ba2d-457e-8154-7c26c091ce0a'
pnconfig.ssl = False

pubnub = PubNub(pnconfig)

camera = Camera()

def generate_jpegs():
    while True:
        time.sleep(0.5)
        yield camera.capture_preview()


class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        print status

    def message(self, pubnub, message):
        print('got message')

    def presence(self, pubnub, presence):
        pass

def publish_callback(result, status):
    print result

if __name__ == "__main__":

    my_listener = MyListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels("hello_world").execute()

    try:
        for jpeg_frame in generate_jpegs():
            from cStringIO import StringIO

            file_jpgdata = StringIO(jpeg_frame)
            dt = Image.open(file_jpgdata)
            dt = dt.resize((300, 200), Image.ANTIALIAS)

            output = StringIO()
            dt.save(output, format='JPEG', quality=90)
            im_data = output.getvalue()

            message = base64.b64encode(im_data)
            pubnub.publish().channel(PUBLISH_CHANNEL).message(message)\
                .should_store(True).use_post(True).async(publish_callback)
    except:
        camera.exit()
