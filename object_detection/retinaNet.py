import os
from imageai.Detection import VideoObjectDetection
from imageai.Detection import ObjectDetection
import time


# Object Detection with RetinaNet on images
def retinanet_image(image, model, output):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model)
    detector.loadModel()
    start_time = time.time()
    detections = detector.detectObjectsFromImage(input_image=image, output_image_path=output)
    for eachObject in detections:
        print(eachObject["name"], " : ", eachObject["percentage_probability"])
    print("Total time: %s seconds" % (time.time() - start_time))


# Object Detection with RetinaNet on video
def retinanet_video(video, model, output):
    detector = VideoObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model)
    detector.loadModel()
    start_time = time.time()
    video_path = detector.detectObjectsFromVideo(input_file_path=video, output_file_path=output, frames_per_second=29,
                                                 log_progress=True)
    print(video_path)
    print("Total time: %s seconds" % (time.time() - start_time))
