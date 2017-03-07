import gphoto2 as gp
from datetime import datetime


class Camera(object):

    def __init__(self):
        # Initialise the camera
        self.context = gp.Context()
        self.camera = gp.Camera()
        self.camera.init(self.context)
        # Check image format and determine the correct file suffix
        self.file_suffix = self.get_file_suffix()

    def capture_image(self):
        print('capturing image...')
        self.camera.trigger_capture(self.context)
        timestamp = datetime.now().isoformat()
        event = [0, None]

        while event[0] != gp.GP_EVENT_FILE_ADDED:
            event = self.camera.wait_for_event(5000, self.context)

        path = event[1]
        image = self.camera.file_get(path.folder, path.name, gp.GP_FILE_TYPE_NORMAL, self.context)
        data = memoryview(image.get_data_and_size())
        filename = 'img_' + timestamp + self.file_suffix

        print('saving image of size ' + str(len(data)) + ' bytes with name ' + filename)
        image.save(filename)

    def capture_preview(self):
        # self.camera.init(self.context)
        image = self.camera.capture_preview(self.context)
        data = memoryview(image.get_data_and_size())
        # self.camera.exit(self.context)
        return data

    def get_file_suffix(self):
        config = self.camera.get_config(self.context)
        image_format = config.get_child_by_name('imgsettings').get_child_by_name('imageformat').get_value()
        return '.cr2' if image_format == 'RAW' else '.jpg'

    def exit(self):
        self.camera.exit(self.context)
