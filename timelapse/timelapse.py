import schedule as schedule
import time

from camera import Camera

camera = Camera()

interval = 1
max_frames = 10

num_frames_taken = 0


def main():
    take_picture()
    schedule.every(interval).seconds.do(take_picture)

    while num_frames_taken < max_frames:
        schedule.run_pending()
        time.sleep(0.01)

    camera.exit()


def take_picture():
    global num_frames_taken

    camera.capture_image()
    num_frames_taken += 1

    if num_frames_taken >= max_frames:
        return schedule.CancelJob


if __name__ == '__main__':
    main()
